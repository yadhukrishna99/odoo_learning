from odoo import api, fields, models


class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _description = "Operation"
    _log_access = False
    _rec_name = 'operation_name'
    # By setting log_access to False, some of the default fields in the given models database will be deleted
    _order = 'sequence'

    doctor_id = fields.Many2one('res.users', string="Doctor")
    operation_name = fields.Char(string="Operation Name")
    patient_record = fields.Reference(selection=[('hospital.patient', 'Patient'),
                                                 ('hospital.appointment', 'Appointment')], string="Patient record")
    patient = fields.Many2one('hospital.patient', string="Patient")
    sequence = fields.Integer(string='Sequence', default=10)

    @api.model
    def name_create(self, name):
        return self.create({'operation_name': name}).name_get()[0]
