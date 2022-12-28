
{
    'name': 'Address Book',
    'version': '1.0.0',
    'category': 'Management',
    'author':'Yadhu',
    'summary': 'Information Storage System',
    'description': """
This module contains features to manage the information of your loved ones....
    """,
    'depends': [ ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/details_view.xml',
    ],
    'demo': [ ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 0,
    'license': 'LGPL-3',
}