# -*- coding: utf-8 -*-
from odoo import models, fields, api


class GymTrainer(models.Model):
    _name = 'gym.trainer'
    _description = 'Gym Trainer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _rec_name = 'name'

    name = fields.Char(string='Trainer Name', required=True, tracking=True)
    ref = fields.Char(
        string='Reference',
        readonly=True,
        copy=False,
        default='New',
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Related Partner',
        tracking=True,
    )
    image_1920 = fields.Binary(string='Photo', attachment=True)
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        string='Gender',
        tracking=True,
    )
    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    skill_ids = fields.Many2many(
        'gym.trainer.skill',
        'gym_trainer_skill_rel',
        'trainer_id',
        'skill_id',
        string='Skills',
    )
    specialization = fields.Char(string='Specialization')
    joining_date = fields.Date(string='Joining Date', tracking=True)
    trainer_fee = fields.Float(string='Trainer Fee', tracking=True)
    member_ids = fields.One2many(
        'gym.member',
        'trainer_id',
        string='Assigned Members',
    )
    member_count = fields.Integer(
        string='Member Count',
        compute='_compute_member_count',
    )
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ref', 'New') == 'New':
                vals['ref'] = self.env['ir.sequence'].next_by_code('gym.trainer') or 'New'
        return super().create(vals_list)

    def _compute_member_count(self):
        for rec in self:
            rec.member_count = len(rec.member_ids)

    def action_view_members(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Members',
            'res_model': 'gym.member',
            'view_mode': 'list,form',
            'domain': [('trainer_id', '=', self.id)],
            'context': {'default_trainer_id': self.id},
        }

    _constraints = [
        models.Constraint('unique(ref)', 'Trainer reference must be unique!'),
    ]
