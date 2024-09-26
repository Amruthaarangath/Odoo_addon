{
    'name': "Product Brand",
    'version': '1.0',
    'summary': 'Product Brand',
    'description': "POS Product Brand",
    'depends': ['base', 'product','point_of_sale'],

'data': [
            'views/product_brand_view.xml'
    ],
'assets': {
        'point_of_sale._assets_pos': [
            'pos_product_brand/static/src/js/pos_brand.js',
            'pos_product_brand/static/src/xml/pos_brand.xml'
        ],
    },
    'license': 'LGPL-3',
}
