from odoo import models, fields ,api
from odoo.exceptions import UserError
from datetime import datetime, timedelta
class PropertyTypeModel(models.Model):
    _name="estate.property.offer"
    _description="hold the offer to a property"

    price = fields.Float()
    status = fields.Selection(
        string="status",
        selection=[('accepeted','Accepted'),('refused','Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner',string="offerer", required=True)
    property_id = fields.Many2one('estate.property',string="property", required=True)
    
    _sql_constraints = [
        ('check_price','CHECK(price > 0)','the price should be a positive value'),
        
    ]
    
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for rec in self :
            rec.date_deadline = datetime.now()
    def _inverse_deadline(self):
        for rec in self:
            date = fields.Date.from_string(rec.date_deadline)
            rec.validity = 10
    
    def accept_offer(self):
    
        for rec in self:
                for offer in rec.property_id.offer_ids :
                    if offer.status == "accepeted":
                        raise UserError("A offer is already accepted for this property")
                        return False
                else:
                    rec.status = "accepeted"
                    rec.property_id.selling_price = rec.price
                    rec.property_id.buyer_id = rec.partner_id
        return True         

    def refuse_offer(self):
        for rec in self:
                rec.status = "refused"
                rec.property_id.selling_price = 0
                rec.property_id.buyer_id = None
                
        return True       
