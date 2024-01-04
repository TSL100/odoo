from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import random


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _inherit = ['hospital.patient', 'mail.thread', 'mail.activity.mixin']
    _rec_name = "ref"
    _order = "id desc"

    name = fields.Char(string="Sequence", default="new", tracking=True)
    # patient_id = fields.Many2one(model_name='hospital.patient', string="Patient Name",ondelete="restrict")
    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patient Name", ondelete="cascade", tracking=1)
    gender_appointment = fields.Selection(related='patient_id.gender', readonly=False)
    appointment_time = fields.Datetime(string="Entering Time", default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)
    ref = fields.Char(string="Reference")
    prescription = fields.Html(string="Prescription")
    priority = fields.Selection([('0', 'low'), ('1', 'normal'), ('2', 'mid'), ('3', 'high'), ('4', 'very high')],
                                string="priority")
    state = fields.Selection([('draft', 'Draft'),
                              ('in_consultation', 'In_consultation'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled')], required=True, string="Status", default='draft')
    doctor_id = fields.Many2one('res.users', string="Doctor", tracking=2)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string="Pharmacy lines")
    hide_sales_price = fields.Boolean(string="Hide Sales Price")
    operation_name = fields.Many2one('hospital.operation', string="Operations", tracking=True)
    progress = fields.Integer(string="Progress", compute="_compute_progress")
    duration = fields.Integer(string="Duration")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    url = fields.Char(string="URL")

    def set_line_number(self):
        sl_no = 0
        for line in self.pharmacy_line_ids:
            sl_no += 1
            line.sl_no = sl_no
        return

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        res = super(HospitalAppointment, self).create(vals)
        res.set_line_number()
        return res

    def write(self, values):
        res = super(HospitalAppointment, self).write(values)
        self.set_line_number()
        return res

    def unlink(self):
        for rec in self:
            if self.state == 'done':
                raise ValidationError(_("you can't delete if state is done"))
        return super(HospitalAppointment, self).unlink()

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.reference

    def action_test(self):
        print("Button clicked !!!!")
        return {
            'type': 'ir.actions.act_url',
            'url': self.url,
            # 'url': 'web',
            # 'url': 'http://google.com',
            'target': 'new',
        }

    def action_notification(self):
        action = self.env.ref('om_hospital.action_hospital_appointment')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Click to open patient record'),
                'message': '%s',
                'links': [{
                    'label': 'Click Here',
                    'url': f'#action={action.id}&id={self.patient_id.id}&model=hospital.appointment'
                }],
                'sticky': True,
                'next': {
                    'type': 'ir.actions.act_window',
                    'res_model': 'hospital.patient',
                    'res_id': self.patient_id.id,
                    'views': [(False, 'form')],
                },
            }
        }

    # if I want to go to patient view
    # action = self.env.ref('om_hospital.action_hospital_patient')
    # return {
    #     'type': 'ir.actions.client',
    #     'tag': 'display_notification',
    #     'params': {
    #         'title': _('Click to open patient record'),
    #         'message': '%s',
    #         'links': [{
    #             'label': 'Click Here',
    #             'url': f'#action={action.id}&id={self.patient_id.id}&model=hospital.patient'
    #         }],
    #         'sticky': False,
    #     }
    # }

    def action_share_whatsapp(self):
        if not self.patient_id.phone:
            raise ValidationError("Please Enter your phone number")
        message = "Hi * %s * your appointment number is : %s ,Thank you" % (self.patient_id.name, self.name)
        whatsapp_api_url = 'https://web.whatsapp.com/send?phone=%s&text=%s' % (self.patient_id.phone, message)
        self.message_post(body=message, subject="Whatsapp Message")
        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_api_url,
            'target': 'new',
        }

    def action_send_email(self):
        template = self.env.ref('om_hospital.appointment_template_mail')
        for rec in self:
            if rec.patient_id.email:
                email_values = {'subject': 'From your company'}
                template.send_mail(rec.id, force_send=True, email_values=email_values)
                # email_values = {
                #     'email_cc': False,
                #     'auto_delete': True,
                #     'recipient_ids': [],
                #     'partner_ids': [],
                #     'scheduled_date': False,}

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Done Successfully',
                'type': 'rainbow_man',
            }
        }

    def action_cancel(self):
        action = self.env.ref('om_hospital.action_hospital_appointment_cancel').read()[0]
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = random.randrange(0, 25)
            elif rec.state == 'in_consultation':
                progress = random.randrange(25, 99)
            elif rec.state == 'done':
                progress = 200
            else:
                progress = 0
            rec.progress = progress


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    sl_no = fields.Integer(string="SNO.")
    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(related='product_id.list_price', digits="Product Price")
    qty = fields.Integer(string="Quantity", default=1)
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    currency_id = fields.Many2one('res.currency', related='appointment_id.currency_id')
    price_subtotal = fields.Monetary(string="Subtotal", compute="_compute_price_total", currency_fied="currency_id")

    @api.depends('price_unit', 'qty')
    def _compute_price_total(self):
        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.qty
