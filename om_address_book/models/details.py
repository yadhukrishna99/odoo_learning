from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta

class PersonDetails(models.Model):
    _name = "person.details"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Person Details"

    name = fields.Char(string='Name', tracking=True)
    ref = fields.Char(string="Reference")
    dob = fields.Date(string='Date of birth', tracking=True)
    age = fields.Integer(string="Age", compute='_compute_age', inverse='_compute_dob', tracking=True, search='search_age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True)
    address = fields.Char(string='Address', tracking=True)
    city = fields.Char(string='City', tracking=True)
    phnum = fields.Char(string='Contact Number', tracking=True)
    email = fields.Char(string='Email id', tracking=True)
    active = fields.Boolean(string="Active", default=True)
    call_ids = fields.One2many('call.details', 'contact', string="Call details")
    image = fields.Image(string="Photo")
    tags = fields.Many2many('contact.tags', 'contact_tags_rel', 'contact_id', 'tag_id', string="Tags")
    call_count = fields.Integer(string="call appointment", compute='_compute_call', store=True)
    parent = fields.Char(string="Parent name")
    marital_status = fields.Selection([('single', 'Single'), ('married', 'Married')], string="Marital status")
    partner = fields.Char(string="Partner")

    @api.constrains('dob')
    def check_dob(self):
        if self.dob and self.dob > fields.date.today():
            raise ValidationError(_("Invalid dob"))

    @api.ondelete(at_uninstall=False)
    def check_call(self):
        for rec in self:
            if rec.call_ids:
                raise ValidationError(_("You cannot delete this record, because of present call appointment"))

    @api.model
    def create(self, vals):
        vals['phnum'] = '**********'
        vals['email'] = '****@gmail.com'
        vals['ref'] = self.env['ir.sequence'].next_by_code('contact.book')
        return super().create(vals)

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('contact.book')
        return super().write(vals)

    def name_get(self):
        print(self)
        return[(rec.id, "%s [%s]" % (rec.name, rec.ref))for rec in self]

    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            if rec.dob:
                today = date.today()
                rec.age = today.year - rec.dob.year
            else:
                rec.age = 0

    @api.depends('age')
    def _compute_dob(self):
        for rec in self:
            dob = date.today() - relativedelta.relativedelta(years=rec.age)
            rec.dob = dob.replace(month=rec.dob.month, day=rec.dob.day)

    @api.depends('call_ids')
    def _compute_call(self):
        for rec in self:
            rec.call_count = self.env['call.details'].search_count([('contact', '=', rec.name)])

    def search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start = date_of_birth.replace(day=1, month=1)
        end = date_of_birth.replace(day=31, month=12)
        return [('dob', '>=', start), ('dob', '<=', end)]

    def action_click(self):
        return
