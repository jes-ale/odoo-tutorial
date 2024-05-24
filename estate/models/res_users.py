from odoo import fields, models


class Users(models.Model):
    _inherit = 'hr.employee'

    property_ids = fields.One2many(
        'estate_property',
        'user_id',
        string='Properties',
        domain=[('state', '=', 'available')]
        )
    