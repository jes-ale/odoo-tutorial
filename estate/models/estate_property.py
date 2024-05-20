from datetime import datetime, timedelta
from odoo import fields, models , api

class PropertyModel(models.Model):
    _name = "estate_property"
    _description = "Test Property"
    
    active = fields.Boolean(default=True)
    name = fields.Char(default="Unknown", required=True)
    description = fields.Char(compute="_compute_description")
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(default=0, string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean(default=True)
    garden = fields.Boolean(default=True)
    garden_area = fields.Integer(default=0, string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Type is used to separate Leads and Opportunities")
    state = fields.Selection(
        string='Type',
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        copy=False,
        default="new"
    )
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    property_type_id = fields.Many2one('estate_property_type', string='Property type', index=True)
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user, copy=False)
    partner_id = fields.Many2one('res.partner', string='Customer', index=True, tracking=10,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]"
    )
    tags_ids = fields.Many2many("estate_property_tags", string='Name')
    offers_id = fields.One2many("property_offer", "property_id", string="Offers")
    total_area = fields.Integer(compute='_compute_total_area', store=True, copy=False, string="Total Area (sqm)")
    best_price = fields.Float(compute='_compute_best_offer', store=True, string="Best Offer")

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('partner_id.name')
    def _compute_description(self):
        for record in self:
            record.description = record.partner_id.name

    @api.depends('offers_id.price')
    def _compute_best_offer(self):
        for record in self:
            prices = record.offers_id.mapped('price')
            record.best_price = max(prices, default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = ''
    
    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled properties cannot be sold.")
            property.state = 'sold'

    def action_cancel(seld):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            property.state = 'canceled'

