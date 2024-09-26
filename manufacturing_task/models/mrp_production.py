# -*- coding: utf-8 -*-

from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    component_cost = fields.Char(string="Total Cost", compute='_onchange_total_component_cost', help="Total cost of components used")
    extra_cost = fields.One2many('mrp.test', 'mrp', string='Extra cost')

    @api.onchange("move_raw_ids.product_id")
    def _onchange_total_component_cost(self):
        """total component cost"""
        for record in self.move_raw_ids:
            cost = record.product_id
            rec = sum(line.lst_price for line in cost)
            self.component_cost = rec

    # def _action_create_bill(self):
    #     for record in self.move_raw_ids:
    #         if record.picked == True:
    #             rec = record.product_id.lst_price + self.extra_cost
