from odoo import api, fields, models, _


class PatientTags(models.Model):
    _name = "patient.tags"
    _description = "Patient Tags"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")
    sequence = fields.Integer(string="Sequence")

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)", self.name)
        default['sequence'] = 10
        return super().copy(default)

    _sql_constraints = [
        ('uniq_tag_name', 'unique (name)', "Tag name already exists !"),
        ('check_sequence', 'check (sequence > 0)', 'Sequence should be non zero and non negative')
    ]
