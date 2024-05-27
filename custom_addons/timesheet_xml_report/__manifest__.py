{
    'name': "Timesheet to Xml Export",
    'summary': "Extracts timesheets in a Zucchetti-XML format.",
    'description': """
    Extracts timesheets from a selection of date interval and number of employees, in a XML format following Zucchetti's standard.
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Human Resources',
    'version': '0.1',
    'depends': ['base', 'project_timesheet_holidays', 'hr_timesheet'],
    'data': [
        'security/ir.model.access.csv',
        'views/timesheet_xml_report_views.xml',
        'views/timesheet_xml_report_menus.xml',
        'views/employee_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True
}
