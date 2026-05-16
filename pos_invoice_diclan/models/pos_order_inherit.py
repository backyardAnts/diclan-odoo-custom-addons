from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = "pos.order"

    customer_invoice_id = fields.Many2one(
        "account.move",
        string="Customer Invoice",
        related="account_move",
        readonly=True,
        store=True,
        copy=False,
    )

    def write(self, vals):
        previously_paid = {
            rec.id: rec.state in ("paid", "invoiced", "done")
            for rec in self
        }

        res = super().write(vals)

        if "state" in vals:
            for rec in self:
                now_paid = rec.state in ("paid", "invoiced", "done")
                became_paid = now_paid and not previously_paid.get(rec.id)

                if not became_paid:
                    continue

                existing_log = self.env["pos.invoice.log"].sudo().search(
                    [("pos_order_id", "=", rec.id)],
                    limit=1,
                )
                if existing_log:
                    continue

                try:
                    line_cmds = []
                    for line in rec.lines:
                        line_cmds.append((0, 0, {
                            "product_id": line.product_id.id,
                            "qty": line.qty,
                            "price_unit": line.price_unit,
                            "discount": line.discount or 0.0,
                            "tax_ids": [(6, 0, line.tax_ids_after_fiscal_position.ids)],
                        }))

                    self.env["pos.invoice.log"].sudo().create({
                        "name": rec.name,
                        "partner_id": rec.partner_id.id or False,
                        "pos_order_id": rec.id,
                        "session_id": rec.session_id.id or False,
                        "user_id": rec.user_id.id or False,
                        "currency_id": (
                            rec.pricelist_id.currency_id.id
                            if rec.pricelist_id
                            else self.env.company.currency_id.id
                        ),
                        "line_ids": line_cmds,
                    })
                except Exception:
                    _logger.exception(
                        "Creating POS invoice log failed for POS order %s",
                        rec.name,
                    )

        return res
