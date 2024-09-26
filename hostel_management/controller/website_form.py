# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64



class StudentForm(http.Controller):

    @http.route(['/student/form'], type='http', auth="public", website=True)
    def partner_form(self, **post):
        room_id = request.env['hostel.room.management'].sudo().search([])
        room = room_id.filtered(lambda r:r.state != 'full')

        country_id = request.env['res.country'].sudo().search([])
        return request.render("hostel_management.student_online_registration_form", {
            'room_id': room,
            'country_id': country_id
        })

    @http.route(['/abc'], type='http', auth="public", website=True)
    def abc(self, **post):
        country_id = request.env['res.country'].sudo().search([])
        return "hiiii"

    @http.route(['/student/form/submit'], type='http', auth="public", website=True)
    def customer_form_submit(self, **post):

        img = post.get('image')
        data = None
        if img:
            image = img.read()
            data = base64.b64encode(image).decode('utf-8')
        student = request.env['hostel.student'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'dob': post.get('dob'),
            'room_id': post.get('Room'),
            'street': post.get('street'),
            'street2': post.get('street2'),
            'city': post.get('city'),
            'country_id': post.get('country'),
            'state_id': post.get('state'),
            'zip': post.get('zip'),
            'image': data,

        })
        vals = {
            'student': student,
        }
        return request.render("hostel_management.student_form_success", vals)

    @http.route('/filtered_states', type="json", auth='public')
    def filtered_states(self, country_id):
        """function to dynamically filter states based on selected country"""
        state = request.env['res.country.state'].sudo().search_read([('country_id', '=', int(country_id))], [
                                                                                                        'id',
                                                                                                        'name'])
        return state
