# -*- coding: utf-8 -*-
# from odoo import http


# class OmPracticeInheritance(http.Controller):
#     @http.route('/om_practice_inheritance/om_practice_inheritance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/om_practice_inheritance/om_practice_inheritance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('om_practice_inheritance.listing', {
#             'root': '/om_practice_inheritance/om_practice_inheritance',
#             'objects': http.request.env['om_practice_inheritance.om_practice_inheritance'].search([]),
#         })

#     @http.route('/om_practice_inheritance/om_practice_inheritance/objects/<model("om_practice_inheritance.om_practice_inheritance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('om_practice_inheritance.object', {
#             'object': obj
#         })
