from odoo import http, exceptions, models
from odoo.http import request

class Main(http.Controller):
    @http.route('/hotel_company/booking', type="http", auth="none")
    def reserve(self):
        reservations = request.env["bedroom"].sudo().search([])
        html_result = "<html><body><ul>"
        for reservation in reservations:
            html_result +="<li> Chambre n°%s au nom de %s</li>" % (reservation.room_id, reservation.contact_id.name)
        html_result += "</ul></body></html>"
        return html_result

    @http.route('/hotel_company/booking/json', type="json", auth="none")
    def reserve_json(self):
        json_reservations = request.env["bedroom"].sudo().search([])
        return json_reservations.read(["room_id"])
    
    @http.route('/hotel_company/all_booking', type="http", auth="none")
    def all_reservations(self):
        reservations = request.env["bedroom"].sudo().search([])
        html_result = "<html><body><ul>"
        for reservation in reservation:
            html_result += "<li> %s </li>" %bedroom.room_id
        html_result = "</ul></body></html>"
        return html_result
    
    @http.route('/hotel_company/all_booking/mark_my_count', type="http", auth="none")
    def reserve_mark_mine(self):
        reservations = request.env["bedroom"].sudo().search([])
        html_result = "<html><body><ul>"
        for reservation in reservations:
            if request.env.user.partner_id.id in reservation.contact_id.ids:
                html_result +="<li><b> %s</b></li>" %reservation.room_id
            else:
                html_result +="<li>%s</li>" %reservation.room_id
        html_result +="</ul></body></html>"
        return html_result 

    @http.route('/hotel_company/all_booking/my_count', type="http", auth="base.group_user") 
    def reserve_mine(self):
        reservations = request.env["bedroom"].search([('contact_id','in', request.env.user.partner_id.ids),])
        html_result = "<html><body><ul>"
        for reservation in reservations:
            html_result += "<li> %s </li>" %reservation.room_id
        html_result += "</ul></body></html>"  
        return html_result
    
    @http.route("/hotel_company/booking_details", type="http", auth="none")
    def reserve_details(self,room_id=4):
        record = request.env["bedroom"].sudo().browse(room_id)
        return u'<html><body><h1> %s' %(record.contact_id)
    
    @http.route("/hotel_company/booking_details/<model('bedroom'):room>", type="http", auth="none")
    def reserve_details_path(self,room):
        return self.reserve_details(room.id)
