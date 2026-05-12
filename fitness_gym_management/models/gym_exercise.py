# -*- coding: utf-8 -*-
from odoo import models, fields


class GymExercise(models.Model):
    _name = 'gym.exercise'
    _description = 'Gym Exercise'
    _order = 'name'

    name = fields.Char(string='Exercise Name', required=True)
    exercise_type_id = fields.Many2one(
        'gym.exercise.type',
        string='Exercise Type',
        required=True,
    )
    body_part_ids = fields.Many2many(
        'gym.body.part',
        'gym_exercise_body_part_rel',
        'exercise_id',
        'body_part_id',
        string='Target Body Parts',
    )
    duration = fields.Float(string='Duration (minutes)', default=0.0)
    calories_burned = fields.Float(string='Calories Burned', default=0.0)
    benefits = fields.Text(string='Benefits')
    steps = fields.Text(string='Steps / Instructions')
    video_url = fields.Char(string='Video URL')
    equipment_ids = fields.Many2many(
        'gym.equipment',
        'gym_exercise_equipment_rel',
        'exercise_id',
        'equipment_id',
        string='Equipment Required',
    )
    difficulty = fields.Selection(
        [
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        string='Difficulty Level',
        default='beginner',
        required=True,
    )
    image = fields.Binary(string='Image', attachment=True)
    active = fields.Boolean(string='Active', default=True)

    _constraints = [
        models.Constraint('unique(name)', 'Exercise name must be unique!'),
    ]
