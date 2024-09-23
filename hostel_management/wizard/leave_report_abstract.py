from odoo import models, api, _
from odoo.exceptions import ValidationError


class ReportFromStudent(models.AbstractModel):
    _name = 'report.hostel_management.report_leave_request'

    @api.model
    def _get_report_values(self, docids, data=None):
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
            print(params)
        if room_ids:
            query += """ AND hr.id IN %s"""
            params.append(tuple(room_ids))
        if leave_date:
            query += """ AND lr.leave_date >= %s"""
            params.append(leave_date)
        if arrival_date:
            query += """ AND lr.arrival_date <= %s"""
            params.append(arrival_date)

        self.env.cr.execute(query, params)
        report = self.env.cr.dictfetchall()
        if len(report) == 0:
            raise ValidationError(_("There is nothing to print"))
        else:
            return {
                'doc_model': 'leave.request',
                'report': report,
            }
