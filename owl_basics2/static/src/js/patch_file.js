///** @odoo-module **/
//import { patch } from "@web/core/utils/patch";
//import { useRef,useState,useEffect } from "@odoo/owl";
//import {ChildSaleDashboard} from "./child_action";
//import { useService } from "@web/core/utils/hooks";
//
//
//patch(ChildSaleDashboard.prototype,{
//    setup(){
//        super.setup()
//        this.InputRef = useRef("inputbox");
//        this.state = useState({ value: 0 });
//        this.orm = useService("orm");
//        this.action = useService("action");
//
//
//        useEffect(
//            () => {
//            console.log("useEffect")
//            },
//            () => [this.state.value]
//        );
//
//    },
//    async onClickRefresh(){
//        this.InputRef.el.value = "AMRUTHA"
//        console.log(this.InputRef,"aarrr")
//        this.state.value = this.state.value + 1
//        console.log(this.state.value,"aaa")
////        this.orm.search("sale.order")
//
////        const modelId = await this.orm.call("sale.order","sale_order",[[]]);
////        const modelId = await this.orm.searchRead("sale.order",[],['partner_id'],{limit:10});
////        console.log(modelId,"modelid")
//        const modelId = await this.orm.search("sale.order",[],{limit:10});
//        console.log(modelId,"modelid")
//        console.log(modelId,"modelid")
//
//        this.action.doAction({
//            type: 'ir.actions.act_window',
//            target: 'New',
//            res_model: 'sale.order',
//            views: [[false, 'form']],
//        });
//
//
//    }
//})
/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { ListRenderer } from "@web/views/list/list_renderer";
patch(ListRenderer.prototype, "my_list_view_patch", {
 // Define the patched method here
 setup() {
   console.log("List view started!");
   this._super.apply(this, arguments);

   // Call the new method
//    this.myNewMethod();
 },

 // Define a new method
 _onClick() {
   window.alert("helooooo");
 },
});