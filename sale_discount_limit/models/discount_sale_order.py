# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import date
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    @api.constrains('discount')
    def _check_monthly_discount(self):
        print('hi')
        today = date.today()
        month_start = date.today().replace(day=1),
        order_lines = sum(self.search([("order_id.partner_id", "=", self.order_id.partner_id.id),
                                      ("order_id.date_order", "<=", month_start)
                                      and ("order_id.date_order", ">=", today)]).mapped('discount'))
        discount_limit = float(self.env['ir.config_parameter'].sudo()
                               .get_param('sale_discount_limit.discount_limit'))

        total_discount = order_lines + self.discount

        if total_discount > discount_limit:
            raise ValidationError(_("Your monthly limit is exceeded"))
