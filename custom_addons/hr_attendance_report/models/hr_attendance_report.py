from odoo import models, fields


class HrAttendanceReport(models.Model):
    _name = 'hr.attendance.report'
    _description = 'HR Attendance Report'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    check_in = fields.Datetime('Check In')
    check_out = fields.Datetime('Check Out')
    duration = fields.Float('Duration', compute='_compute_duration')

    def _compute_duration(self):
        if self.check_in and self.check_out:
            self.duration = (self.check_out - self.check_in).total_seconds() / 3600