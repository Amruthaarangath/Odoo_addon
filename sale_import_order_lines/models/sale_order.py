# -*- coding: utf-8 -*-

from odoo import models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_import_file(self):
        """function for wizard form"""
        return {'type': 'ir.actions.act_window',
                'name': _('Import Lines'),
                'res_model': 'sale.xls.wizard',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'file': 'form'}
