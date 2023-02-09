from odoo import models, fields

class PropertyTypeModel(models.Model):
    _name="estate.property.type"
    _description="hold the type of the property"

    
    name = fields.Char(required=True)
    property_ids = fields