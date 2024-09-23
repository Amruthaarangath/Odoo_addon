# -*- coding: utf-8 -*-
{
    'name': "Hostel Management",
    'version': '1.2',
    'summary': 'Hostel management',
    'application': True,
    'description': "Hostel management",
    'depends': ['mail', 'account', 'product', 'base_automation','website'],

    'data': [
        'data/room_number_sequence.xml',
        'data/student_id_sequence.xml',
        'data/hostel_facilities.xml',
        'data/mail_scheduled_action.xml',
        'data/rental_product.xml',
        'data/mail_template.xml',
        'data/user_automation.xml',
        'security/user_group.xml',
        'security/hostel_security.xml',
        'security/ir.model.access.csv',
        'views/hostel_room_management_view.xml',
        'views/student_view.xml',
        'views/cleaning_service_view.xml',
        'views/facilities_view.xml',
        'views/leave_view.xml',
        'views/account_move_view.xml',
        'views/website_menu_view.xml',
        'views/website_form_template.xml',
        'views/submit_template.xml',
        'wizard/student_report_view.xml',
        'wizard/leave_report_view.xml',
        'views/reception_view.xml',
        'report/student_report.xml',
        'report/leave_report.xml',
        'report/ir_actions_report.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'hostel_management/static/src/js/action_manager.js'
        ],
        'web.assets_frontend': [
            'hostel_management/static/src/js/student_form.js'
        ],
    },
        'license': 'LGPL-3',
}
