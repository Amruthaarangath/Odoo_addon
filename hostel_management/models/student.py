# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import date


class HostelStudent(models.Model):
    _name = 'hostel.student'
    _description = 'Hostel Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"

    name = fields.Char(string="Name", required=True, help="Enter your name")
    sid = fields.Char(string="Reference", readonly=True, default=lambda self: _('New'))
    dob = fields.Date(string="DOB", help="Set your DOB")
    room_id = fields.Many2one("hostel.room.management", string="Room", readonly=True)
    image = fields.Binary(help="Set your image")
    file_name = fields.Char()
    receive_email = fields.Boolean(string="Receive mail", help="Check this boolean to receive mail")
    email = fields.Char(string="Email", help="Enter your email", required=True)
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    age = fields.Integer(string="age", compute="_onchange_get_age")

    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    partner_id = fields.Many2one('res.partner', string='Partner')
    invoice_count = fields.Integer(string='Invoices', compute='_compute_invoice_count', default=0)
    invoice_ids = fields.One2many('account.move', 'student_id', string='Invoices')
    active = fields.Boolean(default=True)
    invoice_status = fields.Selection(selection=[
        ('pending', 'Pending'),
        ('done', 'Done'),
    ], string='Status', readonly=True, copy=False,
        tracking=True, compute='_compute_invoice_status_change')
    monthly_amount = fields.Float(string="Monthly amount", compute='_compute_monthly_amount')
    user_id = fields.Many2one('res.users', 'User')

    @api.onchange('dob')
    def _onchange_get_age(self):
        """age derivation from dob"""
        if self.dob:
            today_date = date.today()
            dob = fields.Datetime.to_datetime(self.dob).date()
            today_age = int((today_date - dob).days / 365)
            self.age = today_age
        else:
            self.age = 0

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the  model """
        for vals in vals_list:
            if vals.get('sid', _('New')) == _('New'):
                """create a partner"""
                vals['sid'] = self.env['ir.sequence'].next_by_code(
                    'hostel.student')

            partner_id = {
                'name': vals.get('name'),
                'email': vals.get('email'),
                'street': vals.get('street'),
                'street2': vals.get('street2'),
                'city': vals.get('city'),
                'state_id': vals.get('state_id'),
                'zip': vals.get('zip'),
                'country_id': vals.get('country_id')

            }
            vals['partner_id'] = self.env['res.partner'].create(partner_id).id
            return super().create(vals_list)

    def action_room_alot(self):
        """room allocation based on state"""
        room_id = self.env['hostel.room.management'].search([('state', 'in', ['partial', 'empty'])], limit=1)
        if room_id:
            self.room_id = room_id.id
            room_id._compute_change_state()
        else:
            raise ValidationError(_("No rooms are available"))

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        """invoice smart tab"""
        for student in self:
            student.invoice_count = self.env['account.move'].search_count([('student_id', '=', student.id)])

    def action_view_invoices(self):
        """invoice view"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('student_id', '=', self.id)],
            'context': "{'create': True}",
        }

    def vacate_room(self):
        """room vacate"""
        self.active = False
        self.room_id._compute_change_state()
        # self.room_id = False

        if self.room_id.state == 'empty':
            self.env['hostel.cleaning.service'].create({
                'room_id': self.room_id.id,
                'state': 'new'
            })
            self.room_id.state = 'cleaning'
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'hostel.student'
            }
        self.room_id = False

    def _compute_invoice_status_change(self):
        """invoice status change"""
        for state in self:
            status = self.env['account.move'].search([('student_id', '=', state.id), ('state', '!=', 'draft')])
            if status:
                state.invoice_status = 'done'
            else:
                state.invoice_status = 'pending'

    def _compute_monthly_amount(self):
        """monthly amount"""
        self.monthly_amount = self.room_id.total_rent

    def create_user(self):
        """automated action user creation"""
        for user in self:
            user_id = user.env['res.users'].create([{
                'name': user.name,
                'login': user.email,
                'partner_id': user.partner_id.id
            }])
            user.user_id = user_id.id


