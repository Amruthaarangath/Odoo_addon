# -*- coding: utf-8 -*-

import logging
import pprint
import requests

from werkzeug import urls

from odoo import _, models
from odoo.exceptions import ValidationError

from odoo.addons.payment_multisafepay import const
from odoo.addons.payment_multisafepay.controllers.main import MultisafepayController

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'multisafepay':
            return res

        payload = self._multisafepay_prepare_payment_request_payload()
        _logger.info("sending '/payments' request for link creation:\n%s", pprint.pformat(payload))
        payment_data = self.provider_id._multisafepay_make_request('/payments', data=payload)

        # self.provider_reference = payment_data['data']['order_id']

        checkout_url = payment_data['data']['payment_url']
        parsed_url = urls.url_parse(checkout_url)
        url_params = urls.url_decode(parsed_url.query)
        return {'api_url': checkout_url, 'url_params': url_params}

    def _multisafepay_prepare_payment_request_payload(self):
        user_lang = self.env.context.get('lang')
        base_url = self.provider_id.get_base_url()
        redirect_url = urls.url_join(base_url, MultisafepayController._return_url)
        return {
            "type": "redirect",
            "order_id": f'my-order-id-{self.id}',
            "gateway": "",
            'description': self.reference,
            "currency": self.currency_id.name,
            "amount": self.amount * 100,
            "payment_options": {
                "notification_url": "https://www.example.com/client/notification?type=notification",
                "notification_method": "POST",
                "redirect_url": f'{redirect_url}?ref={self.reference}',
            },
            "close_window": True,
            'locale': user_lang if user_lang in const.SUPPORTED_LOCALES else 'en_US',
            'method': [const.PAYMENT_METHODS_MAPPING.get(
                self.payment_method_code, self.payment_method_code
            )],
            "ip_address": "123.123.123.123",
            "first_name": self.partner_id.name[0],
            "last_name": self.partner_id.name[1],
            "company_name": self.partner_id.company_id.name,
            "address1": self.partner_id.street,
            "zip_code": self.partner_id.zip,
            "city": self.partner_id.city,
            "country": self.partner_id.country_id.name,
            "phone": self.partner_id.phone,
            "email": self.partner_id.email,

        }

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of payment to find the transaction based on multisafepay data.

        :param str provider_code: The code of the provider that handled the transaction
        :param dict notification_data: The notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'multisafepay' or len(tx) == 1:
            return tx
        tx = self.search(
            [('reference', '=', notification_data.get('ref')), ('provider_code', '=', 'multisafepay')]
        )
        if not tx:
            raise ValidationError("multisafepay: " + _(
                "No transaction found matching reference %s.", notification_data.get('ref')
            ))
        return tx

    def _process_notification_data(self, notification_data):
        """ Override of payment to process the transaction based on multisafepay data.

        Note: self.ensure_one()

        :param dict notification_data: The notification data sent by the provider
        :return: None
        """
        super()._process_notification_data(notification_data)
        if self.provider_code != 'multisafepay':
            return
        transaction_id = notification_data.get('transactionid')
        api = self.env['payment.provider'].search([('code', '=', 'multisafepay')])
        api_key = api.api_key
        url = urls.url_join(
            f"https://testapi.multisafepay.com/v1/json/orders/my-order-id-{self.id}?api_key={api_key}", '')
        response = requests.request(method="GET", url=url, json=transaction_id, timeout=60)
        payment_data = response.json()

        # Update the payment state.
        print("payment data", payment_data)
        payment_status = payment_data['data']['status']
        if payment_status == 'completed':
            self._set_done()
        elif payment_status in ['canceled']:
            self._set_canceled("multisafepay: " + _("Canceled payment with status: %s", payment_status))
        else:
            _logger.info(
                "received data with invalid payment status (%s) for transaction with reference %s",
                payment_status, self.reference
            )
            self._set_error(
                "multisafepay: " + _("Received data with invalid payment status: %s", payment_status)
            )
