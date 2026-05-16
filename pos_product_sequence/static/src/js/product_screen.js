/** @odoo-module **/



const ProductsWidget = require("point_of_sale.ProductsWidget");
const Registries = require("point_of_sale.Registries");

function sortProducts(products) {
    return [...products].sort((a, b) => {
        const seqA = a.x_pos_sequence ?? 999999;
        const seqB = b.x_pos_sequence ?? 999999;

        if (seqA !== seqB) {
            return seqA - seqB;
        }

        return (a.display_name || "").localeCompare(b.display_name || "");
    });
}

const PosProductSequenceProductsWidget = (ProductsWidget) =>
    class extends ProductsWidget {
        get productsToDisplay() {
            const products = super.productsToDisplay || [];
            const sorted = sortProducts(products);



            return sorted;
        }
    };

Registries.Component.extend(ProductsWidget, PosProductSequenceProductsWidget);