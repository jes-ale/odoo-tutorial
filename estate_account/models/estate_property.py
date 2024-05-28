from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PropertyModel(models.Model):
    _inherit = 'estate_property'

    def action_sold(self):
        print("Estate Property action_sold method called.")
        
        partner_id = self.user_partner_id.id

        move_vals = {
            'partner_id': partner_id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'Selling Price Commission (6%)',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                (0, 0, {
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00,
                }),
            ],
        }
        move = self.env['account.move'].create(move_vals)
        return super(PropertyModel, self).action_sold()
