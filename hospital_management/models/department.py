from odoo import fields, models


class HospitalManagement(models.Model):
    _name = "hospitalmanagement.department"
    _description = "hospital management department"

    name = fields.Char(string="name")