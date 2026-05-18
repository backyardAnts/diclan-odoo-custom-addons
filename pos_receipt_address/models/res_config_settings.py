from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    lbp_usd_rate = fields.Float(
        related="pos_config_id.lbp_usd_rate",
        readonly=False,
        string="LBP / USD Rate",
        help="Display-only USD conversion rate used on printed POS receipts.",
    )
