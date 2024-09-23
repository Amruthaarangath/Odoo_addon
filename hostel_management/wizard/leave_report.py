# -*- coding: utf-8 -*-

from odoo import fields, models, _
import io
import json
import xlsxwriter
from odoo.tools import date_utils
from odoo.exceptions import ValidationError


class StudentReport(models.TransientModel):
    _name = 'leave.report'
    _description = "Hostel management leave request Report"

    room_id = fields.Many2many("hostel.room.management", string="Room")
    student_id = fields.Many2many("hostel.student", string="Student")
    leave_date = fields.Date(string="leave date")
    arrival_date = fields.Date(string="Arrival date")

    def print_report(self):
        """function for print pdf report"""
        data = {
            'room_ids': self.room_id.ids,
            'student_ids': self.student_id.ids,
            'leave_date': self.leave_date,
            'arrival_date': self.arrival_date
        }
        return self.env.ref('hostel_management.action_report_leave_request_template').report_action(self, data=data)

    def print_excel_leave_report(self):
        """function for print excel report"""
        data = {
            'room_ids': self.room_id.ids,
            'student_ids': self.student_id.ids,
            'leave_date': self.leave_date,
            'arrival_date': self.arrival_date
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'leave.report',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Leave Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        student_ids = data.get('student_ids', [])
        room_ids = data.get('room_ids', [])
        leave_date = data.get('leave_date', None)
        arrival_date = data.get('arrival_date', None)

        query = """SELECT hs.name,hr.room_number,lr.leave_date , lr.arrival_date,lr.duration 
                FROM leave_request lr 
                JOIN hostel_room_management hr ON lr.room_id = hr.id 
                JOIN hostel_student hs ON lr.student_id = hs.id WHERE 1=1"""

        params = []
        if student_ids:
            query += """ AND hs.id IN %s"""
            params.append(tuple(student_ids))
        if room_ids:
            query += """ AND hr.id IN %s"""
            params.append(tuple(room_ids))
        if leave_date:
            query += """ AND lr.leave_date = %s"""
            params.append(leave_date)
        if arrival_date:
            query += """ AND lr.arrival_date <= %s"""
            params.append(arrival_date)

        self.env.cr.execute(query, params)
        report = self.env.cr.dictfetchall()

        if len(report) == 0:
            raise ValidationError(_("There is nothing to print"))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        title_style = workbook.add_format({'font_name': 'Times', 'font_size': 14, 'bold': True, 'align': 'center'})
        header_style = workbook.add_format(
            {'font_name': 'Times', 'bold': True, 'left': 2, 'bottom': 2, 'right': 2, 'top': 2,
             'align': 'center', 'color': '#FFFFFF', 'fg_color': '##7F00FF.'})
        name_style = workbook.add_format(
            {'font_name': 'Times', 'bold': True, 'left': 2, 'bottom': 2, 'right': 2, 'top': 2,
             'align': 'center', 'color': '#FFFFFF', 'fg_color': '#808080.'})
        column_style = workbook.add_format(
            {'font_name': 'Times', 'bold': False, 'left': 2, 'bottom': 2, 'right': 2, 'top': 2, 'align': 'center'})
        text_style = workbook.add_format(
            {'font_name': 'Times', 'left': 2, 'bottom': 2, 'right': 2, 'top': 2, 'align': 'left'})

        if len(report) == 1:
            for record in report:
                sheet.write('F5', 'Name', name_style)
                sheet.write('G5', record.get('name'))
                sheet.write('H5', 'Room', name_style)
                sheet.write('I5', record.get('room_number'))
                sheet.write('J5', 'Start Date', name_style)
                sheet.write('K5', str(record.get('leave_date')))

                sheet.merge_range('E2:K2', 'EXCEL LEAVE REPORT', title_style)
                sheet.write('G7', 'No.', header_style)
                sheet.write('G8', 1, column_style)
                sheet.write('H7', 'End Date', header_style)
                sheet.write('H8', str(record.get('arrival_date')), column_style)
                sheet.write('I7', 'Duration', header_style)
                sheet.write('I8', record.get('duration'), column_style)

        if len(report) > 1:
            res = [sub['room_number'] for sub in report]
            start_date = [sub['leave_date'] for sub in report]
            if len(set(res)) == 1:
                for record in report:
                    sheet.write('I5', 'Room', name_style)
                    sheet.write('J5', record.get('room_number'))

                    sheet.merge_range('G3:K3', 'EXCEL LEAVE REPORT', title_style)
                    sheet.write('G7', 'No.', header_style)
                    sheet.write('H7', 'Student', header_style)
                    sheet.write('I7', 'Start Date', header_style)
                    sheet.write('J7', 'Leave Date', header_style)
                    sheet.write('K7', 'Duration', header_style)

                    number = 1

                    for r, data in enumerate(report, start=6):
                        data.pop("room_number", None)
                        for col, (key, value) in enumerate(data.items()):
                            val = str(value)
                            sheet.write(r + 1, col + 7, val, column_style)
                        sheet.write(r + 1, 6, number, text_style)
                        r += 6
                        number += 1

            elif len(set(start_date)) == 1:
                for record in report:
                    sheet.write('G5', 'Start Date', name_style)
                    sheet.write('H5', str(record.get('leave_date')))

                    sheet.merge_range('G3:K3', 'EXCEL LEAVE REPORT', title_style)
                    sheet.write('G7', 'No.', header_style)
                    sheet.write('H7', 'Student', header_style)
                    sheet.write('I7', 'Room', header_style)
                    sheet.write('J7', 'Arrival Date', header_style)
                    sheet.write('K7', 'Duration', header_style)

                number = 1

                for r, data in enumerate(report, start=6):
                    data.pop("leave_date", None)
                    for col, (key, value) in enumerate(data.items()):
                        val = str(value)
                        sheet.write(r + 1, col + 7, val, column_style)
                    sheet.write(r + 1, 6, number, text_style)
                    r += 6
                    number += 1

            else:
                sheet.merge_range('H5:K5', 'EXCEL LEAVE REPORT', title_style)
                sheet.write('G7', 'No.', header_style)
                sheet.write('H7', 'Name', header_style)
                sheet.write('I7', 'Room', header_style)
                sheet.write('J7', 'Start Date', header_style)
                sheet.write('K7', 'Leave Date', header_style)
                sheet.write('L7', 'Duration', header_style)

                number = 1

                for r, data in enumerate(report, start=6):
                    for col, (key, value) in enumerate(data.items()):
                        val = str(value)
                        sheet.write(r + 1, col + 7, val, column_style)
                    sheet.write(r + 1, 6, number, text_style)
                    r += 6
                    number += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
