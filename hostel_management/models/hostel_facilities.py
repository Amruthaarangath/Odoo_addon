# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class HostelFacilities(models.Model):
    _name = "hostel.facilities"
    _description = "Hostel Facilities"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", help="Enter the facility name")
    charge = fields.Integer(string="Charge", help="Set charge of the facility")
    active = fields.Boolean(default=True)

    @api.constrains('charge')
    def _check_charge(self):
        """facility charge check"""
        for record in self:
            if record.charge <= 0:
                raise ValidationError(_("Update charge of facility to a positive value"))
