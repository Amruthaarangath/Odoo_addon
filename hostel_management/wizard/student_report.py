# -*- coding: utf-8 -*-

from odoo import fields, models, _
import io
import json
import xlsxwriter
from odoo.tools import date_utils
from odoo.exceptions import ValidationError


class StudentReport(models.TransientModel):
    _name = 'student.report'
    _description = "Hostel management Student Report"

    room_ids = fields.Many2many("hostel.room.management", string="Room")
    student_ids = fields.Many2many("hostel.student", string="Student")

    def print_report(self):
        """function for print pdf student report"""
        data = {
            'room_ids': self.room_ids.ids,
            'student_ids': self.student_ids.ids
        }
        return self.env.ref('hostel_management.action_report_student_template').report_action(self, data=data)

    def print_student_report_excel(self):
        """function for print excel report"""
        data = {
            'room_ids': self.room_ids.ids,
            'student_ids': self.student_ids.ids,
        }

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'student.report',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Student Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):

        student_ids = data.get('student_ids')
        room_ids = data.get('room_ids')
        params = []

        query = """SELECT hs.name, hr.pending_amount, hr.room_number, ri.state
                                    FROM hostel_student hs
                                    JOIN hostel_room_management hr ON hs.room_id = hr.id
                                    join account_move ri ON hr.id = ri.id
                                    WHERE 1=1 """

        if room_ids:
            query += """AND hr.id IN %s"""
            params.append(tuple(room_ids))
        if student_ids:
            query += """ AND hs.room_id IN %s"""
            params.append(tuple(student_ids))

        self.env.cr.execute(query, params)
        report = self.env.cr.dictfetchall()

        if len(report) == 0:
            raise ValidationError(_("There is nothing to print"))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        title_style = workbook.add_format({'font_name': 'Times', 'font_size': 14, 'bold': True, 'align': 'center'})
        header_style = workbook.add_format(
            {'font_name': 'Times', 'bold': True, 'left': 2, 'bottom': 2, 'right': 2, 'top': 2, 'align': 'center',
             'color': '#FFFFFF', 'fg_color': '##7F00FF.'})
        name_style = workbook.add_format(
            {'font_name': 'Times', 'bold': True, 'left': 2, 'bottom': 2, 'right': 2, 'top': 2, 'align': 'center',
             'color': '#FFFFFF', 'fg_color': '#808080.'})
        column_style = workbook.add_format(
            {'font_name': 'Times', 'bold': False, 'left': 2, 'bottom': 2, 'right': 2, 'top': 2, 'align': 'center'})
        text_style = workbook.add_format(
            {'font_name': 'Times', 'left': 2, 'bottom': 2, 'right': 2, 'top': 2, 'align': 'left'})

        if len(report) == 1:
            print("one")
            for record in report:
                sheet.write('F5', 'Name', name_style)
                sheet.write('G5', record.get('name'))
                sheet.write('I5', 'Room', name_style)
                sheet.write('J5', record.get('room_number'))

                sheet.merge_range('E3:K3', 'EXCEL STUDENT REPORT', title_style)
                sheet.write('G7', 'No.', header_style)
                sheet.write('G8', 1, column_style)
                sheet.write('H7', 'Amount', header_style)
                sheet.write('H8', record.get('pending_amount'), column_style)
                sheet.write('I7', 'State', header_style)
                sheet.write('I8', record.get('state'), column_style)

        if len(report) > 1:
            res = [sub['room_number'] for sub in report]
            print(res)
            if len(set(res)) == 1:
                for record in report:
                    print("hii")
                    sheet.write('I5', 'Room', name_style)
                    sheet.write('J5', record.get('room_number'))

                    sheet.merge_range('E3:K3', 'EXCEL STUDENT REPORT', title_style)
                    sheet.write('G7', 'No.', header_style)
                    sheet.write('H7', 'Student', header_style)
                    sheet.write('I7', 'Amount', header_style)
                    sheet.write('J7', 'State', header_style)

                    number = 1

                    for r, data in enumerate(report, start=6):
                        data.pop("room_number", None)
                        for col, (key, value) in enumerate(data.items()):
                            print(data.items())
                            sheet.write(r + 1, col + 7, value, column_style)
                        sheet.write(r + 1, 6, number, text_style)
                        r += 6
                        number += 1

            else:
                sheet.merge_range('G4:K4', 'EXCEL STUDENT REPORT', title_style)
                sheet.write('G7', 'No.', header_style)
                sheet.write('H7', 'Student', header_style)
                sheet.write('I7', 'Amount', header_style)
                sheet.write('J7', 'Room', header_style)
                sheet.write('K7', 'State', header_style)

                number = 1

                for r, data in enumerate(report, start=6):
                    for col, (key, value) in enumerate(data.items()):
                        sheet.write(r + 1, col + 7, value, column_style)
                    sheet.write(r + 1, 6, number, text_style)
                    r += 6
                    number += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
