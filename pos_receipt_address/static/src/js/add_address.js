odoo.define('pos_receipt_address.models', function(require) {
    'use strict';

    var { Order } = require('point_of_sale.models');
    var Registries = require('point_of_sale.Registries');

    const DEFAULT_USD_RATE = 89000;

    function getReceiptUsdRate(pos) {
        const configuredRate = pos && pos.config ? Number(pos.config.lbp_usd_rate) : 0;
        return configuredRate > 0 ? configuredRate : DEFAULT_USD_RATE;
    }

    const CustomOrder = (Order) => class CustomOrder extends Order {
        export_for_printing() {
            var result = super.export_for_printing(...arguments);
            result.client = this.get_partner();

            const total_lbp = result.total_with_tax || 0;
            const usdRate = getReceiptUsdRate(this.pos);
            result.total_usd = total_lbp / usdRate;
            return result;
        }
    };

Registries.Model.extend(Order, CustomOrder);
});
