# -*- coding: utf-8 -*-

from odoo import fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_discount_limit = fields.Boolean(string='Discount limit',
                                       config_parameter='sale_discount_limit.is_discount_limit',
                                       help='Check this field for enabling discount limit')
    discount_limit = fields.Float(string='Limit amount',
                                  config_parameter='sale_discount_limit.discount_limit',
                                  help='The discount limit amount in percentage ')
