from odoo import models, fields, api

class hotel(models.Model):
    _name = "hotel"
    _description = "Model of my company's hotels"

    name=fields.Char("hotel", required=True)
    address= fields.Char("address")
    contact_id=fields.Many2many("res.partner","new_hotel_id")
    room_id=fields.One2many("bedroom.room","hotel_id")