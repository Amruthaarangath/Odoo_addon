from odoo import models, api, _
from odoo.exceptions import ValidationError


class ReportFromStudent(models.AbstractModel):
    _name = 'report.hostel_management.report_student'

    @api.model
    def _get_report_values(self, docids, data=None):
        student_ids = data.get('student_ids', [])
        room_ids = data.get('room_ids', [])

        query = """SELECT hs.room_id, hs.name, hr.pending_amount, hr.room_number, ri.state
                    FROM hostel_student hs
                    JOIN hostel_room_management hr ON hs.room_id = hr.id
                    join account_move ri ON hr.id = ri.id
                    WHERE 1=1 """

        params = []
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
        else:
            return {
                'doc_model': 'hostel.student',
                'report': report,
            }
