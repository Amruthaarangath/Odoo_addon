# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.product'

    average_cost = fields.Monetary(string="Average Cost", compute='_compute_average_cost', store=True,
                               help="Total average cost of the product from it's previous purchases")

    @api.depends('purchased_product_qty')
    def _compute_average_cost(self):
        for record in self:
            total_orders = record.env['purchase.order.line'].search([("product_id", "=", record.id)])
            total_quantity = sum(total_orders.mapped('product_qty'))
            total_cost = sum(total_orders.mapped('price_unit'))

            if total_quantity > 0:
                average_cost = total_cost / total_quantity
                record.average_cost = average_cost
            else:
                record.average_cost = 0
