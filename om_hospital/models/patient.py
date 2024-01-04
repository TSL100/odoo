from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date, datetime
from dateutil import relativedelta


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "reference"

    name = fields.Char(string="Name", tracking=True, trim=True)
    date_of_birth = fields.Date(string="Date Of Birth")
    age = fields.Integer(string="Age", compute='_compute_age', inverse="_inverse_compute_age"
                         , search="_search_age", tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True)
    reference = fields.Char(string="Reference")
    active = fields.Boolean(string="Active", default=True)
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string="Tags")
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointment Ids")
    parent = fields.Char(string="Parent")
    marital_state = fields.Selection([('married', 'Married'), ('single', 'Single')], string="Marital State",
                                     tracking=True)
    parent_name = fields.Char(string="Parent Name")
    is_birthday = fields.Boolean(string="Birthday?", compute="_compute_birthday")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="URL")

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("The entered date not valid"))

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("You can't delete because there is appointments."))

    @api.model
    def create(self, vals):
        vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient2')
        # vals['date_of_birth'] = self.env['res.user'].next_by_code('hospital.patient2')
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        if not self.reference and not vals.get('reference'):
            print(vals.get('reference'))
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 1

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

    def _search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        star_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        print("hiiiiiiiiiiii...")
        return [('date_of_birth', '>=', star_of_year), ('date_of_birth', '<=', end_of_year)]

    def name_get(self):
        list = []
        for rec in self:
            name = "%s:%s" % (rec.reference,rec.name)
            list.append((rec.id, name))
        return list
        # return [(record.id, "%s %s" % (record.reference, record.name)) for record in self]

    def action_test(self):
        print("Goooooooood")
        return

    @api.depends('date_of_birth')
    def _compute_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if rec.date_of_birth.day == today.day and rec.date_of_birth.month == today.month:
                    is_birthday = True
            rec.is_birthday = is_birthday

    def action_view_appointments(self):
        return {
            'name': _('Appointments'),
            'view_mode': 'tree,form,calendar',
            'domain': [('patient_id', '=', self.id)],
            'res_model': 'hospital.appointment',
            'type': 'ir.actions.act_window',
            'context': {'default_patient_id': self.id},
        }

    def print_report(self):
        return self.env.ref('om_hospital.report_patient_card').report_action(self)

    def print_report_excel(self):
        return self.env.ref('om_hospital.report_patient_card_xls').report_action(self)
