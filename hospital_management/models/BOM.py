from odoo import fields, models


class HospitalManagement(models.Model):
    _name = "hospitalmanagement.bom"
    _description = "BOM"
    _inherit = "mrp.bom"

state = fields.Selection(selection=[
        ('draft', 'DRAFT'),
        ('approved', 'APPROVED'),
        ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='empty')
visible_id = fields.Many2one('mrp.bom', string='Visible')


def action_visible(self):
    """room allocation based on state"""
    visible_id = self.env['mrp.bom'].search([('state', 'in','approved')], limit=1)
    if visible_id:
        self.visible_id = visible_id.id

