from odoo import api, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    def _get_walkin_customer(self, config):
        partner = config.default_receipt_partner_id

        if partner:
            return partner

        partner = (
            self.env["res.partner"]
            .sudo()
            .search([("name", "=", "Walk-in Customer")], limit=1)
        )

        if not partner:
            partner = (
                self.env["res.partner"]
                .sudo()
                .create(
                    {
                        "name": "Walk-in Customer",
                        "customer_rank": 1,
                    }
                )
            )

        return partner

    def _process_order(self, order, draft, existing_order):
        data = order.get("data", {})

        session_id = data.get("pos_session_id")
        if session_id:
            session = self.env["pos.session"].sudo().browse(session_id)
            config = session.config_id

            if config.force_invoice_on_receipt:
                if not data.get("partner_id"):
                    partner = self._get_walkin_customer(config)
                    data["partner_id"] = partner.id

                data["to_invoice"] = True

        return super()._process_order(order, draft, existing_order)

    def _generate_pos_order_invoice(self):
        orders_to_invoice = self.filtered(lambda order: not order.account_move)

        if not orders_to_invoice:
            return False

        return super(PosOrder, orders_to_invoice)._generate_pos_order_invoice()

    @api.model
    def get_invoice_number_for_receipt(self, pos_order_id):
        order = self.sudo().browse(int(pos_order_id))

        if not order.exists():
            return ""

        if not order.account_move:
            return ""

        if order.account_move.name and order.account_move.name != "/":
            return order.account_move.name

        return ""
