from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char('Type', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many('estate.property.offer')
    offer_count = fields.Integer(compute="_compute_offer_count")

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Name must be unique.')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            offer_list = self.env['estate.property.offer'].search([
                        ('property_type_id', '=', record.id),
                        ])
            record.offer_count = offer_list.count(record.id)
        return True
