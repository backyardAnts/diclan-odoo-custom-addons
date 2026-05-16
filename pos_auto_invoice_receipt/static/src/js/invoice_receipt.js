odoo.define("pos_auto_invoice_receipt.invoice_receipt", function (require) {
    "use strict";

    const { PosGlobalState, Order } = require("point_of_sale.models");
    const Registries = require("point_of_sale.Registries");
    const rpc = require("web.rpc");

    const PosAutoInvoiceGlobalState = (PosGlobalState) =>
        class extends PosGlobalState {
            async push_single_order(order, opts) {
                const result = await super.push_single_order(...arguments);

                try {
                    let posOrderId = false;

                    if (order.server_id) {
                        posOrderId = order.server_id;
                    } else if (Array.isArray(result) && result.length) {
                        if (typeof result[0] === "object") {
                            posOrderId = result[0].id;
                        } else {
                            posOrderId = result[0];
                        }
                    } else if (result && typeof result === "object") {
                        posOrderId = result.id;
                    } else {
                        posOrderId = result;
                    }

                    if (posOrderId) {
                        const invoiceNumber = await rpc.query({
                            model: "pos.order",
                            method: "get_invoice_number_for_receipt",
                            args: [posOrderId],
                        });

                        order.invoice_number = invoiceNumber || "";
                    }
                } catch (error) {
                    console.warn("Could not fetch invoice number for receipt:", error);
                    order.invoice_number = "";
                }

                return result;
            }
        };

    Registries.Model.extend(PosGlobalState, PosAutoInvoiceGlobalState);

    const PosAutoInvoiceOrder = (Order) =>
        class extends Order {
            constructor(obj, options) {
                super(...arguments);
                this.invoice_number = this.invoice_number || "";
            }

            init_from_JSON(json) {
                super.init_from_JSON(...arguments);
                this.invoice_number = json.invoice_number || "";
            }

            export_as_JSON() {
                const json = super.export_as_JSON(...arguments);
                json.invoice_number = this.invoice_number || "";
                return json;
            }

            export_for_printing() {
                const receipt = super.export_for_printing(...arguments);
                receipt.invoice_number = this.invoice_number || "";
                return receipt;
            }
        };

    Registries.Model.extend(Order, PosAutoInvoiceOrder);
});