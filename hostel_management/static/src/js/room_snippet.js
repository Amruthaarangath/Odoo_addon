/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";
export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
publicWidget.registry.DynamicSnippet = publicWidget.Widget.extend({
   selector: '.room_snippet',
   willStart: async function () {
        let data = await jsonrpc('/room', {});
        this.data = data;
   },
   start: function () {
        const refEl = this.$el.find("#room_snippet");
        const chunkData = _chunk(this.data, 4);
        chunkData[0].is_active = true
        var unique_id = "unique_id" + Math.random().toString(16).slice(2)
        console.log(unique_id)
        refEl.html(renderToElement("hostel_management.room_category_wise", {
                chunkData,
                unique_id
            })
        );
    },
});
export default publicWidget.registry.DynamicSnippet;
