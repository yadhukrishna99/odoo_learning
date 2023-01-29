import random
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Appointments"
    _order = 'id desc'
    _rec_name = 'appointment_id'
    # since there is no name field in this model, we are adding the _rec_name here to take a specific field as name

    patient_id = fields.Many2one('hospital.patient', string="Patient", ondelete="restrict", tracking=1)
    gender = fields.Selection(related="patient_id.gender")
    # By default related fields are readonly...to change to editable write (readonly=False)
    appointment_time = fields.Datetime(string="Appointment Time", tracking=4)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today,
                               help="Date of booking the appointment")
    #   similarly for Datetime field (default=fields.Datetime.now) is the format
    ref = fields.Char(string='Reference', tracking=True)
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority", tracking=3)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')], string="State", default='draft', tracking=True, required=True)
    doctor_id = fields.Many2one('res.users', string="Doctor", tracking=2)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lists', 'appointment_id', string="Pharmacy lines")
    show_sales_price = fields.Boolean(string="Show sales price", default=True)
    appointment_id = fields.Char()
    operation = fields.Many2one('hospital.operation', string="Operation")
    progress = fields.Integer(string="Progress", compute='_compute_progress')
    duration = fields.Float(string="Duration", tracking=101)
    url = fields.Char(string="url")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    total_value = fields.Monetary(string="Total value", compute='_compute_total_value')

    @api.model
    def create(self, val):
        val['appointment_id'] = self.env['ir.sequence'].next_by_code('patient.appointment')
        return super().create(val)

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError(_('You can delete records only in draft state'))
        return super().unlink()

    @api.onchange("patient_id")
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def object_button(self):
        # url action
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': self.url
        }

    def action_whatsapp_msg(self):
        if not self.patient_id.phone:
            raise ValidationError(_('Phone number is not available for this patient.'))
        message = 'Hii *%s*. Your appointment number is *%s* fixed on date:*%s*. Come to India on the next flight.' % (self.patient_id.name, self.appointment_id, self.appointment_time)
        whatsapp_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.patient_id.phone, message)
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_url
        }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Successfully completed an appointment',
                    'type': 'rainbow_man',
                }
            }

    def action_draft(self):
        for rec in self:
            if rec.state == 'cancelled':
                rec.state = 'draft'

    # def action_cancelled(self):
    #     for rec in self:
    #         rec.state = 'cancelled'

# This function is for launching the wizard from the object button
    def action_cancelled(self):
        for rec in self:
            if rec.state == 'draft' or rec.state == 'in_consultation':
                action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
                return action

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = random.randrange(0, 25)
            elif rec.state == 'in_consultation':
                progress = random.randrange(25, 75)
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress

    @api.depends('pharmacy_line_ids')
    def _compute_total_value(self):
        for rec in self:
            rec.total_value = 0
            for line in rec.pharmacy_line_ids:
                rec.total_value += line.price_subtotal


class AppointmentPharmacyLists(models.Model):
    _name = "appointment.pharmacy.lists"
    _description = "Pharmacy Lists"

    product_id = fields.Many2one('product.product', required=True)
    qty = fields.Integer(string="Quantity", default=1)
    price_unit = fields.Float(related="product_id.list_price")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointments")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    price_subtotal = fields.Monetary(string="Subtotal", compute='_compute_price_subtotal')

    @api.depends('price_unit', 'qty')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.qty * rec.price_unit
