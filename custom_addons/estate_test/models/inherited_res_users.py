from odoo import models, fields, api

class InheritedResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'salesperson', domain="['|', ('state','=','new'), ('state','=','off_rec')]")
