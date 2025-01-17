# -*- coding: utf-8 -*-
{
    'name': "custom_sale_report",

    'summary': """
        Testing report""",

    'description': """
       Testing report
    """,

    'author': "OutsourceArg",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale'],
    'data':['data/sale_report_actions.xml']

}