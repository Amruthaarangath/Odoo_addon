{
    'name': "Remove Order Lines",
    'version': '1.0',
    'summary': 'Remove Order Lines POS',
    'description': "Remove Order Lines POS",
    'depends': ['base','point_of_sale'],

'assets': {
        'point_of_sale._assets_pos': [
            'pos_remove_order_lines/static/src/js/remove_order_line.js',
            'pos_remove_order_lines/static/src/js/clear_all_lines.js',
            'pos_remove_order_lines/static/src/xml/remove_line_button.xml',
            'pos_remove_order_lines/static/src/xml/clear_all_button.xml'
        ],
    },
    'license': 'LGPL-3',
}
