/** @odoo-module */
import { _t } from "@web/core/l10n/translation";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";
import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";
import { useService } from "@web/core/utils/hooks";

export class DeleteOrderLines extends Component {
    static template = "ClearAllButton";
    setup(){
        this.pos = usePos();
        this.popup = useService("popup");
        this.notification = useService("pos_notification");
    }
    async onClick(){
        var order = this.pos.get_order();
        var lines = order.get_orderlines();
        if (lines.length){
            await this.popup.add(ConfirmPopup, {
                title: "clear orders",
                body:"Do you want to clear all the orders?"
            }).then(({confirmed}) => {
                if (confirmed == true){
                    lines.filter(line => line.get_product())
                        .forEach(line => order.removeOrderline(line));
                }else{
                    return false;
                }
            })
        }else{
            this.notification.add(_t("No items to remove."),3000);
            }
    }
}
ProductScreen.addControlButton({
    component : DeleteOrderLines,
});
