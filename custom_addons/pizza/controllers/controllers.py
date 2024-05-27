# -*- coding: utf-8 -*-
# from odoo import http


# class Pizza(http.Controller):
#     @http.route('/pizza/pizza', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pizza/pizza/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pizza.listing', {
#             'root': '/pizza/pizza',
#             'objects': http.request.env['pizza.pizza'].search([]),
#         })

#     @http.route('/pizza/pizza/objects/<model("pizza.pizza"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pizza.object', {
#             'object': obj
#         })

