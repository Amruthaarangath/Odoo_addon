#-*- coding: utf-8 -*-

from odoo import _, fields, models, api
from odoo.tools.populate import compute


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    state = fields.Selection(
        selection_add=[('to_approve', 'To Approve'),('second_approval','Second Approval')]
    )
    current_user = fields.Many2one('res.users',compute = "_compute_current_user")
    current_first_approver = fields.Char(compute = "_compute_partner_approval")
    current_second_approver = fields.Char(compute = "_compute_partner_approval")

    def _compute_current_user(self):
        self.current_user = self.env.user
        print(self.current_user,"userrr")

    def _compute_partner_approval(self):
        self.current_first_approver = self.env['ir.config_parameter'].sudo().get_param('spotter_sale_order_approval.first_user_ids') or False
        self.current_second_approver = self.env['ir.config_parameter'].sudo().get_param('spotter_sale_order_approval.second_user_ids') or False
        # self.current_user = self.env.user
        # for user in first_approver:
        #     if user == self.current_user.user_id:
        #         self.current_first_approver = user
        #         print("crct")
        #     print(user,"tttt")
        # print(self.current_user, "userrr")
        # first = self.current_first_approver
        # user = self.current_user

        # print("first",first_approver)
        print("first",self.current_first_approver)
        print("second",self.current_second_approver)

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