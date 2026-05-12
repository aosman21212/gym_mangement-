# -*- coding: utf-8 -*-
from odoo import models, fields, api


class GymBmiBmr(models.Model):
    _name = 'gym.bmi.bmr'
    _description = 'BMI & BMR Record'
    _order = 'date desc'

    member_id = fields.Many2one(
        'gym.member',
        string='Member',
        required=True,
        ondelete='cascade',
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.today,
    )
    height = fields.Float(string='Height (cm)', required=True)
    weight = fields.Float(string='Weight (kg)', required=True)
    age = fields.Integer(string='Age', required=True)
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        string='Gender',
        required=True,
    )
    bmi = fields.Float(
        string='BMI',
        compute='_compute_bmi_bmr',
        store=True,
        digits=(6, 2),
    )
    bmi_category = fields.Char(
        string='BMI Category',
        compute='_compute_bmi_bmr',
        store=True,
    )
    bmr = fields.Float(
        string='BMR (kcal/day)',
        compute='_compute_bmi_bmr',
        store=True,
        digits=(10, 2),
    )
    notes = fields.Text(string='Notes')

    @api.depends('height', 'weight', 'age', 'gender')
    def _compute_bmi_bmr(self):
        for rec in self:
            if rec.height and rec.weight:
                height_m = rec.height / 100.0
                bmi = rec.weight / (height_m ** 2)
                rec.bmi = round(bmi, 2)

                if bmi < 18.5:
                    rec.bmi_category = 'Underweight'
                elif bmi < 25.0:
                    rec.bmi_category = 'Normal'
                elif bmi < 30.0:
                    rec.bmi_category = 'Overweight'
                else:
                    rec.bmi_category = 'Obese'
            else:
                rec.bmi = 0.0
                rec.bmi_category = ''

            # Mifflin-St Jeor Formula
            if rec.height and rec.weight and rec.age:
                base = 10 * rec.weight + 6.25 * rec.height - 5 * rec.age
                if rec.gender == 'male':
                    rec.bmr = round(base + 5, 2)
                elif rec.gender == 'female':
                    rec.bmr = round(base - 161, 2)
                else:
                    rec.bmr = round(base, 2)
            else:
                rec.bmr = 0.0
