from odoo import models, fields

class PropertyTypeModel(models.Model):
    _name="estate.property.tag"
    _description="hold the tag of the property"

    name = fields.Char(required=True)
    