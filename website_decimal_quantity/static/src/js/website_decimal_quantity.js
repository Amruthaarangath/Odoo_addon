/** @odoo-module **/

import { WebsiteSale } from '@website_sale/js/website_sale';
import wSaleUtils from "@website_sale/js/website_sale_utils";
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import VariantMixin from "@website_sale/js/sale_variant_mixin";


WebsiteSale.include({
    events: Object.assign({}, WebsiteSale.prototype.events, {
        'click .oe_website_sale': 'onClickAddCartJSON',
        'change .oe_cart input.js_quantity[data-product-id]': '_onChangeCartQuantity',
        'change .js_main_product [data-attribute_exclusions]': 'onChangeVariant',
        'click input.js_product_change': 'onChangeVariant',
        'change .js_main_product [data-attribute_exclusions]': 'onChangeVariant',
    }),

    onClickAddCartJSON: function (ev, $dom_optional) {
//    const searchDomain = [];
//        let productCategoryId = this.$el.get(0).dataset.productCategoryId;
//        console.log("wwww",$dom_optional)
//        if (productCategoryId && productCategoryId !== 'all') {
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var $input = $link.closest('.input-group').find("input");
        var min = parseFloat($input.data("min") || 0);
        var max = parseFloat($input.data("max") || Infinity);
        var previousQty = parseFloat($input.val() || 0, 10);
        var quantity = (($link.has(".fa-minus").length ? -0.1 : 0.1) + previousQty).toFixed(1);
        var newQty = (quantity > min ? (quantity < max ? quantity : max) : min);

        console.log("oooohhho",($input))
        console.log("quantity",ev.js_quantity)
        console.log("previousQty",previousQty)
        console.log("newQty",newQty)
        if (newQty !== previousQty) {
            $input.val(newQty).trigger('change');
        }
        return false;
    },
//    else{
//        ev.preventDefault();
//            var $link = $(ev.currentTarget);
//            var $input = $link.closest('.input-group').find("input");
//            var min = parseFloat($input.data("min") || 0);
//            var max = parseFloat($input.data("max") || Infinity);
//            var previousQty = parseFloat($input.val() || 0, 10);
//            var quantity = (($link.has(".fa-minus").length ? -1 : 1) + previousQty).toFixed(1);
//            var newQty = (quantity > min ? (quantity < max ? quantity : max) : min);
//
//            console.log("oooohhho",($input))
//            console.log("quantity",ev.js_quantity)
//            console.log("previousQty",previousQty)
//            console.log("newQty",newQty)
//            console.log("ooo",newQty * amount)
//            if (newQty !== previousQty) {
//                $input.val(newQty).trigger('change');
//            }
//            return false;
//        }
        _changeCartQuantity: function ($input, value, $dom_optional, line_id, productIDs) {
        $($dom_optional).toArray().forEach((elem) => {
            $(elem).find('.js_quantity').text(value);
            productIDs.push($(elem).find('span[data-product-id]').data('product-id'));
        });
        $input.data('update_change', true);

        rpc("/shop/cart/update_json", {
            line_id: line_id,
            product_id: parseFloat($input.data('product-id'), 10),
            set_qty: value,
            display: true,
        }).then((data) => {
            $input.data('update_change', false);
            var check_value = parseFloat($input.val() || 0, 10);
//            console.log("yyy",$input.data)
              console.log("yyyppp",productIDs)
            if (isNaN(check_value)) {
                check_value = 1;
            }
            if (value !== check_value) {
                $input.trigger('change');
                return;
            }
            if (!data.cart_quantity) {
                return window.location = '/shop/cart';
            }
            $input.val(data.quantity);
            $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).text(data.quantity);

            wSaleUtils.updateCartNavBar(data);
            wSaleUtils.showWarning(data.notification_info.warning);
            // Propagating the change to the express checkout forms
            Component.env.bus.trigger('cart_amount_changed', [data.amount, data.minor_amount]);
//            var val = $input.val(data.quantity);
            console.log("amount",)
//            console.log("data.minor_amount",data.minor_amount)
////            console.log("product_category_id",data)
//            console.log("id",data)
        });
    },
    onChangeVariant: function (ev) {
        var $component = $(ev.currentTarget).closest('.js_product');
        $component.find('input').each(function () {
            var $el = $(this);
            $el.attr('checked', $el.is(':checked'));
            console.log("hloo",$el)
        });
        $component.find('select option').each(function () {
            var $el = $(this);
            $el.attr('selected', $el.is(':selected'));
             console.log("hloo2",$el.data('data-oe-id'))
        });

        this._setUrlHash($component);

        return VariantMixin.onChangeVariant.apply(this, arguments);
    },
});
export default WebsiteSale;

