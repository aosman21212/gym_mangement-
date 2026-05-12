# -*- coding: utf-8 -*-
from odoo import models, fields


class GymTrainerSkill(models.Model):
    _name = 'gym.trainer.skill'
    _description = 'Trainer Skill'
    _order = 'name'

    name = fields.Char(string='Skill Name', required=True)
    description = fields.Text(string='Description')

    _constraints = [
        models.Constraint('unique(name)', 'Skill name must be unique!'),
    ]


class GymBodyPart(models.Model):
    _name = 'gym.body.part'
    _description = 'Body Part'
    _order = 'name'

    name = fields.Char(string='Body Part', required=True)
    description = fields.Text(string='Description')

    _constraints = [
        models.Constraint('unique(name)', 'Body part name must be unique!'),
    ]


class GymWorkoutDay(models.Model):
    _name = 'gym.workout.day'
    _description = 'Workout Day'
    _order = 'sequence, name'

    name = fields.Char(string='Day Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)

    _constraints = [
        models.Constraint('unique(name)', 'Workout day name must be unique!'),
    ]


class GymWorkoutCategory(models.Model):
    _name = 'gym.workout.category'
    _description = 'Workout Category'
    _order = 'name'

    name = fields.Char(string='Category Name', required=True)
    description = fields.Text(string='Description')

    _constraints = [
        models.Constraint('unique(name)', 'Workout category name must be unique!'),
    ]


class GymExerciseType(models.Model):
    _name = 'gym.exercise.type'
    _description = 'Exercise Type'
    _order = 'name'

    name = fields.Char(string='Exercise Type', required=True)
    description = fields.Text(string='Description')

    _constraints = [
        models.Constraint('unique(name)', 'Exercise type name must be unique!'),
    ]


class GymDietInterval(models.Model):
    _name = 'gym.diet.interval'
    _description = 'Diet Interval'
    _order = 'name'

    name = fields.Char(string='Interval Name', required=True)
    description = fields.Text(string='Description')

    _constraints = [
        models.Constraint('unique(name)', 'Diet interval name must be unique!'),
    ]


class GymEquipment(models.Model):
    _name = 'gym.equipment'
    _description = 'Gym Equipment'
    _order = 'name'

    name = fields.Char(string='Equipment Name', required=True)
    description = fields.Text(string='Description')

    _constraints = [
        models.Constraint('unique(name)', 'Equipment name must be unique!'),
    ]


class GymFoodItem(models.Model):
    _name = 'gym.food.item'
    _description = 'Food Item'
    _order = 'name'

    name = fields.Char(string='Food Item', required=True)
    calories = fields.Float(string='Calories (per 100g)', default=0.0)
    protein = fields.Float(string='Protein (g per 100g)', default=0.0)
    carbs = fields.Float(string='Carbohydrates (g per 100g)', default=0.0)
    fat = fields.Float(string='Fat (g per 100g)', default=0.0)
    description = fields.Text(string='Description')

    _constraints = [
        models.Constraint('unique(name)', 'Food item name must be unique!'),
    ]
