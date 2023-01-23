from odoo import api, fields, models


class SaleOrders(models.Model):
    _inherit = "res.groups"

    def get_application_groups(self, domain):
        print("Domain", domain)
        group_id = self.env.ref('stock.group_stock_picking_wave').id
        print(group_id)
        return super().get_application_groups(domain + [('id', '!=', group_id)])
