from odoo import fields, models, api

class PropertyTagsModel(models.Model):
    _name = "estate_property_tags"
    _description = "Property Tags"
    _order = "name"

    active = fields.Boolean(default=True)
    name = fields.Char(default="Unknown", required=True)
    description = fields.Text()

    @api.constrains('name')
    def _check_tag_name(self):
        for record in self:
            if self.search([('name', '=', record.name), ('id', '!=', record.id)]):
                raise ValidationError("Tag names should be unique")