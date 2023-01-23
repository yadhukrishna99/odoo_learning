# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    cancel_day = fields.Integer(string="Cancel Call", config_parameter='om_address_book.cancel_day')
