# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'category': 'Management',
    'author': 'Yadhu',
    'summary': 'Hospital Management System',
    'description': """
This module contains features to manage an entire hospital
    """,
    'depends': ['mail', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'data/patient.tags.csv',
        'data/sequence.xml',
        'data/sequence_appointment.xml',
        'views/menu.xml',
        'wizard/cancel_appointment_view.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/male_patient_view.xml',
        'views/appointment_view.xml',
        'views/patient_tags.xml',
        'views/res_config_settings_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': -100,
    'license': 'LGPL-3',
}
