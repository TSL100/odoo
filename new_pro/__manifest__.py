# -*- coding: utf-8 -*-
{
    'name': " Inherit Invoicing",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,
    'author': "My Company",
    'category': 'uncategory',
    'version': '0.1',
    'depends': ['account','stock'],
    'data': [
        # 'views/sale_inherit.xml',
        'views/Receipts_inherit.xml',
             ],
    'demo': [],
}
