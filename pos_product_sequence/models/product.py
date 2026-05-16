from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    x_pos_sequence = fields.Integer(
        string="POS Sequence",
        default=10,
        help="Controls the product order in POS. Lower numbers appear first.",
    )


class ProductProduct(models.Model):
    _inherit = "product.product"

    x_pos_sequence = fields.Integer(
        related="product_tmpl_id.x_pos_sequence",
        readonly=False,
        store=True,
    )
