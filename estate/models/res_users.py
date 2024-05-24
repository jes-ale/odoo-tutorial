from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        'estate_property',
        'user_id',
        string='Properties',
        domain=[('state', '=', 'available')]
        )
    
    user_partner_id = fields.Many2one('res.partner', string="Related Partner")