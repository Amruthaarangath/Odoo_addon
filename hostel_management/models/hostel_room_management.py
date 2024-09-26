# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo import Command
from datetime import date
from odoo.exceptions import ValidationError


class RoomManagement(models.Model):
    _name = "hostel.room.management"
    _description = "Hostel Room Management"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "room_number"

    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    rent = fields.Monetary(string="Rent", help="enter the room rent")
    room_number = fields.Char(string="Reference", readonly=True, default=lambda self: _('New'), copy=False)
    room_type = fields.Selection([('single', 'Single'), ('double', 'Double')], help="Select room type which you want")
    no_of_beds = fields.Integer(string="Number of beds", help="Enter the number of beds which you need")
    state = fields.Selection(selection=[
        ('empty', 'Empty'),
        ('cleaning', 'Cleaning'),
        ('partial', 'Partial'),
        ('full', 'Full'),
    ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='empty', compute='_compute_change_state')
    facility_ids = fields.Many2many("hostel.facilities", string="Facilities", help="Select the allowed facilities")
    student_ids = fields.One2many('hostel.student', 'room_id', string='Students', readonly=True)
    total_rent = fields.Monetary(string="Total rent", compute='_onchange_total_room_rent',
                                 required=True, help="Set the room rent")
    post_invoice_count = fields.Integer(string='Posted Invoices', compute='_compute_post_invoice_count', default=0)
    draft_invoice_count = fields.Integer(string='Draft Invoices', compute='_compute_draft_invoice_count', default=0)
    invoice_ids = fields.One2many('account.move', 'student_id', string='Invoices')
    pending_amount = fields.Monetary(string='Pending amount', compute="_compute_pending_amount", store=True,
                                     help="Total amount from unpaid invoices")
    active = fields.Boolean(default=True)
    image = fields.Binary(help="Set your image")

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the room model """
        for vals in vals_list:
            if vals.get('room_number', _('New')) == _('New'):
                vals['room_number'] = self.env['ir.sequence'].next_by_code(
                    'hostel.room.management')
        return super().create(vals_list)

    @api.depends('no_of_beds', 'student_ids')
    def _compute_change_state(self):
        """state change """
        for record in self:
            student_length = len(record.student_ids)
            if student_length == 0:
                record.state = "empty"
            elif student_length >= record.no_of_beds:
                record.state = "full"
            else:
                record.state = "partial"

    @api.onchange("rent", "facility_ids")
    def _onchange_total_room_rent(self):
        """rent calculation from room rent and facilities"""
        for room in self:
            rec = room.rent
            total_rent = sum(self.facility_ids.mapped('charge'))
            room.total_rent = total_rent + rec

    def monthly_invoice_button(self):
        """create invoice from monthly invoice button"""
        for student in self.student_ids:
            if self.env['account.move'].search([
                ('invoice_date', '=', date.strftime(date.today(), "%Y-%m-01")),
                ("move_type", "=", "out_invoice"),
                ("student_id", "=", student.ids),
            ]):
                raise ValidationError(_("current month invoice is created"))
            else:
                self.env['account.move'].create([{
                    'move_type': 'out_invoice',
                    'partner_id': student.partner_id.id,
                    'invoice_date': date.today().replace(day=1),
                    'student_id': student.id,
                    'invoice_line_ids': [Command.create({
                        'product_id': self.env.ref('hostel_management.product_rental').id,
                        'price_unit': self.total_rent,
                    })]
                }])
                template = self.env.ref('hostel_management.email_template_invoice_post')
                template.send_mail(student.id, force_send=True)

    @api.depends('invoice_ids')
    def _compute_post_invoice_count(self):
        """ smart tab for posted invoices"""
        for student in self:
            student.post_invoice_count = self.env['account.move'].search_count(
                [('student_id', 'in', student.student_ids.ids), ('state', '!=', 'draft')])

    def action_view_post_invoices(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('student_id', '=', self.student_ids.ids), ('state', '!=', 'draft')],
            'context': "{'create': True}",
        }

    @api.depends('invoice_ids')
    def _compute_draft_invoice_count(self):
        """invoice smart tab for draft invoices"""
        for student in self:
            student.draft_invoice_count = self.env['account.move'].search_count(
                [('student_id', 'in', student.student_ids.ids), ('state', '=', 'draft')])

    def action_view_draft_invoices(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('student_id', '=', self.student_ids.ids), ('state', '=', 'draft')],
            'context': "{'create': True}",
        }

    @api.depends('invoice_ids')
    def _compute_pending_amount(self):
        for student in self:
            """pending amount from invoices"""
            pending_invoice = self.env['account.move'].search(
                [('student_id', 'in', student.student_ids.ids)])
            student.pending_amount = sum(pending_invoice.mapped('amount_total'))
