{
    'name': "Multisafepay Payment",
    'version': '1.0',
    'summary': 'Multisafepay Payment',
    'description': "Multisafepay Payment",
    'depends': ['base', 'payment'],

    'data': [
                'views/payment_multisafepay_templates.xml',
                'views/multisafepay_api_view.xml',
                'data/payment_provider_data.xml',
                # 'data/payment_method_data.xml'
        ],

    'license': 'LGPL-3',
}
