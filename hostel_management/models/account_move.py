# -*- coding: utf-8 -*-
from odoo import fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    student_id = fields.Many2one("hostel.student", string="Student", help="Enter name of the student")

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for record in self:
            if record.move_type in ['out_invoice'] and record.state == 'posted':
                template = self.env.ref('hostel_management.email_template_invoice_post')
                template.send_mail(record.student_id.id, force_send=True)
        return res
