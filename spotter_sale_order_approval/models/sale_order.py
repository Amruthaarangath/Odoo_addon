#-*- coding: utf-8 -*-

from odoo import _, fields, models, api
from odoo.tools.populate import compute


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    state = fields.Selection(
        selection_add=[('to_approve', 'To Approve'),('second_approval','Second Approval')]
    )

    def action_confirm(self):
        print("hyyy")
        res = super(SaleOrder, self).action_confirm()
        for record in self:
            if record.state == "draft" or record.amount_total >= 25000:
                record.state = "to_approve"
        return res

    def approve_button(self):
        self.state = "second_approval"


    def second_approval_button(self):
        self.state = "sale"