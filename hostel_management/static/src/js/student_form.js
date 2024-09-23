/** @odoo-module **/

import { Component } from "@odoo/owl";
import { sortBy } from "../utils/arrays";
import { ErrorHandler } from "../utils/components";

export class OverlayContainer extends Component {
    static template = "web.OverlayContainer";
    static components = { ErrorHandler };
    static props = { overlays: Object };

    publicWidget.registry.CountryData = publicWidget.Widget.extend({
        selector: '.container',
        events: {
//        'change select[name="country_id"]': '_onCountryChange',
        'change #country_id': '_onCountryChange',
    },
    init: function (parent, options) {
        this._super.apply(this, arguments);
        this.rpc = this.bindService("rpc");
    },
    _onCountryChange: async function () {
        var self = this
        var country_id = this.$el.find('#country_id').val();
        await jsonrpc("/filtered_states", {
            country_id: country_id,

    }).then(function (records) {
        self.$el.find('#state_id').empty();
        self.$el.find('#state_id').prepend('<option value="">Select State</option>');
        records.forEach(function (record) {
        self.$('#state_id').append('<option value="${record.id}">${record.name}</option>');
            });
        });
    }
})