import datetime

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta
from datetime import date


class CancelCallWizard(models.TransientModel):
    _name = "cancel.call.wizard"
    _description = "Cancel Call Wizard"

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['cancel_date'] = datetime.date.today()
        print(self.env.context)
        if self.env.context.get('active_id'):
            res['contact_id'] = self.env.context.get('active_id')
        print(res)
        return res

    contact_id = fields.Many2one('call.details', string="Contact Call ID",
                                 domain=[('state', '=', 'in_consultation')])
    reason = fields.Text(string="Reason")
    cancel_date = fields.Date(string="Cancel Date")

    def action_cancellation(self):
        cancel_day = self.env['ir.config_parameter'].get_param('om_address_book.cancel_day')
        allowed_day = self.contact_id.call_time + relativedelta.relativedelta(days=int(cancel_day))
        if self.contact_id.call_time == self.cancel_date:
            raise ValidationError(_("Cannot cancel the call record on the same date the call record created!!"))
        elif date.today() < allowed_day:
            raise ValidationError(_("Cannot cancel the call record before 10 days of recording the call call!!"))
        elif self.contact_id.state == 'in_consultation':
            self.contact_id.state = 'cancelled'
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }


