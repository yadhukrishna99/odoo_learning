import random
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CallDetails(models.Model):
    _name = "call.details"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Call Details"
    _order = 'id desc'

    contact = fields.Many2one('person.details', string="Name", ondelete="cascade")
    ref = fields.Char(string="Reference")
    call_reference = fields.Char(string="Call Reference")
    gender = fields.Selection(related='contact.gender')
    call_time = fields.Date(string='Call Time', default=fields.date.today())
    phnum = fields.Char(string='Contact Number', tracking=True)
    conversation = fields.Html()
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'High')], string="Priority")
    state = fields.Selection([
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')], string="Status", default='in_consultation', required=True)
    call_connector = fields.Many2one('res.users', string="Connector")
    active = fields.Boolean(string="Active", default=True)
    product_ids = fields.One2many('items.list', 'person_ids', string="Products Needed")
    sales_price = fields.Boolean(string="Sales price", default=False)
    tasks = fields.Many2one('contact.tasks', string="Tasks")
    progress = fields.Integer(string="Progress", compute='_compute_progress')
    duration = fields.Float(string="Duration")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    value = fields.Monetary(string='Value', compute='_compute_value')
    url = fields.Char(string="Url")

    @api.onchange('contact')
    def onchange_contact(self):
        self.phnum = self.contact.phnum
        self.ref = self.contact.ref

    def unlink(self):
        if self.state == 'in_consultation' or self.state == 'cancelled':
            return super().unlink()
        raise ValidationError(_("Cannot cancel the done calls"))

    @api.model
    def create(self, vals):
        vals['call_reference'] = self.env['ir.sequence'].next_by_code('call.detail')
        return super().create(vals)

    def write(self, vals):
        if not self.call_reference and not vals.get('call_reference'):
            vals['call_reference'] = self.env['ir.sequence'].next_by_code('call.detail')
        return super().write(vals)

    def object_button(self):
        if self.url:
            return {
              'type': 'ir.actions.act_url',
              'target': 'new',
              'url': self.url
            }
        raise ValidationError(_('Enter a url in the url field...'))

    def whatsapp_message(self):
        if not self.phnum:
            raise ValidationError(_('Please provide a phone number'))
        msg = 'Hii *%s*. Your call *%s* is fixed on *%s*.Please call me on time.' % (self.contact.name, self.call_reference, self.call_time)
        url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.phnum, msg)
        return{
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': url
        }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'cancelled':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            if rec.state == 'in_consultation':
                rec.state = 'done'
                return {
                    'effect': {
                        'fadeout': 'slow',
                        'message': 'Successfuly printed the python statement in log',
                        'type': 'rainbow_man',
                    }
                }

    def action_cancelled(self):
        action = self.env.ref('om_address_book.action_cancel_call').read()[0]
        return action

    def _compute_progress(self):
        for rec in self:
            if rec.state == 'in_consultation':
                rec.progress = 50
            elif rec.state == 'done':
                rec.progress = 100
            else:
                rec.progress = 0

    def name_get(self):
        return [(rec.id, "[%s] %s" % (rec.call_reference, rec.contact.name)) for rec in self]

    @api.depends('product_ids')
    def _compute_value(self):
        for rec in self:
            rec.value = 0
            for line in rec.product_ids:
                rec.value += line.sub_total


class ItemsList(models.Model):
    _name = "items.list"
    _description = "Item Lists"

    items = fields.Many2one('product.product', string="Items", required=True)
    qaty = fields.Integer(string="Quantity", default=1)
    price = fields.Float(related="items.list_price")
    person_ids = fields.Many2one('call.details', string="Person IDs")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    sub_total = fields.Monetary(string="Sub Total", compute='_compute_subtotal', currency_field='currency_id')

    @api.depends('qaty', 'price')
    def _compute_subtotal(self):
        for rec in self:
            rec.sub_total = rec.qaty * rec.price
