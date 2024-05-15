from odoo import fields, models

class PropertyTypeModel(models.Model):
    _name = "estate_property_type"
    _description = "Type property"

    name = fields.Char(default="Unknown", required=True)
    property_type = fields.Selection(
        string='Type',
        selection=[('house','House'), ('apartment','Apartment'), ('infonavit','Infonavit')]

    )
    postcode = fields.Char()
    
    