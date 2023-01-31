from odoo import api, fields, models


class SaleOrders(models.Model):
    _inherit = "sale.order"

    confirmed_user_id = fields.Many2one('res.users', string="Confirmed User")
    cancelled_user_id = fields.Many2one('res.users', string="Cancelled User")

    def action_confirm(self):
        super().action_confirm()
        print("sucess.................................")
        self.confirmed_user_id = self.env.user.id
        self.cancelled_user_id = None

    def action_cancel(self):
        super().action_cancel()
        print("Cancelled..........................")
        self.confirmed_user_id = None
        self.cancelled_user_id = self.env.user.id

    def action_draft(self):
        super().action_draft()
        self.cancelled_user_id = None

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals['so_confirmed_user_id'] = self.confirmed_user_id.id
        return invoice_vals



