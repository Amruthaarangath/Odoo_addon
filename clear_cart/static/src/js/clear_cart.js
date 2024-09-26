/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

console.log("aaaaa");

publicWidget.registry.ClearCart = publicWidget.Widget.extend({
    selector: '#clear_cart',
    events: {
        click: "_onClickClearCart"
    },

    _onClickClearCart: function () {
        jsonrpc("/shop/clear_cart", {}).then(function(){
            location.reload();
//            console.log(window.location.reload(),"hhh")
        });
        return false;
    },
});
