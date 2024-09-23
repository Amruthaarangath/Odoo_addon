/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { useRef } from "@odoo/owl";
import {ChildSaleDashboard} from "./child_action";

patch(ChildSaleDashboard.prototype,{
    setup(){
        super.setup()
        this.InputRef = useRef("inputbox");
    },
    onClickRefresh(){
        this.InputRef.el.value = " "
    }
})