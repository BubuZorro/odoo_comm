from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char('Tag', required=True)
    color = fields.Integer('Color')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Name must be unique.')
    ]
