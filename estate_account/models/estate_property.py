from odoo import models, fields, api, _
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError(_("Canceled properties cannot be sold."))
            record.state = 'sold'
            self.create_invoice(record)
        return super(EstateProperty, self).action_sold()

    def create_invoice(self, record):
        invoice_vals = {
            'partner_id': record.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'name': record.name,
                'quantity': 1,
                'price_unit': record.selling_price,
            })],
        }
        self.env['account.move'].create(invoice_vals)
        print("Invoice created for property:", record.name)