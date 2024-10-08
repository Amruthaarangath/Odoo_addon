# -*- coding: utf-8 -*-

import logging

import requests
from werkzeug import urls

from odoo import _, fields, models

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('multisafepay', 'MultiSafePay')], ondelete={'multisafepay': 'set default'}
    )
    api_key = fields.Char(
        string=" API Key",
        help="The Test or Live API Key depending on the configuration of the provider",
        required_if_provider="multisafepay", groups="base.group_system"
    )

    def _multisafepay_make_request(self, endpoint, data=None, method='POST'):
        """ Make a request at multisafepay endpoint.

        Note: self.ensure_one()

        :param dict data: The payload of the request
        :param str method: The HTTP method of the request
        :return The JSON-formatted content of the response
        :rtype: dict
               """
        self.ensure_one()
        url = urls.url_join(f"https://testapi.multisafepay.com/v1/json/orders?api_key={self.api_key}", '')
        headers = {
            'Content-Type': 'application/json',
            'accept': 'application/json'
        }
        response = requests.request(method, url, json=data, headers=headers, timeout=60)
        return response.json()
