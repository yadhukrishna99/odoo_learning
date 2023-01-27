from odoo import api, fields, models


class ContactTasks(models.Model):
    _name = "contact.tasks"
    _description = "Contact Tasks"
    _rec_name = "task"
    _order = 'reference'

    task = fields.Char(string="Task")
    contact = fields.Many2one('person.details', string="Contact")
    record = fields.Reference(selection=[('call.details', 'Call Details')], string="Call Record")
    reference = fields.Integer(string="Reference", default=1)

    @api.model
    def name_create(self, name):
        return self.create({'task': name}).name_get()[0]
