from odoo import fields, models


class HospitalManagement(models.Model):
    # _name = "patient"
    _inherit = "hr.employee"

    qualification = fields.Char(string = "Qualification")
    age = fields.Integer(string = "Age")
    shift = fields.Char(string = "Shift")
    fees = fields.Integer(string ="fees")