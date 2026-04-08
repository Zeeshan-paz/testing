from odoo import models, fields, api


class ImportLcReportWizard(models.TransientModel):
    _name = 'payment.report'
    _description = 'Payment Report Voucher'

    customer = fields.Many2one('res.partner', string="Partner")
    payment_ref = fields.Many2many('account.payment', string="Payment Ref", domain="[('partner_id', '=', customer)]")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")

    @api.onchange('customer')
    def _onchange_customer(self):

        if self.customer:
            return {
                'domain': {
                    'payment_ref': [('partner_id', '=', self.customer.id)],
                }
            }
        else:
            return {
                'domain': {
                    'contract_no': []
                }
            }

    def get_payment_voucher(self):
        print("hit the function Import LC Report")

        domain = []

        if self.customer:
            domain += [('partner_id', '=', self.customer.id)]
        if self.payment_ref:
            domain += [('id', '=', self.payment_ref.ids)]
        if self.from_date:
            domain += [('date', '>=', self.from_date)]

        if self.to_date:
            domain += [('date', '<=', self.to_date)]

        orders = self.env['account.payment'].search(domain)
        delivery_data = []
        total_amount = 0.0
        for order in orders:
            total_amount += order.amount_company_currency_signed
            print("delivery entries", order.name)
            delivery_data.append({
                'name': order.name,
                'journal': order.journal_id.name,
                'partner': order.partner_id.name,
                'amount': order.amount_company_currency_signed,
                'date': order.date,
                'method': order.payment_method_line_id.name,
                'amount_in_words': order.check_amount_in_words,
                'cheque_no' : order.cheque_no,
                'description': order.description,
            })
        amount_in_words = self.env.company.currency_id.amount_to_text(abs(total_amount))
        print(amount_in_words)

        total_amount = abs(total_amount)  # optional safety

        data = {
            'delivery_data' : delivery_data,
            'customer' : self.customer.name,
            'amount_in_words' : amount_in_words,
            'total_amount' : total_amount,
            'bill_date' : self.to_date or self.from_date,
            'from' : self.from_date,
            'to' : self.to_date,
            'name' : self.env.company.name,
            'street' : self.env.company.street,
            'street2' : self.env.company.street2,
            'city' : self.env.company.city,
            'country' : self.env.company.country_id.name,
            'phone' : self.env.company.phone,
            'email' : self.env.company.email,
        }

        return self.env.ref('bulk_payment.payment_voucher_report_action').report_action(self, data=data)
