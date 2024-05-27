from odoo import models, fields

class EmployeeInternal(models.Model):
    _inherit = "hr.employee"

    internal_code = fields.Char(string='Internal ID', required=True)
