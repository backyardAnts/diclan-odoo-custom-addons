{
    "name": "POS Auto Invoice and Invoice Number Receipt",
    "version": "16.0.1.0.0",
    "summary": "Automatically invoice POS orders and print invoice number on receipt",
    "category": "Point of Sale",
    "depends": ["point_of_sale", "account", "pos_receipt_address"],
    "data": [
        "views/pos_config_views.xml",
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_auto_invoice_receipt/static/src/js/invoice_receipt.js",
            "pos_auto_invoice_receipt/static/src/xml/order_receipt.xml",
        ],
    },
    "installable": True,
    "application": False,
}
