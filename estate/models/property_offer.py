from datetime import datetime, timedelta
from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class OfferModel(models.Model):
    _name = "property_offer"
    _description = "Property Offer"

    price = fields.Float()
    status = fields.Selection(
        string='Type',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
        readonly=True
    )
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    partner_id = fields.Many2one('res.partner', string='Customer', index=True, tracking=10,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        required=True
    )
    property_id = fields.Many2one('estate_property', string="property", required=True, index=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True, string="Deadline", readonly=True)
    create_date = fields.Datetime(string="Creation Date", readonly=True)

    def action_accept(self):
        for offer in self:
            if offer.property_id.state == 'offer accepted':
                raise UserError("An offer was already accepted.")
            offer.status = 'accepted'
            offer.property_id.partner_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer accepted'
    
    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
            offer.property_id.state = 'offer received'
            offer.property_id.partner_id = ''

    @api.onchange('status')
    def _onchange_garden(self):
        for offer in self:
            if offer.status == 'refused':
                offer.property_id.selling_price = 0.0

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
                