/** @odoo-module */

import { Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

console.log("rthjm")
patch(Orderline.prototype, {
    getDisplayData() {
        return {
            ...super.getDisplayData(),
            brand: this.get_product().brand,
        };
    },
});
