# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime


class LeaveRequest(models.Model):
    _name = "leave.request"
    _description = "leave request"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "display_name"

    student_id = fields.Many2one("hostel.student", string="Student",
                                 ondelete='cascade', help="Select name", required=True)
    leave_date = fields.Date(string="leave date", required=True, help="Set the leave date", ondelete='cascade')
    arrival_date = fields.Date(string="Arrival date", required=True,
                               help="Set the date which you are arrive", ondelete='cascade')
    display_name = fields.Char(compute="_compute_display_name", string="ID", ondelete='cascade')
    status = fields.Selection(selection=[
        ('new', 'New'),
        ('approved', 'Approved'),
    ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='new')
    room_id = fields.Many2one("hostel.room.management", string="Room", help="enter your room number")
    duration = fields.Integer(string="Duration", compute="_compute_date_calculation", store=True)

    @api.constrains('leave_date', 'arrival_date')
    def _check_date(self):
        """validate leave date"""
        for record in self:
            if record.leave_date and record.leave_date < date.today():
                raise ValidationError(_("Leave date must be today day or future date"))
            elif record.arrival_date and record.leave_date and record.arrival_date < record.leave_date:
                raise ValidationError(_("Date must be greater than the Leave date you choose"))

    def leave_action(self):
        """Approve button action"""
        self.room_id = self.student_id.room_id
        room = self.student_id.room_id
        if room:
            student_leaves = self.env['leave.request'].search([
                ('room_id', '=', room.id),
                ('id', '!=', self.id)
            ])

            same_dates = []

            for leave in student_leaves:
                start = max(self.leave_date, leave.leave_date)
                end = min(self.arrival_date, leave.arrival_date)
                if start < end:
                    same_dates.append((start, end))
            if same_dates:
                for period in same_dates:
                    common_date = period[0]
                    self.env['hostel.cleaning.service'].create({
                        'room_id': room.id,
                        'state': 'new',
                        'date': common_date
                    })
                self.status = "approved"
                room.state = 'cleaning'
            else:
                self.status = "approved"

    @api.depends('student_id.name', 'leave_date')
    def _compute_display_name(self):
        """name and leave date combination for _rec_name """
        for record in self:
            if record.student_id.name and record.leave_date:
                val = str(record.leave_date)
                display_name = [record.student_id.name, val]
                record.display_name = ' / '.join(filter(None, display_name))
            else:
                record.display_name = _('New')

    @api.depends('leave_date', 'arrival_date')
    def _compute_date_calculation(self):
        """duration between start date and arrival date"""
        for rec in self:
            if rec.leave_date and rec.arrival_date:
                d1 = datetime.strptime(str(rec.leave_date), '%Y-%m-%d')
                d2 = datetime.strptime(str(rec.arrival_date), '%Y-%m-%d')
                d3 = d2 - d1
                rec.duration = str(d3.days)
