from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import datetime
from datetime import date
from dateutil import relativedelta


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    # appointment_id = fields.Many2one('hospital.appointment', string="Appointment",domain="[('state','=','draft'),('priority','in',('0','1',False))]")
    reason = fields.Text(string="Reason")
    date_cancelled = fields.Date(string="Cancellation Date")

    # def action_cancel(self):
    #     if self.appointment_id.booking_date == fields.Date.today():
    #         raise ValidationError(_("Sorry,Cannot cancel in the same day of booking"))
    #     self.appointment_id.state='cancel'
    #     return

    def action_cancel(self):
        cancel_day = self.env['ir.config_parameter'].get_param('om_hospital.cancel_days')
        allowed_date = self.appointment_id.booking_date - relativedelta.relativedelta(days=int(cancel_day))
        if cancel_day != 0 and allowed_date < date.today():
            raise ValidationError(_("It 's too late ,You cannot cancel because the appointment is passed"))
        self.appointment_id.state = 'cancel'
        # query = """select id,name from hospital_patient"""
        query = """select id,patient_id from hospital_appointment where id=%s""" % self.appointment_id.id
        self._cr.execute(query)
        # self.env.cr.execute(query)
        # patients = self._cr.fetchall()
        # patients = self._cr.fetchone()
        patients = self._cr.dictfetchone()
        print(patients)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',  # --->reload page after cancellation
            # 'type': 'ir.actions.act_window',
            # 'view_mode': 'form',
            # 'res_model': 'cancel.appointment.wizard',
            # 'res_id': self.id,
            # 'target': 'new'
        }

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['date_cancelled'] = datetime.date.today()
        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
        return res

    def action_print_report(self):
        return
