# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class GymMembershipWizard(models.TransientModel):
    _name = 'gym.membership.wizard'
    _description = 'Purchase Membership Wizard'

    member_id = fields.Many2one(
        'gym.member',
        string='Member',
        required=True,
    )
    membership_type_id = fields.Many2one(
        'gym.membership.type',
        string='Membership Type',
        required=True,
    )
    date_start = fields.Date(
        string='Start Date',
        required=True,
        default=fields.Date.today,
    )
    trainer_id = fields.Many2one(
        'gym.trainer',
        string='Trainer',
    )
    trainer_fee = fields.Float(string='Trainer Fee', default=0.0)
    create_invoice = fields.Boolean(
        string='Create Invoice',
        default=True,
        help='If checked, an invoice will be created for this membership.',
    )
    price = fields.Float(
        string='Membership Fee',
        related='membership_type_id.price',
        readonly=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='membership_type_id.currency_id',
        readonly=True,
    )

    def action_purchase_membership(self):
        self.ensure_one()

        # Check for existing active membership
        existing = self.env['gym.membership'].search([
            ('member_id', '=', self.member_id.id),
            ('state', '=', 'active'),
        ])
        if existing:
            raise UserError(
                f'Member {self.member_id.name} already has an active membership ({existing[0].ref})!'
            )

        membership_vals = {
            'member_id': self.member_id.id,
            'membership_type_id': self.membership_type_id.id,
            'date_start': self.date_start,
            'trainer_id': self.trainer_id.id if self.trainer_id else False,
            'trainer_fee': self.trainer_fee,
        }

        # Update member's trainer if one is selected
        if self.trainer_id:
            self.member_id.trainer_id = self.trainer_id

        membership = self.env['gym.membership'].create(membership_vals)

        if self.create_invoice:
            membership.action_create_invoice()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Membership',
            'res_model': 'gym.membership',
            'res_id': membership.id,
            'view_mode': 'form',
            'target': 'current',
        }
