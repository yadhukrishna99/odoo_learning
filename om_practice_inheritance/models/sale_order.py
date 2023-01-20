# from odoo import models, fields, api
#
#
# class SalesOrder(models.Model):
#     _inherit = 'sale.order'
#
#     cancelled_user_id = fields.Many2one('res.users', string="Cancelled User")
#
#     def action_cancel(self):
#         super().action_cancel()
#         print("Cancelled..........................")
#         self.confirmed_user_id = None
#         self.cancelled_user_id = self.env.user.id
#
#     def action_draft(self):
#         super().action_draft()
#         self.cancelled_user_id = None




