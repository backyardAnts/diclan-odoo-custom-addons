{
    "name": "POS Product Sequence",
    "version": "16.0.1.0.0",
    "category": "Point of Sale",
    "summary": "Control product order inside the POS product screen",
    "depends": [
        "point_of_sale",
        "product",
    ],
    "data": [
        "views/product_template_views.xml",
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_product_sequence/static/src/js/product_screen.js",
        ],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
