import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


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
                                     domain=[('state', '=', 'draft'), ('priority', 'in', (0, 1))])
    reason = fields.Text(string="Reason")
    cancel_date = fields.Date(string="Cancelling Date")

    def action_cancellation(self):
        # instead of self.cancel_date we can also use fields.Date.today()
        if self.appointment_id.booking_date == self.cancel_date:
            raise ValidationError(_("sorry, cancellation is not possible on the same day of booking"))
        else:
            self.appointment_id.state = 'cancelled'




