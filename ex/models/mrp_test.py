# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class MrpTest(models.Model):
    _name = "mrp.test"
    _description = "Mrp Test"

    mrp = fields.Many2one("mrp.production", string="Room", readonly=True)