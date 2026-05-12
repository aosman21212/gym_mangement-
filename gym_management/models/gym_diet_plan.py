# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GymDietPlan(models.Model):
    _name = 'gym.diet.plan'
    _description = 'Diet Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc'

    name = fields.Char(string='Plan Name', required=True, tracking=True)
    member_id = fields.Many2one(
        'gym.member',
        string='Member',
        required=True,
        tracking=True,
        ondelete='cascade',
    )
    trainer_id = fields.Many2one(
        'gym.trainer',
        string='Trainer / Nutritionist',
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
        required=True,
        tracking=True,
    )
    diet_line_ids = fields.One2many(
        'gym.diet.plan.line',
        'diet_plan_id',
        string='Diet Items',
    )
    total_calories = fields.Float(
        string='Total Daily Calories',
        compute='_compute_total_calories',
        store=True,
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('completed', 'Completed'),
        ],
        string='Status',
        default='draft',
        tracking=True,
    )
    notes = fields.Text(string='Notes')

    @api.depends('diet_line_ids', 'diet_line_ids.calories')
    def _compute_total_calories(self):
        for rec in self:
            rec.total_calories = sum(rec.diet_line_ids.mapped('calories'))

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_end and rec.date_start and rec.date_end < rec.date_start:
                raise ValidationError('End date must be greater than or equal to start date!')

    def action_activate(self):
        self.write({'state': 'active'})

    def action_complete(self):
        self.write({'state': 'completed'})

    def action_reset_draft(self):
        self.write({'state': 'draft'})


class GymDietPlanLine(models.Model):
    _name = 'gym.diet.plan.line'
    _description = 'Diet Plan Line'
    _order = 'diet_day, id'

    diet_plan_id = fields.Many2one(
        'gym.diet.plan',
        string='Diet Plan',
        required=True,
        ondelete='cascade',
    )
    food_item_id = fields.Many2one(
        'gym.food.item',
        string='Food Item',
        required=True,
    )
    diet_interval_id = fields.Many2one(
        'gym.diet.interval',
        string='Meal',
        required=True,
    )
    diet_day = fields.Selection(
        [
            ('monday', 'Monday'),
            ('tuesday', 'Tuesday'),
            ('wednesday', 'Wednesday'),
            ('thursday', 'Thursday'),
            ('friday', 'Friday'),
            ('saturday', 'Saturday'),
            ('sunday', 'Sunday'),
        ],
        string='Day',
        required=True,
    )
    quantity = fields.Float(
        string='Quantity (g)',
        default=100.0,
        required=True,
    )
    calories = fields.Float(
        string='Calories',
        compute='_compute_calories',
        store=True,
    )
    notes = fields.Char(string='Notes')

    @api.depends('food_item_id', 'food_item_id.calories', 'quantity')
    def _compute_calories(self):
        for rec in self:
            if rec.food_item_id and rec.quantity:
                # calories per 100g * quantity / 100
                rec.calories = (rec.food_item_id.calories * rec.quantity) / 100.0
            else:
                rec.calories = 0.0
