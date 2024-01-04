from odoo import models, fields, api

class Partner(models.Model):
    _inherit='res.partner'


    instructor =fields.Boolean()
    session_ids = fields.Many2many('open_academy.session',readonly=True)
