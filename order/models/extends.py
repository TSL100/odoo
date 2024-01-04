from odoo import fields,models,api


class inheritmodel(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    new_fild = fields.Char()