from odoo import fields, models

class PropertyTagsModel(models.Model):
    _name = "estate_property_tags"
    _description = "Property Tags"

    active = fields.Boolean(default=True)
    name = fields.Char(default="Unknown", required=True)
    description = fields.Text()
    
    _sql_constraints = [
        ('unique_tag_name', 'unique(name)', 'Tag names shoulde be unique')
    ]