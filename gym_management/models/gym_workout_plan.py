# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GymWorkoutPlan(models.Model):
    _name = 'gym.workout.plan'
    _description = 'Workout Plan'
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
        string='Trainer',
        tracking=True,
    )
    category_id = fields.Many2one(
        'gym.workout.category',
        string='Category',
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
    workout_line_ids = fields.One2many(
        'gym.workout.plan.line',
        'workout_plan_id',
        string='Exercises',
    )
    total_calories = fields.Float(
        string='Total Calories Burned',
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

    @api.depends('workout_line_ids', 'workout_line_ids.calories')
    def _compute_total_calories(self):
        for rec in self:
            rec.total_calories = sum(rec.workout_line_ids.mapped('calories'))

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_end and rec.date_start and rec.date_end < rec.date_start:
                raise ValidationError('End date must be greater than or equal to start date!')

    @api.constrains('workout_line_ids')
    def _check_workout_lines(self):
        for rec in self:
            if rec.state != 'draft' and not rec.workout_line_ids:
                raise ValidationError('A workout plan must have at least one exercise!')

    def action_activate(self):
        for rec in self:
            if not rec.workout_line_ids:
                raise ValidationError('Please add at least one exercise before activating the plan!')
            rec.state = 'active'

    def action_complete(self):
        self.write({'state': 'completed'})

    def action_reset_draft(self):
        self.write({'state': 'draft'})


class GymWorkoutPlanLine(models.Model):
    _name = 'gym.workout.plan.line'
    _description = 'Workout Plan Line'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    workout_plan_id = fields.Many2one(
        'gym.workout.plan',
        string='Workout Plan',
        required=True,
        ondelete='cascade',
    )
    exercise_id = fields.Many2one(
        'gym.exercise',
        string='Exercise',
        required=True,
    )
    workout_day_ids = fields.Many2many(
        'gym.workout.day',
        'gym_workout_line_day_rel',
        'line_id',
        'day_id',
        string='Days',
    )
    sets = fields.Integer(string='Sets', default=3)
    reps = fields.Integer(string='Reps', default=10)
    duration = fields.Float(
        string='Duration (min)',
        related='exercise_id.duration',
        store=True,
    )
    calories = fields.Float(
        string='Calories Burned',
        related='exercise_id.calories_burned',
        store=True,
    )
    notes = fields.Char(string='Notes')
