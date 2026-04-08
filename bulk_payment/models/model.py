# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, datetime
import logging
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class AccountPaymentInherit(models.Model):
    _inherit = "account.payment"

    payment_line_ids = fields.One2many('account.payment.line', 'payment_id', string="Payment Line Ids")
    payment_ref = fields.Char(string="Reference")
    description = fields.Char(string="Description")

    def _compute_display_name(self):
        for rec in self:
            name = rec.payment_ref if rec.payment_ref else rec.name
            rec.display_name = name

    def action_post(self):
        res = super(AccountPaymentInherit, self).action_post()

        payment_lines = self.env['account.payment.line'].sudo().search([('is_payment_done', '=', False)])

        print(payment_lines)
        for line in payment_lines:
            new_payment_vals = {
                'partner_id': line.partner_id.id,
                'payment_ref': line.ref,
                'date': line.date if line.date else self.date.today(),
                'journal_id': line.journal_id.id,
                'currency_id': self.currency_id.id,
                'payment_type': line.payment_type if line.payment_type else self.payment_type,
                'amount': line.payment_amount,
                'cheque_no': line.memo,
                'description': line.description,
                'payment_method_line_id': line.payment_method.id if line.payment_method else self.payment_method_line_id.id,
            }

            # Check if the amount is not zero before creating the payment

            new_payment = self.env['account.payment'].create(new_payment_vals)
            # _logger.info("Created new payment record with ID: %s", new_payment.id)
            #
            line.write({
                'is_payment_done': True,
            })
            for pay in new_payment:
                if pay.state == 'draft':
                    print(pay.partner_id.name)
                    return pay.action_post()
        return res


class AccountPaymentLine(models.Model):
    _name = "account.payment.line"
    _description = 'Account Payment Lines'

    payment_id = fields.Many2one('account.payment', string="Payments")
    payment_type = fields.Selection(related="payment_id.payment_type")
    partner_id = fields.Many2one(related="payment_id.partner_id", string="Partner")
    date = fields.Date(string="Date")
    cheque_date = fields.Date(string="cheque.Date")
    journal_id = fields.Many2one(related="payment_id.journal_id")
    currency_id = fields.Many2one(related="payment_id.currency_id")
    payment_method = fields.Many2one(related="payment_id.payment_method_line_id")
    payment_amount = fields.Monetary(string="Amount")
    memo = fields.Char(string="Cheque No")
    ref = fields.Char(string="Reference")
    description = fields.Char(related="payment_id.description")
    is_payment_done = fields.Boolean(string="Is payment Done", default=False)
