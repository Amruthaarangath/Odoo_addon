{
    'name': "Sale Import lines",
    'version': '1.0',
    'summary': 'Sale Import lines',
    'description': "Sale Import lines",
    'depends': ['base', 'sale'],

    'data': [
              'views/sale_xls_wizard_view.xml',
              'views/import_lines_form_view.xml',
              'security/ir.model.access.csv',

    ],
    'license': 'LGPL-3',
}
