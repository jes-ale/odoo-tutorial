from odoo import fields, models


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    offer_ids = fields.One2many("property_offer", "partner_id", string='Offer')