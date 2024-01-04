from odoo import api, fields, models


class ResGroups(models.Model):
    _inherit = "res.groups"

    def get_application_groups(self, domain):
        group_id = self.env.ref('sale_management.group_sale_order_template').id
        wave_group_id = self.env.ref('sale.group_delivery_invoice_address').id
        return super(ResGroups, self).get_application_groups(domain + [('id', 'not in', (group_id,wave_group_id))])
