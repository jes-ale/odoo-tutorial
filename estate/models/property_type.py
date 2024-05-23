from odoo import fields, models, api

class PropertyTypeModel(models.Model):
    _name = "estate_property_type"
    _description = "Type property"
    _order = "name"

    name = fields.Char(default="Unknown", required=True)
    property_ids = fields.One2many('estate_property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1, help="Used to order propertys.")
    offer_ids = field.One2many('property_offer', 'property_type_id')
    offer_count = field.Integer(compute='_check_offer_ids', store=True)

    @api.constrains('name')
    def _check_type_name(self):
        for record in self:
            if self.search([('name', '=', record.name), ('id', '!=', record.id)]):
                raise ValidationError("Type names should be unique")
    
    @api.depends('offer_ids')
    def _check_offer_ids(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    
    