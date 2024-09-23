# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64
from io import BytesIO
import json


class StudentForm(http.Controller):

    @http.route(['/student/form'], type='http', auth="public", website=True)

    def partner_form(self, **post):

        room_id = request.env['hostel.room.management'].sudo().search([('state', 'in', ['partial', 'empty'])])
        country_id = request.env['res.country'].sudo().search([])
        # country_id = request.env['res.country'].sudo().search([])
        # state_id = request.env['res.country.state'].sudo().search([])
        # state_id = request.env['res.country.state'].sudo().search([('country_id', '=', int(country_id))]) if post.get('country_id') else False
        return request.render("hostel_management.student_online_registration_form", {
            'room_id': room_id,
            'country_id': country_id
        })

    @http.route(['/student/form/submit'], type='http', auth="public", website=True)
    def customer_form_submit(self, **post):

        img = post.get('image')
        data = None
        if img:
            print("hlo")
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
        print("hloo123")
        # state = request.env['res.country.state'].sudo().browse(int(country_id))
        state = request.env['res.country.state'].sudo().select([('country_id','=',country_id)])
        print(state)
        return state

