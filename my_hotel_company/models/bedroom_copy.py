from odoo import fields, models, api

class BedroomCopy(models.Model):
    _name = "bedroom.copy"
    _inherit = "bedroom"
    _description = "Bedroom copy just for an example"