# -*- coding: utf-8 -*-
{
    'name': 'Fitness Gym Management',
    'version': '19.0.1.0.0',
    'category': 'Services',
    'summary': 'Comprehensive Gym & Fitness Center Management',
    'description': """
Gym Management System
=====================
A comprehensive module for managing gym operations including:
- Member registration and management
- Membership plans and billing
- Trainer management
- Exercise library
- Workout plan creation
- Diet plan management
- BMI & BMR tracking
- PDF reports for members, workout plans, and diet schedules
- Email notifications for membership renewal
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'mail', 'account'],
    'assets': {
        'web.assets_backend': [
            'fitness_gym_management/static/src/js/gym_dashboard.js',
            'fitness_gym_management/static/src/xml/gym_dashboard.xml',
        ],
    },
    'data': [
        # Security
        'security/gym_security.xml',
        'security/ir.model.access.csv',
        # Data
        'data/gym_email_template.xml',
        # Wizards
        'wizards/gym_membership_wizard_views.xml',
        # Views
        'views/gym_dashboard_views.xml',
        'views/gym_config_views.xml',
        'views/gym_trainer_views.xml',
        'views/gym_member_views.xml',
        'views/gym_membership_views.xml',
        'views/gym_exercise_views.xml',
        'views/gym_workout_plan_views.xml',
        'views/gym_diet_plan_views.xml',
        'views/gym_bmi_bmr_views.xml',
        # Reports
        'report/gym_member_report.xml',
        'report/gym_member_report_template.xml',
        'report/gym_workout_report.xml',
        'report/gym_workout_report_template.xml',
        'report/gym_diet_report.xml',
        'report/gym_diet_report_template.xml',
        # Menu (last so actions are defined)
        'views/gym_menu.xml',
    ],
    'demo': [
        'demo/gym_demo.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
