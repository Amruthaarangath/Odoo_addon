# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def sale_order(self):
        order = self.env['sale.order'].search_read([],limit = 10)
        print(order)
        return order