from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()

        if "x_pos_sequence" not in result["search_params"]["fields"]:
            result["search_params"]["fields"].append("x_pos_sequence")

        result["search_params"]["order"] = "x_pos_sequence asc, display_name asc"

        return result
