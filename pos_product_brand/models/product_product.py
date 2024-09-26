# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.product'

    brand = fields.Char(string = "Brand", help="Enter the brand of this product")
