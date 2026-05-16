from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    force_invoice_on_receipt = fields.Boolean(
        string="Force Invoice on POS Receipt",
        default=True,
    )

    default_receipt_partner_id = fields.Many2one(
        "res.partner",
        string="Default Receipt Customer",
        help="Used automatically when no customer is selected in POS.",
    )
