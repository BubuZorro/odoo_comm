# -*- coding: utf-8 -*-
# from odoo import http


# class Pippo(http.Controller):
#     @http.route('/pippo/pippo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pippo/pippo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pippo.listing', {
#             'root': '/pippo/pippo',
#             'objects': http.request.env['pippo.pippo'].search([]),
#         })

#     @http.route('/pippo/pippo/objects/<model("pippo.pippo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pippo.object', {
#             'object': obj
#         })

