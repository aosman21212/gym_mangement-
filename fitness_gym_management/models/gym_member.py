# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date


class GymMember(models.Model):
    _name = 'gym.member'
    _description = 'Gym Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _rec_name = 'name'

    name = fields.Char(string='Member Name', required=True, tracking=True)
    ref = fields.Char(
        string='Member ID',
        readonly=True,
        copy=False,
        default='New',
        tracking=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Related Partner',
        tracking=True,
    )
    image_1920 = fields.Binary(string='Photo', attachment=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True,
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        string='Gender',
        tracking=True,
    )
    blood_group = fields.Selection(
        [
            ('a+', 'A+'), ('a-', 'A-'),
            ('b+', 'B+'), ('b-', 'B-'),
            ('ab+', 'AB+'), ('ab-', 'AB-'),
            ('o+', 'O+'), ('o-', 'O-'),
        ],
        string='Blood Group',
    )
    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    street = fields.Char(string='Street')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')
    trainer_id = fields.Many2one(
        'gym.trainer',
        string='Assigned Trainer',
        tracking=True,
    )
    membership_ids = fields.One2many(
        'gym.membership',
        'member_id',
        string='Memberships',
    )
    active_membership_id = fields.Many2one(
        'gym.membership',
        string='Active Membership',
        compute='_compute_active_membership',
        store=False,
    )
    membership_status = fields.Selection(
        [('active', 'Active'), ('inactive', 'Inactive'), ('expired', 'Expired')],
        string='Membership Status',
        compute='_compute_membership_status',
        store=True,
    )
    bmi_bmr_ids = fields.One2many(
        'gym.bmi.bmr',
        'member_id',
        string='BMI/BMR Records',
    )
    workout_plan_ids = fields.One2many(
        'gym.workout.plan',
        'member_id',
        string='Workout Plans',
    )
    diet_plan_ids = fields.One2many(
        'gym.diet.plan',
        'member_id',
        string='Diet Plans',
    )
    membership_count = fields.Integer(
        string='Memberships',
        compute='_compute_counts',
    )
    workout_plan_count = fields.Integer(
        string='Workout Plans',
        compute='_compute_counts',
    )
    diet_plan_count = fields.Integer(
        string='Diet Plans',
        compute='_compute_counts',
    )
    bmi_count = fields.Integer(
        string='BMI Records',
        compute='_compute_counts',
    )
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ref', 'New') == 'New':
                vals['ref'] = self.env['ir.sequence'].next_by_code('gym.member') or 'New'
        return super().create(vals_list)

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.date_of_birth:
                dob = rec.date_of_birth
                rec.age = today.year - dob.year - (
                    (today.month, today.day) < (dob.month, dob.day)
                )
            else:
                rec.age = 0

    @api.depends('membership_ids', 'membership_ids.state')
    def _compute_active_membership(self):
        for rec in self:
            active = rec.membership_ids.filtered(lambda m: m.state == 'active')
            rec.active_membership_id = active[:1] if active else False

    @api.depends('membership_ids', 'membership_ids.state')
    def _compute_membership_status(self):
        for rec in self:
            active = rec.membership_ids.filtered(lambda m: m.state == 'active')
            if active:
                rec.membership_status = 'active'
            else:
                expired = rec.membership_ids.filtered(lambda m: m.state == 'expired')
                if expired:
                    rec.membership_status = 'expired'
                else:
                    rec.membership_status = 'inactive'

    def _compute_counts(self):
        for rec in self:
            rec.membership_count = len(rec.membership_ids)
            rec.workout_plan_count = len(rec.workout_plan_ids)
            rec.diet_plan_count = len(rec.diet_plan_ids)
            rec.bmi_count = len(rec.bmi_bmr_ids)

    def action_view_memberships(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Memberships',
            'res_model': 'gym.membership',
            'view_mode': 'list,form',
            'domain': [('member_id', '=', self.id)],
            'context': {'default_member_id': self.id},
        }

    def action_view_workout_plans(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Workout Plans',
            'res_model': 'gym.workout.plan',
            'view_mode': 'list,form',
            'domain': [('member_id', '=', self.id)],
            'context': {'default_member_id': self.id},
        }

    def action_view_diet_plans(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Diet Plans',
            'res_model': 'gym.diet.plan',
            'view_mode': 'list,form',
            'domain': [('member_id', '=', self.id)],
            'context': {'default_member_id': self.id},
        }

    def action_view_bmi_bmr(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'BMI/BMR Records',
            'res_model': 'gym.bmi.bmr',
            'view_mode': 'list,form',
            'domain': [('member_id', '=', self.id)],
            'context': {'default_member_id': self.id},
        }

    def action_open_membership_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Membership',
            'res_model': 'gym.membership.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_member_id': self.id,
                'default_trainer_id': self.trainer_id.id,
            },
        }

    _constraints = [
        models.Constraint('unique(ref)', 'Member reference must be unique!'),
    ]
