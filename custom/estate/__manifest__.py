# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'estate',
    'depends': ['base',],
    'application': True,
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/estate_type_views.xml',
        'views/estate_tag_views.xml',
        'views/estate_offer_views.xml'

    ],
}
