from odoo import api, fields, models


class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _description = "Operation"
    _log_access = False
    # By setting log_access to False, some of the default fields in the given models database will be deleted

    doctor_id = fields.Many2one('res.users', string="Doctor")
    operation_name = fields.Char(string="Operation Name")

    @api.model
    def name_create(self, name):
        return self.create({'operation_name': name}).name_get()[0]
