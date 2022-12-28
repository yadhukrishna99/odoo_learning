from odoo import api, fields, models

class PersonDetails(models.Model):
    _name = "person.details"
    _description = "Person Details"

    name = fields.Char(string='Name')
    age = fields.Integer(string="Age")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    address = fields.Char(string='Address')
    city = fields.Char(string='City')
    phnum = fields.Char(string='Contact Number')
    email = fields.Char(string='Email id')
    active = fields.Boolean(string="Active",default=True)