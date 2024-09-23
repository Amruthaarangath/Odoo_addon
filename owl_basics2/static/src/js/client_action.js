/** @odoo-module **/
import {registry} from "@web/core/registry";
import { Component } from "@odoo/owl";
import {ChildSaleDashboard} from "./child_action";

class SaleDashboard extends Component{
    static components = {
        ChildSaleDashboard,
    };
    setup() {
        console.log('qqqq',this)
    }
}
SaleDashboard.template = "saleDashboard"
registry.category("actions").add("sale_dashboard", SaleDashboard);