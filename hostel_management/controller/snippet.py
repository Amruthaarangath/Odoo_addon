from odoo import http
from odoo.http import request


class RoomSnippet(http.Controller):
   @http.route('/room', type='json', auth='public')
   def room_list(self):
       room = request.env['hostel.room.management'].sudo().search([])
       rooms = room.filtered(lambda r: r.state != 'full')
       data = rooms.read(['id','room_number','image'])
       return data


   @http.route(['/room_details/<int:room_id>'], type='http', auth="public", website=True)
   def room_details(self, room_id):
       print("dfg")
       room_id = request.env['hostel.room.management'].sudo().browse(room_id)
       values = {
           'room_id': room_id
       }
       return request.render('hostel_management.room_details', values)
