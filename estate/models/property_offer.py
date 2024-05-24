from datetime import datetime, timedelta
from odoo import fields, models, api, exceptions
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class OfferModel(models.Model):
    _name = "property_offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string='Type',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
        readonly=True
    )
    partner_id = fields.Many2one('res.partner', string='Customer', index=True, tracking=10,
        required=True
    )
    property_id = fields.Many2one('estate_property', string="property", required=True, index=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True, string="Deadline", readonly=True)
    create_date = fields.Datetime(string="Creation Date", readonly=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True, string="Property Type")

    def action_accept(self):
        for offer in self:
            if any(other_offer.status == 'accepted' for other_offer in offer.property_id.offers_id):
                raise UserError("An offer was already accepted.")
            offer.status = 'accepted'
            offer.property_id.partner_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer-accepted'
    
    def action_refuse(self):
        for offer in self:
            if offer.status == 'accepted':
                offer.status = 'refused'
                offer.property_id.selling_price = 0
                if not any(other_offer.status == 'accepted' for other_offer in offer.property_id.offers_id):
                    offer.property_id.state = 'offer-received' if any(o.status == 'accepted' for o in offer.property_id.offers_id) else 'new'
            else:
                offer.status = 'refused'

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                if not offer.create_date:
                    offer.create_date = fields.Datetime.now()
                delta = offer.date_deadline - offer.create_date.date()
                offer.validity = delta.days
            else:
                offer.validity = 0

    @api.constrains('price')
    def _check_price(self):
        for offer in self:
            if offer.price < 0:
                raise ValidationError("The price should be upper than 0")
            offer.property_id.state = 'offer-received'

    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        price = vals.get('price')

        if property_id and price:
            property_obj = self.env['estate.property'].browse(property_id)
            existing_offers = property_obj.offer_ids.filtered(lambda offer: offer.id != vals.get('id'))
            if existing_offers and any(offer.price <= price for offer in existing_offers):
                raise exceptions.ValidationError("Offer price must be higher than existing offers.")     

        vals['status'] = 'offer-received'

        return super(OfferModel, self).create(vals)         