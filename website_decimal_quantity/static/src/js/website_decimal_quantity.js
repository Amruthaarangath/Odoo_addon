/** @odoo-module **/

//import publicWidget from "@web/legacy/js/public/public_widget";
//import { jsonrpc } from "@web/core/network/rpc_service";
//
//console.log("aaaaa");
//
//publicWidget.registry.AddQuantity = publicWidget.Widget.include({
//    selector: '.oe_website_sale',
//    events: {
//        click: "_onChangeAddQuantity",
//
//
//    },
////    _submitForm: function () {
////        const params = this.rootProduct;
////
////        params.add_qty = params.quantity;
////        return this.addToCart(params);
////        console.log("aammmrrr".params)
////    },
//    _onChangeAddQuantity: function () {
////        const params = this.rootProduct;
////        let a = .1
////        quantity: parseFloat($form.find('input[name="add_qty"]').val() || 1)
////        quantity: $('#product_quantity').val(parseInt($('#product_quantity').val()) + 2);
////        params.add_qty = params.quantity;
//        console.log("aammmrrr")
//    },
//});
odoo.define('website_decimal_quantity.DecimalQuantity', function (require) {
    'use strict';
    var core = require('web.core');
    var MyClass = require('some.module.MyClass');
    var _t = core._t;
    MyClass.extend({
        myMethod: function () {
            // Calling parent class method
            this._super();
            // Adding new functionality to the parent method
            // ...
        },
    });
    return MyClass;
});
//odoo.define('website_decimal_quantity.DecimalQuantity', function (require) {
//"use strict";
//
//var FieldManagerMixin = require('web.models');
//
//var LineRenderer = Widget.extend(FieldManagerMixin, {
//    _onChangeAddQuantity: function () {
//        console.log("werty")
//        // Copy whole code of _renderCreate method and Paste here. Just change your domain for account_id.
//        // Note: Don't call super
//    },
//});
//
//return { LineRenderer: LineRenderer, };
//
//});