from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PropertyModel(models.Model):
    _inherit = 'estate_property'

    @api.model
    def action_sold(self):
        print("Estate Property action_sold method called.")
        
        partner_id = self.buyer_id.id

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
        move = self.env['account_move'].create(move_vals)
        return super(self).action_sold()
