/** @odoo-module */

import { ProductCard } from "@point_of_sale/app/generic_components/product_card/product_card";
import { patch } from "@web/core/utils/patch";
import { CustomButtonPopup } from "./custom_button_popup";
import { _t } from "@web/core/l10n/translation";

patch(ProductCard.prototype, {
    async videoClick(){
        const video = await this.props.video_file;
        this.env.services.popup.add(CustomButtonPopup, {
                    title: _t(this.props.name),
                    body: video
                });
    }
});
