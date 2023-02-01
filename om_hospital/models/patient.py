from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patients"

    name = fields.Char(string='Name', tracking=True)
    dob = fields.Date(string="Date Of Birth")
    ref = fields.Char(string='Reference', tracking=True)
    age = fields.Integer(string="Age", compute="_compute_age", inverse="inverse_compute_age", store=True, tracking=True)
# search="search_age" is used if we want to search a computed field, but here i already stored my field in the database
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tags', 'hospital_patient_tags_rel', 'patient_id', 'tag_id', string="Tags")
    appointment_count = fields.Integer(string="Appointment count", compute="_compute_appointment_count")
    parent = fields.Char(string="Parent Name")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string="Marital Status")
    partner = fields.Char(string="Partner Name")
    operation_records = fields.One2many('hospital.operation', 'patient', string="Operation Record")
    is_birthday = fields.Boolean(string="Birthday", compute="_compute_is_birthday")
    phone = fields.Char(string="Phone number")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")
    operation_count = fields.Integer(string="Operation Count", compute='_compute_operation_count')

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.name)])

    # this is a compute_method using read_group method
    # @api.depends('appointment_ids')
    # def _compute_appointment_count(self):
    #         print("...self", self)
    #         appointment_group = self.env['hospital.appointment'].read_group(domain=[('state', '=', 'done')],
    #                                                                     fields=['patient_id'], groupby=['patient_id'])
    #         for app in appointment_group:
    #             print("...app", app)
    #             patient_id = app.get('patient_id')[0]
    #             patient_rec = self.browse(patient_id)
    #             print("...rec", patient_rec)
    #             patient_rec.appointment_count = app['patient_id_count']
    #             self -= patient_rec
    #         self.appointment_count = 0

    @api.depends('operation_records')
    def _compute_operation_count(self):
        for rec in self:
            rec.operation_count = self.env['hospital.operation'].search_count([('patient', '=', rec.id)])

    @api.constrains('dob')
    def check_dob(self):
        if self.dob and self.dob > fields.date.today():
            raise ValidationError(_("Invalid date of birth"))

    @api.ondelete(at_uninstall=False)
    def check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("You cannot delete patient with appointment"))

    # This is to overwrite the create function of the odoo
    @api.model
    def create(self, val):
        print(val)
        val['ref'] = self.env['ir.sequence'].next_by_code('hospital.patients')
        print("Created Record and going to be saved in the database", val)
        return super().create(val)

    def write(self, val):
        for rec in self:
            if not rec.ref and not val.get('ref'):
                val['ref'] = self.env['ir.sequence'].next_by_code('hospital.patients')
            print("Trigerred write method", val)
        return super().write(val)

    @api.depends('dob')
    # the above api line is for sudden execution of the age value
    def _compute_age(self):
        for rec in self:
            if rec.dob:
                today = date.today()
                rec.age = today.year - rec.dob.year
            else:
                rec.age = 0

    @api.depends('age')
    def inverse_compute_age(self):
        for rec in self:
            today = date.today()
            rec.dob = today - relativedelta.relativedelta(years=rec.age)

    # def search_age(self, operator, value):
    # here self is a model, since we are searching for a match in a model, so we cannot iterate using a for loop
    #         print('value...', value)
    #         date_of_birth = date.today() - relativedelta.relativedelta(years=value)
    #         start_of_year = date_of_birth.replace(day=1, month=1)
    #         end_of_year = date_of_birth.replace(day=31, month=12)
    #         print('start...', start_of_year)
    #         print('end...', end_of_year)
    #         return [('dob', '>=', start_of_year), ('dob', '<=', end_of_year)]

    @api.depends('dob')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.dob:
                today = date.today()
                if today.day == rec.dob.day and today.month == rec.dob.month:
                    is_birthday = True
        rec.is_birthday = is_birthday

    def name_get(self):
        return [(rec.id, "[%s] %s" % (rec.ref, rec.name)) for rec in self]

    def action_test(self):
        print("Clicked...")
        return

    def action_view_appointments(self):
        print(self.id)
        return {
            'name': _('Appointments'),
            'res_model': 'hospital.appointment',
            'view_mode': 'tree,form,calendar',
            'context': {'default_patient_id': self.id},
            'domain': [('patient_id', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',
        }

    def action_view_operations(self):
        return {
            'name': _('Operations'),
            'res_model': 'hospital.operation',
            'view_mode': 'tree,form',
            'context': {'default_patient': self.id},
            'domain': [('patient', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',
        }


