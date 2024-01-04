# -*- coding: utf-8 -*-
{
    'name': "order",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,
    'author': "My Company",
    'category': 'uncategory',
    'version': '0.1',
    'depends': ['base','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/view_active.xml',
        'views/loures.xml',
        'views/extends_view.xml',
             ],
    'demo': [],
}
