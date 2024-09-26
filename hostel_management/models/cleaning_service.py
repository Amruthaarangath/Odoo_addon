# -*- coding: utf-8 -*-
from odoo import fields, models


class CleaningService(models.Model):
    _name = "hostel.cleaning.service"
    _description = "Hostel Room Cleaning Service"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "room_id"

    room_id = fields.Many2one("hostel.room.management", string="Room", required=True, help="Room which want to clean")
    time = fields.Float(string='Time', help="Time for cleaning service")
    cleaning_staff_id = fields.Many2one("res.users", "Staff", help="Responsible staff for cleaning")
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('done', 'Done'),
    ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='new')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    date = fields.Date(string="Date", help="Available date for cleaning")

    def assign_button(self):
        """assign button"""
        self.state = "assigned"
        self.room_id.state = 'cleaning'

    def complete_button(self):
        """complete button"""
        self.state = "done"
        self.room_id._compute_change_state()
