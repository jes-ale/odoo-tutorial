from odoo import fields, models, api

class PropertyTypeModel(models.Model):
    _name = "estate_property_type"
    _description = "Type property"
    _order = "name"

    name = fields.Char(default="Unknown", required=True)
    property_ids = fields.One2many('estate_property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1, help="Used to order propertys.")

    @api.constrains('name')
    def _check_type_name(self):
        for record in self:
            if self.search([('name', '=', record.name), ('id', '!=', record.id)]):
                raise ValidationError("Type names should be unique")
    
    