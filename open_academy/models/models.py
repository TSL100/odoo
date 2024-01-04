# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions

class Course(models.Model):
    _name = 'open_academy.course'

    name = fields.Char('First')
    description = fields.Text(string="Description")
    response_id = fields.Many2one('res.users',ondelete = 'set null')
    session_ids = fields.One2many('open_academy.session','course_id')

    _sql_constraints = [
        ('name_description_check', 'check (name != description)', 'The course should not the description'),
        ('name_uniq', 'unique (name)', 'The course name must be unique !')

    ]
class Session(models.Model):
    _name = 'open_academy.session'

    name = fields.Char('session')
    start_date = fields.Date(default = fields.Date.today)
    duration = fields.Float(digits = (6,2))
    seats = fields.Integer()
    instructor_id = fields.Many2one("res.partner")
    course_id = fields.Many2one("open_academy.course",ondelete = 'cascade',required = True)
    attendee_ids = fields.Many2many('res.partner')
    active = fields.Boolean(default = True)
    taken_seats = fields.Float(compute='seat_taken')
    # end_date = fields.Date(store =True,compute='get_end_date',inverse='set_end_date')
    @api.depends('seats','attendee_ids')
    def seat_taken(self):
        for rec in self:
            if not rec.seats:
                rec.taken_seats = 0.0
            else:
                rec.taken_seats = 100 * len(rec.attendee_ids)/rec.seats
    @api.constrains('instructor_id','attendee_ids')
    def check_not(self):
        for rec in self:
            if rec.instructor_id and rec.instructor_id in rec.attendee_ids:
                raise exceptions.VaildationErorr('asessions instructor cant be attendee')
