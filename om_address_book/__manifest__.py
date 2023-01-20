
{
    'name': 'Address Book',
    'version': '1.0.0',
    'category': 'Management',
    'author':'Yadhu',
    'summary': 'Information Storage System',
    'description': """
This module contains features to manage the information of your loved ones....
    """,
    'depends': ['mail', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/contact_tags.xml',
        'data/contact.tags.csv',
        'data/sequence.xml',
        'wizard/cancel_call_view.xml',
        'views/menu.xml',
        'views/details_view.xml',
        'views/male_contacts.xml',
        'views/female_contacts.xml',
        'views/call_details.xml',
        'views/tag_view.xml',
    ],
    'demo': [ ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 0,
    'license': 'LGPL-3',
}