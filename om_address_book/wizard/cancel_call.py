import datetime

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


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
        if self.contact_id.call_time == self.cancel_date:
            raise ValidationError(_("Cannot cancel the call record on the same date the call record created!!"))
        elif self.contact_id.state == 'in_consultation':
            self.contact_id.state = 'cancelled'


