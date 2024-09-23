# -*- coding: utf-8 -*-

from odoo import fields, models, _
from io import BytesIO
import base64
import openpyxl
from odoo.exceptions import UserError
from odoo import Command


class SaleXlsWizard(models.TransientModel):
    _name = 'sale.xls.wizard'
    _description = "Sale XLS Wizard"

    file = fields.Binary(string='File Upload', help='upload your file in xls format')
    file_name = fields.Char()

    def action_send(self):
        """ action button for file send"""
        try:
            wb = openpyxl.load_workbook(
                filename=BytesIO(base64.b64decode(self.file)), read_only=True
            )
            ws = wb.active
            order_record = self.env['sale.order'].browse(self._context.get('active_id'))
            for row in ws.iter_rows(min_row=2, values_only=True):
                product_name = row[0]
                price = row[1]
                qty = row[2]
                uom = row[3]
                description = row[4]

                product = self.env['product.product'].search([('name', '=', product_name)])
                uom_id = self.env['uom.uom'].search([('name', '=', uom)])

                order_record.write({
                    'partner_id': order_record.partner_id.id,
                    'order_line': [Command.create({
                        'product_id': product.id,
                        'name': description,
                        'product_uom_qty': qty,
                        'price_unit': price,
                        'product_uom': uom_id.id,
                    })]
                })
        except:
            raise UserError(_('Please insert a valid file'))
