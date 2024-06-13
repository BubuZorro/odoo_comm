from odoo import models, fields, api, exceptions
from odoo.tools import date_utils, float_is_zero

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'id desc'

    name = fields.Char('Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Available From', copy=False, default=date_utils.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
        )
    active = fields.Boolean(default=False)
    state = fields.Selection(string='Status',
                             selection=[('new','New'), ('off_rec','Offer Received'), ('off_acc','Offer Accepted'), ('sold','Sold'), ('canceled','Canceled')])
    property_type_id = fields.Many2one('estate.property.type', string ='Property Type')
    buyer = fields.Many2one('res.partner', copy=False)
    salesperson = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offer')
    total_area = fields.Integer('Total Area (sqm)', compute='_compute_area')
    best_price = fields.Float('Best Offer', compute='_compute_best_price')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive.')
    ]

    @api.depends('garden_area', 'living_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
        return True

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            prices = [offer.price for offer in record.offer_ids if offer.price]
            if prices:
                record.best_price = max(prices)
            else:
                record.best_price = 0.0
        return True

    @api.onchange('garden')
    def onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = ''
            self.garden_orientation = False

    def set_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise exceptions.UserError('Canceled properties cannot be sold')
            record.state = 'sold'
        return True

    def set_canceled(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError('Sold properties cannot be canceled')
            record.state = 'canceled'
        return True

    @api.constrains('expected_price', 'selling_price')
    def check_sellings_price(self):
        for record in self:
            if record.selling_price < (record.expected_price * 0.9) and not float_is_zero(record.selling_price, precision_rounding=0.01):
                raise exceptions.ValidationError("The selling price must be at least 90% of the expected price!")
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        if not set(self.mapped("state")) <= {"new", "canceled"}:
            raise exceptions.UserError("Only new and canceled properties can be deleted.")
