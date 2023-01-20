from odoo import api, fields, models, _


class ContactTags(models.Model):
    _name = "contact.tags"
    _description = "Contact Tags"
    _rec_name = 'tag_name'

    tag_name = fields.Char(string="Tag name")
    active = fields.Boolean(string="Active", default=True, copy=False)
    color_pick = fields.Integer(string="Color pick")
    color = fields.Char(string="Color")
    sequence = fields.Integer(string="Sequence", default=1)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        print(default)
        if default is None:
            default = {}
            print(default)
        if not default.get('tag_name'):
            default['tag_name'] = _("%s (copy)", self.tag_name)
            print(default)
        default['sequence'] = 10
        return super().copy(default)

    _sql_constraints = [
        ('unique_tag_name', 'unique (tag_name)', 'Tag name should be unique'),
        ('check_sequence', 'check (sequence > 0)', 'Sequence should be greater than 0')
    ]
