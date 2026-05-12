# -*- coding: utf-8 -*-
from odoo import models, fields


class GymMembershipType(models.Model):
    _name = 'gym.membership.type'
    _description = 'Membership Type'
    _order = 'name'

    name = fields.Char(string='Membership Type', required=True)
    duration = fields.Integer(
        string='Duration (Days)',
        required=True,
        default=30,
        help='Duration of this membership in days.',
    )
    price = fields.Float(string='Price', required=True, default=0.0)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='Color Index', default=0)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='company_id.currency_id',
        readonly=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    _constraints = [
        models.Constraint('unique(name)', 'Membership type name must be unique!'),
        models.Constraint('CHECK(duration > 0)', 'Duration must be positive!'),
        models.Constraint('CHECK(price >= 0)', 'Price cannot be negative!'),
    ]
