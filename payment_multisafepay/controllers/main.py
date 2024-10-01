#-*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class MultisafepayController(http.Controller):
    _return_url = '/payment/multisafepay/return'

    @http.route(_return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False,
        save_session=False)
    def multisafepay_return_from_checkout(self, **data):
        print("amm",data)
        _logger.info("handling redirection from MultiSafePay with data:\n%s", pprint.pformat(data))
        request.env['payment.transaction'].sudo()._handle_notification_data('multisafepay', data)
        return request.redirect('/payment/status')