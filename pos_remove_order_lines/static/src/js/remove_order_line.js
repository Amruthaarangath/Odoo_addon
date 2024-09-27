/** @odoo-module */

import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";

patch(Orderline.prototype, {
    removeLine() {

        var order = this.env.services.pos.get_order();
        var orderlines = order.get_orderlines()
        var selected_line = orderlines.find((line) => line.full_product_name == this.props.line.productName)

        return order.removeOrderline(selected_line);
    }
});
