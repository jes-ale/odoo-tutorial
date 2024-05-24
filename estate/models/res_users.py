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
    hr_presence_state = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('not_set', 'Not Set'),
    ], string="Presence State")
    hr_icon_display = fields.Char(string="Icon Display")
    last_activity_time = fields.Datetime(string="Last Activity Time")
    last_activity = fields.Char(string="Last Activity")