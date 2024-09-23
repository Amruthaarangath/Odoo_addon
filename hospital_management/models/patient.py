from odoo import fields, models


class HospitalManagement(models.Model):
    # _name = "patient"
    _inherit = "res.partner"

    patient = fields.Char(string="Patient")
    age = fields.Integer(string="Age")
    blood_group = fields.Selection(
        [('A+ve', 'A+ve'), ('A-ve', 'A-ve'), ('B+ve', 'B+ve'), ('B-ve', 'B-ve'), ('o-ve', 'o-ve'),
         ('O+ve', 'O+ve'), ('AB+ve', 'AB+ve'), ('AB-ve', 'AB-ve')])
    date = fields.Date(string="DOB")

