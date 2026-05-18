from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    lbp_usd_rate = fields.Float(
        string="LBP / USD Rate",
        default=89000.0,
        help="Display-only USD conversion rate used on printed POS receipts.",
    )
