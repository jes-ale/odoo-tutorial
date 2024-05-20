from datetime import datetime, timedelta
from odoo import fields, models, api

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
    property_id = fields.Many2one('estate_property', string="property", required=True, index=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True, string="Deadline")
    create_date = fields.Date(string="Creation Date", readonly=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = False

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                delta = offer.date_deadline - offer.create_date.date()
                offer.validity = delta.days
            else:
                offer.validity = 0