{
    'name': "POS Product Video",
    'version': '1.0',
    'summary': 'POS Product Video',
    'description': "POS Product Video",
    'depends': ['base', 'product','point_of_sale'],

'data': [
            'views/product_video_view.xml'
    ],
'assets': {
        'point_of_sale._assets_pos': [
            'pos_product_video/static/src/js/custom_button_popup.js',
            'pos_product_video/static/src/xml/custom_button_popup.xml',
            'pos_product_video/static/src/js/pos_product_button.js',
            'pos_product_video/static/src/js/video_props.js',
            'pos_product_video/static/src/xml/product_video.xml',
        ],
    },
    'license': 'LGPL-3',
}
