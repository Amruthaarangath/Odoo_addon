from odoo import fields, models , api , _


class HospitalManagement(models.Model):
    _name = "hospitalmanagement.op"
    _description = "hospital management op"

    sequence = fields.Char(string = "Reference",readonly = True,default = lambda self: _('New'))
    token_number = fields.Integer(string = "Token number")
    name = fields.Char(string = "name")
    age = fields.Integer(string = "age")
    date = fields.Date(string = "Date")
    patient_id = fields.Many2one("res.partner","patient")
    doctor_id = fields.Many2one("hr.employee","doctor")

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the op model """
        for vals in vals_list:
            if vals.get('sequence', _('New')) == _('New'):
                vals['sequence'] = self.env['ir.sequence'].next_by_code(
                    'hospitalmanagement.op')
        return super().create(vals_list)

    @api.onchange('patient_id')
    def compute_age(self):
        self.age = self.patient_id.age