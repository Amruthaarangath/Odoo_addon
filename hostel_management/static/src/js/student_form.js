/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

    publicWidget.registry.CountryData = publicWidget.Widget.extend({
        selector: '.student_registration',
        events: {
        'change #country_id': '_onCountryChange',
    },
    _onCountryChange: async function () {
        var self = this
        console.log('self')
        var country_id = this.$el.find('#country_id').val();

        await jsonrpc("/filtered_states", {
            country_id: country_id,

    }).then(function (records) {
        self.$el.find('#state_id').empty();
        self.$el.find('#state_id').prepend('<option value="">Select State</option>');
        records.forEach(function (record) {
        self.$('#state_id').append(`<option value="${record.id}">${record.name}</option>`);
            });
        });
    }
})