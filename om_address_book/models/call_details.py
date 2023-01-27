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
        print("Button Clicked!!")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Successfuly printed the python statement in log',
                'type': 'rainbow_man',
            }
        }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'cancelled':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            if rec.state == 'in_consultation':
                rec.state = 'done'

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


class ItemsList(models.Model):
    _name = "items.list"
    _description = "Item Lists"

    items = fields.Many2one('product.product', string="Items", required=True)
    qaty = fields.Integer(string="Quantity", default=1)
    price = fields.Float(related="items.list_price")
    person_ids = fields.Many2one('call.details', string="Person IDs")
