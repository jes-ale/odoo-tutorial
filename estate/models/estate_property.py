from datetime import datetime, timedelta
from odoo import fields, models

class PropertyModel(models.Model):
    _name = "estate_property"
    _description = "Test Property"
    
    active = fields.Boolean(default=True)
    name = fields.Char(default="Unknown", required=True)
    description = fields.Char()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(default=0)
    facades = fields.Integer()
    garage = fields.Boolean(default=True)
    garden = fields.Boolean(default=True)
    garden_area = fields.Integer(default=0)
    garden_orientation = fields.Selection(
        string='Type',
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
    total_area = fields.Integer(self: 'garden_area' + 'living_area', copy=False)

   
