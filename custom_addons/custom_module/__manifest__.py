{
    'name': "CustomModule",
    'summary': "A brief description of your module.",
    'description': """
        A longer description of your module.
    """,
    'author': "Your Name",
    'website': "http://www.example.com",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/custom_module_view.xml',
        # 'views/templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True
}
