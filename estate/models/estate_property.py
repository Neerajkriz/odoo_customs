"""from odoo import models, fields

class EstateProperty(models.Model):
	_name = 'estate.property'
	_description = 'Estate property'
	
	name = fields.Char('Name', required = True)
	description = fields.Text('Description')
	postcode = fields.Char('Postcode')
	date_availability = fields.Date('Available From')
	expected_price = fields.Float('Expected Price', required = True)
	selling_price = fields.Integer('Selling price')
	bedrooms = fields.Float('Bedrooms')
	living_area = fields.Integer('Living area')
	facades = fields.Integer('Facades')
	garage = fields.Boolean('Garage')
	garden = fields.Boolean('Garden')"""
	

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')], string="Garden Orientation"
    )

    total_area = fields.Integer(compute="_compute_total_area", store=True)

    state = fields.Selection([
        ('new', 'New'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], string="Status", required=True, default='new')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and record.selling_price < 0.9 * record.expected_price:
                raise ValidationError("Selling price must be at least 90% of expected price.")

    def action_mark_sold(self):
        for record in self:
            if record.state != 'cancelled':
                record.state = 'sold'

    def action_mark_cancel(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'cancelled'
