from odoo import models, fields, api
from odoo.tools import date_utils

class TimesheetXml(models.Model):
    _name = 'timesheet.xml'
    _description = 'Timesheet XML converter'

    name = fields.Char('Name')
    #info = fields.Char('List of users extracted')                       # M2M lista di user nel report hr.employee - computed?

    #user = fields.Many2one('hr.employee', string='Reporter')                                      # M2O user che ha creato il report - hr.employee?
    date_report_start = fields.Datetime('Start of the time frame')
    date_report_end = fields.Datetime('End of the time frame')
    #employee_ids = fields.Many2many('hr.employee', string='List of Employees in the Report')            # Lista degli employees nel singolo report
    #timesheet_ids = fields.Many2many('account.analytic.line', string='List of Lines in the Report')     # Lista degli employees nel singolo report
