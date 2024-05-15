from odoo import fields, models

class PropertyTypeModel(models.Model):
    _name = "estate_property_type"
    _description = "Type property"

    name = fields.Char(default="Unknown", required=True)
    
    