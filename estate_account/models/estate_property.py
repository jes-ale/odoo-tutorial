from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PropertyModel(models.Model):
    _inherit = 'estate.estate_property'

    @api.model
    def action_sold(self):
        print("Overridden action_sold method called")

        result = super(PropertyModel, self).action_sold()

        partner_id = self.user_partner_id.id

        selling_price = self.selling_price
        commission = selling_price * 0.06
        admin_fee = 100.00

        invoice_values = {
            'partner_id': partner_id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'Commission (6% of selling price)',
                    'quantity': 1,
                    'price_unit': commission,
                }),
                (0, 0, {
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': admin_fee,
                }),
            ],
        }

        invoice = self.env['estate_account'].create(invoice_values)

        print(f"Created invoice: {invoice}")

        return result
