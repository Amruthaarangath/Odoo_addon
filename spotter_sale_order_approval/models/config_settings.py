# -*- coding: utf-8 -*-

from odoo import fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_sale_order_approve = fields.Boolean(string='Sale Order Approval',
                                       config_parameter='spotter_sale_order_approval.is_sale_order_approve',
                                       help='check this field to set approvals for sale orders greater than 25K')
    first_user = fields.Many2many('res.users','student_category_rel',
      'student_id', 'category_id', string="First Approver")

    second_user = fields.Many2many('res.users', string="Second Approver")