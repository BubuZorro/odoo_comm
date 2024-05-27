from odoo import models, fields, api, exceptions
from odoo.tools import date_utils
from datetime import timedelta, date

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted','Accepted'), ('refused','Refused')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7, string='Validity (days)')
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline')
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'Price must be strictly positive.')
    ]

    @api.depends('create_date','validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = date.today() + timedelta(days=record.validity)

    @api.depends('date_deadline')
    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = abs((record.date_deadline - record.create_date.date()).days)
            else:
                record.validity = abs((record.date_deadline - date.today()).days)

    def accept_offer(self):
        for record in self:
            if 'accepted' in self.mapped('property_id.offer_ids.status'):
                raise exceptions.UserError('Only one offer can be accepted')
            else:
                record.status = 'accepted'
                record.property_id.state = 'off_acc'
                record.property_id.buyer = record.partner_id
                record.property_id.selling_price = record.price
        return True

    def refuse_offer(self):
        for record in self:
            record.status = 'refused'
            """ if not 'accepted' in self.mapped('property_id.offer_ids.status'):
                record.property_id.selling_price = 0 """
        return True
