# -*- coding: utf-8 -*-
{
    'name': 'OWL Basics',
    'version': "17.0.1.0.0",
    'depends': ['base','sale','sale_management'],
    'data': [
        'views/dashboard_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            '/owl_basics2/static/src/js/client_action.js',
            '/owl_basics2/static/src/js/child_action.js',
            '/owl_basics2/static/src/js/patch_file.js',
            '/owl_basics2/static/src/xml/client_action.xml'
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}