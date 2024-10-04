#-*- coding: utf-8 -*-

from odoo import _, fields, models, api
from odoo.tools.populate import compute


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    state = fields.Selection(
        selection_add=[('to_approve', 'To Approve'),('second_approval','Second Approval')]
    )

    @api.constrains('amount_total')
    def _total_amount_calculation(self):
        if self.amount_total > 25000:
            self.state = "to_approve"


    def approve_button(self):
        print("hy")
        print("hy", self.amount_total)
        self.state = "second_approval"


    def second_approval_button(self):
        self.state = "sale"