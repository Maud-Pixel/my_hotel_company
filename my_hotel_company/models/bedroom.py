import time
from datetime import datetime
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

    _sql_constraints = [('number_pers_sup_0', 'CHECK(number_person>0)', 'Nombre de personnes supérieur à 0.')]
    room_id = fields.Many2many("bedroom.room","new_bedroom_id")
    number_room = fields.Char("number_of_room", compute="_compute_number",store=True, readonly=True)
    number_person = fields.Integer("Nb of persons", required=True, ) 
    date_start = fields.Datetime("Date start", required=True)
    date_end = fields.Datetime("Date end", required=True)
    cost_price = fields.Float("Price", digits="Bedroom Price")
    nights_price = fields.Float("Price of trip", compute="_compute_price", store=True, readonly=True )
    retail_price= fields.Monetary("Night Price")
    is_breakfast = fields.Boolean("Have breakfast", default=True)
    is_children = fields.Boolean("is there children", default=False) 
    contact_id = fields.Many2one('res.partner')
    currency_id = fields.Many2one("res.currency", string="Currency")
    category_id = fields.Many2one("bedroom.categ")
    date_of_booking = fields.Datetime("Date of booking", readonly=True, compute="_compute_date", store=True)
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
                    record.nights_price = round((record.cost_price * total_night),1)
                else:
                    record.nights_price = 0  
            else: 
                record.nights_price = 0
    @api.depends("room_id","number_room")
    def _compute_number(self):
        list_number =""
        for record in self:
            if record.room_id :
                for room in record.room_id:
                    list_number += str(room.number) 
                record.number_room = list_number

    @api.depends("date_of_booking","date_start","date_end")
    def _compute_date(self):
        for record in self:
            if record.date_start and record.date_end:
                record.date_of_booking = datetime.now()

    def find_bedroom(self):
        domain = ["|", "&",("number_room","ilike","Number of room"),("date_start", "ilike", "Date of start"), ("category_id.name", "ilike", "Category"), ("contact_id.name", "ilike", "client")]
        bedroom_search = self.search(domain)

class ResPartner(models.Model):
    _inherit = "res.partner"
    bedroom_id = fields.One2many("bedroom","contact_id", string="Booking")

class Room(models.Model):
    _name="bedroom.room"
    _description="Room to reserve for a trip"

    number = fields.Integer("Room's number", required=True)
    bedroom_id=fields.Many2many("bedroom","new_room_id")
    is_clean = fields.Boolean("Is clean", default=True)
    is_available = fields.Boolean("Is available", default=True)
    hotel_id = fields.Many2one("hotel")
    
class BookingState(models.Model):
    _name="booking.state"
    _order="sequence,name"

    name=fields.Char()
    sequence=fields.Integer()
    booking_status=fields.Selection([('booked',"Booked"),('deposit',"Deposit"),('allpayed','Allpayed')],'State',default="booked")

    @api.model
    def _default_status_booking(self):
        State = self.env['booking.state']
        return State.search([], limit=1)
