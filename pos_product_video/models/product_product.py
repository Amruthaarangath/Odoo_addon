# -*- coding: utf-8 -*-

from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.product'

    video_file = fields.Char(string = "Video",help= "paste the url of the product video")
