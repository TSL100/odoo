from odoo import api, fields, models, _


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer(string="Color", copy="3")
    color_2 = fields.Char(string="Color 2")
    sequence = fields.Integer(string="Sequence")

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get("name"):
            default['name'] = _("%s (copy)") % (self.name)
        default['sequence'] = 10
        return super(PatientTag, self).copy(default)

    _sql_constraints = [
        ('unique_tag_name', 'unique (name)', 'Name of the patient must be unique  !'),
        ('check_sequence', 'check(sequence>0)', 'Sequence of the patient must be positive number!')]
