import time
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class BookingArchive(models.AbstractModel):
    _name="base.archive"
    _description= "archive for booking"

    active = fields.Boolean(default=True)

    def do_archive(self):
        for record in self: 
            if record.active:
                record.active = not record.active

class Bedroom(models.Model):
    _name = "bedroom"
    _inherit = ["base.archive"]
    _description = "Bedroom of the hotel"

    _sql_constraints = [('number_uniq', 'UNIQUE (number_room)','Choisissez le numéro dans la liste')]
    number_room = fields.Selection([("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),("9","9"),("10","10")],
    required=True)
    number_person = fields.Integer("Nb of persons", required=True) 
    date_start = fields.Datetime("Date start", required=True)
    date_end = fields.Datetime("Date end", required=True)
    cost_price = fields.Float("Price", digits="Bedroom Price")
    nights_price = fields.Float("Price of trip", compute="_compute_price", store=True, readonly=True )
    retail_price= fields.Monetary("Night Price")
    is_clean = fields.Boolean("Is clean", default=True)
    is_breakfast = fields.Boolean("Have breakfast", default=True)
    is_children = fields.Boolean("is there children", default=False) 
    contact_id = fields.Many2one('res.partner')
    currency_id = fields.Many2one("res.currency", string="Currency")
    category_id = fields.Many2one("bedroom.categ")
    note = fields.Text("Note")

    @api.constrains("date_start")
    def _check_date_start(self):
        for record in self:
            if record.date_start and record.date_start < datetime.now():
                raise models.ValidationError("Error. The date must be in the futur")

    @api.constrains("date_end","date_start")
    def _check_date_end(self):
        for record in self:
            if record.date_end and record.date_end < record.date_start:
                raise models.ValidationError("Error. The date must be after the date start")

    @api.constrains("cost_price")
    def _check_cost_price(self):
        for record in self:
            if record.cost_price and record.cost_price < 0:
                raise models.ValidationError("Error.The price must be positif")
    
    @api.depends("nights_price", "date_start", "date_end", "cost_price")
    def _compute_price(self):
        for record in self:
            if record.date_start and record.date_end:
                number_day_start = record.date_start
                number_day_end = record.date_end
                total_night = (number_day_end - number_day_start).days
                if record.cost_price:
                    record.nights_price = record.cost_price * total_night
                else:
                    record.nights_price = 0  
            else: 
                record.nights_price = 0

    
class ResPartner(models.Model):
    _inherit = "res.partner"
    bedroom_id = fields.One2many("bedroom","contact_id", string="Booking")

