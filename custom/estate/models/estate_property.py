from odoo import api,fields, models
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
class PropertyModel(models.Model):
    _name = "estate.property"
    _description = " estate model"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default=(date.today() + relativedelta(months=3)))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north','North'),('east','East'),('south','South'),('west','West')])
    active = fields.Boolean(default=False)
    state = fields.Selection(
        string='Status',
        selection=[('new','NEW'),('received','Offer Received'),('accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')],
        required=True,
        default='new',
        copy=False
    )
    property_type_id = fields.Many2one("estate.property.type",string="type")
    buyer_id = fields.Many2one('res.partner',string="buyer", copy=False)
    salesperson_id= fields.Many2one('res.users',string='Salesperson', default=lambda self: self.env.user)
    tag_ids= fields.Many2many('estate.property.tag',string="tag")
    offer_ids = fields.One2many('estate.property.offer','property_id',string="offer")
    
    _sql_constraints = [
        ('check_expected_price','CHECK(expected_price > 0)','the expected price should be a positive value'),
        ('check_selling_price','CHECK(selling_price >= 0)', 'selling price must be a positive value'),
        ('unique_name','UNIQUE(name)',"name should be unique for every property")
    ]
    
    total_area = fields.Integer(compute="_compute_area")
    
    @api.depends("garden_area","living_area")
    def _compute_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    best_offer = fields.Float(compute="_best_offer")

    @api.depends("offer_ids.price")
    def _best_offer(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_offer = max(rec.offer_ids.mapped("price"))
            else:
                rec.best_offer = 0
    
    @api.onchange("garden")
    def _onchange_garden(self):
        if(self.garden):
            self.garden_area=10
            self.garden_orientation="north"
        else:
            self.garden_area=0
            self.garden_orientation=""
    
    def sell_property(self):
        for rec in self:
            if rec.state == "canceled":
                raise UserError("canceled property cannot be sold")
                return False
            else : 
                rec.state = "sold"

    def cancel_property(self):
        for rec in self:
            if rec.state == "sold":
                raise UserError("sold property cannot be sold")
                return False
            else : 
                rec.state = "canceled"
    
    @api.constrains("selling_price","expected_price")
    def _check_selling_price(self):
        for rec in self:
            if not float_is_zero(rec.selling_price, precision_digits=2) and float_compare(rec.selling_price, rec.expected_price * 0.9,precision_digits=2):
                raise ValidationError("seeling price must be at 90`%` of the expected price")