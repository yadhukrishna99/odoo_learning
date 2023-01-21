import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta
from datetime import date



class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields):
        print(fields)
        res = super().default_get(fields)
        res['cancel_date'] = datetime.date.today()
        print("........", self.env.context)
        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment ID",
                                     domain=['|', ('state', '=', 'draft'), ('state', '=', 'in_consultation'),
                                             ('priority', '!=', '3')])
    reason = fields.Text(string="Reason")
    cancel_date = fields.Date(string="Cancelling Date")

    def action_cancellation(self):
        # instead of self.cancel_date we can also use fields.Date.today()
        allowed_days = self.env['ir.config_parameter'].get_param('om_hospital.cancel_days')
        cancel_day_before = self.appointment_id.appointment_time.date() - relativedelta.relativedelta(days=int(allowed_days))
        print("cancel...", cancel_day_before)
        if self.appointment_id.booking_date == self.cancel_date:
            raise ValidationError(_("sorry, cancellation is not possible in the same date of booking"))
        elif date.today() > cancel_day_before:
            raise ValidationError(_("Appointment time is less than 5days from today, you cannot cancel this booking now"))
        else:
            self.appointment_id.state = 'cancelled'




