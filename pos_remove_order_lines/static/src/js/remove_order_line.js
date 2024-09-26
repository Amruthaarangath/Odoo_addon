/** @odoo-module */

import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";

patch(Orderline.prototype, {
    removeLine() {
        var order = this.env.services.pos.get_order();
        const orderline = this.orderlines
        if(order.full_product_name == this.props.productName){
        return order.removeOrderline(orderline);
        }
//        console.log(orderline,"aa")
//        return removeOrderline(order.full_product_name == this.props.productName);
//
//
////        const order = this.env.services.pos.get_order();
//        const orderline = order.orderlines.find((line) => line.full_product_name == this.props.line.productName);
//        return order.removeOrderline(orderline);
    }
});
