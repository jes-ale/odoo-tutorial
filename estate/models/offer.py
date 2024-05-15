from odoo import fields, models

class OfferModel(models.Model):
    _name = "property_offer"
    _description = "Property Offer"

    price = fields.Float()
    status = fields.Selection(
        string='Type',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    partner_id = fields.Many2one('res.partner', string='Customer', index=True, tracking=10,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        required=True
    )
    property_id = fields.Many2one('estate_property', string='Property', required=True)