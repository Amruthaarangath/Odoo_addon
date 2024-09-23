# -*- coding: utf-8 -*-
{
    'name': 'OWL Basics',
    'version': "17.0.1.0.0",
    'depends': ['base','sale'],
    'data': [
        'views/dashboard_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            '/owl_basics/static/src/js/**',
            '/owl_basics/static/src/xml/client_action.xml'
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}