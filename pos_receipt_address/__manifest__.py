{
    "name": "POS Receipt Address",
    "version": "16.0.1.0.0",
    "category": "Point of Sale",
    "summary": "Show company address and VAT on POS receipt",
    "depends": ["point_of_sale"],
    "data": [
        "views/pos_config_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_receipt_address/static/src/xml/receipt.xml",
            "pos_receipt_address/static/src/js/add_address.js",
        ],
    },
    "installable": True,
    "application": False,
}
