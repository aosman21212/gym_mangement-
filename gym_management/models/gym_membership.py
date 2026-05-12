# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta


class GymMembership(models.Model):
    _name = 'gym.membership'
    _description = 'Gym Membership'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc'
    _rec_name = 'ref'

    ref = fields.Char(
        string='Reference',
        readonly=True,
        copy=False,
        default='New',
        tracking=True,
    )
    member_id = fields.Many2one(
        'gym.member',
        string='Member',
        required=True,
        tracking=True,
        ondelete='cascade',
    )
    membership_type_id = fields.Many2one(
        'gym.membership.type',
        string='Membership Type',
        required=True,
        tracking=True,
    )
    date_start = fields.Date(
        string='Start Date',
        required=True,
        default=fields.Date.today,
        tracking=True,
    )
    date_end = fields.Date(
        string='End Date',
        compute='_compute_date_end',
        store=True,
        tracking=True,
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('expired', 'Expired'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        compute='_compute_state',
        store=True,
        tracking=True,
    )
    invoice_id = fields.Many2one(
        'account.move',
        string='Invoice',
        readonly=True,
        copy=False,
        tracking=True,
    )
    trainer_id = fields.Many2one(
        'gym.trainer',
        string='Trainer',
        tracking=True,
    )
    trainer_fee = fields.Float(string='Trainer Fee', tracking=True)
    price = fields.Float(
        string='Membership Fee',
        related='membership_type_id.price',
        store=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        readonly=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ref', 'New') == 'New':
                vals['ref'] = self.env['ir.sequence'].next_by_code('gym.membership') or 'New'
        return super().create(vals_list)

    @api.depends('date_start', 'membership_type_id', 'membership_type_id.duration')
    def _compute_date_end(self):
        for rec in self:
            if rec.date_start and rec.membership_type_id:
                duration = rec.membership_type_id.duration
                rec.date_end = rec.date_start + timedelta(days=duration)
            else:
                rec.date_end = False

    @api.depends('date_start', 'date_end', 'state')
    def _compute_state(self):
        today = date.today()
        for rec in self:
            if rec.state == 'cancelled':
                continue
            if not rec.date_start:
                rec.state = 'draft'
            elif rec.date_end and today > rec.date_end:
                rec.state = 'expired'
            elif rec.date_start <= today and (not rec.date_end or today <= rec.date_end):
                rec.state = 'active'
            else:
                rec.state = 'draft'

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_create_invoice(self):
        self.ensure_one()
        if self.invoice_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Invoice',
                'res_model': 'account.move',
                'res_id': self.invoice_id.id,
                'view_mode': 'form',
            }

        partner = self.member_id.partner_id
        if not partner:
            # Create a partner from member if none linked
            partner = self.env['res.partner'].create({
                'name': self.member_id.name,
                'phone': self.member_id.phone,
                'email': self.member_id.email,
            })
            self.member_id.partner_id = partner

        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'name': f'Membership: {self.membership_type_id.name} ({self.ref})',
                'quantity': 1.0,
                'price_unit': self.membership_type_id.price,
            })],
            'narration': f'Membership for {self.member_id.name} from {self.date_start} to {self.date_end}',
        }

        # Add trainer fee line if applicable
        if self.trainer_fee > 0 and self.trainer_id:
            invoice_vals['invoice_line_ids'].append((0, 0, {
                'name': f'Trainer Fee: {self.trainer_id.name}',
                'quantity': 1.0,
                'price_unit': self.trainer_fee,
            }))

        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_id = invoice

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
        }

    _constraints = [
        models.Constraint('unique(ref)', 'Membership reference must be unique!'),
    ]
