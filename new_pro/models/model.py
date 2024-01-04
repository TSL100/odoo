from odoo import fields, models, api


class CanDepends(models.Model):
    _inherit = 'account.move'

    account_ids = fields.One2many('stock.picking','stock_id', string="Acctype")
    picking_type_id = fields.Many2one('stock.picking.type')

    pick_ids = fields.Many2many('stock.picking', compute='_compute_picking_ids', string='Receptions', copy=False,
                                store=True)
    incoming_picking_count = fields.Integer("Incoming Shipment count", compute='_compute_incoming_picking_count')

    def action_view_picking(self):
        res = self.env['stock.picking.type'].fields_get(['picking_type_id.id'])
        res2 = self.env["ir.actions.actions"]._for_xml_id('stock.action_picking_tree_all')
        res2['context'] = dict(self._context, default_partner_id=self.partner_id.id,
                                 default_picking_type_id=self.picking_type_id.id, default_origin=self.name)
        print(res2['context'])
        return self._get_action_view_pick(self.pick_ids)

    def _get_action_view_pick(self, pickings):
        self.ensure_one()
        result = self.env["ir.actions.actions"]._for_xml_id('stock.action_picking_tree_all')
        result['context'] = dict(self._context, default_partner_id=self.partner_id.id,
                                 default_picking_type_id=self.account_ids.picking_type_id.id, default_origin=self.name)
        if not pickings or len(pickings) > 1:
            result['domain'] = [('id', 'in', pickings.ids)]
        elif len(pickings) == 1:
            res = self.env.ref('stock.view_picking_form', False)
            form_view = [(res and res.id or False, 'form')]
            result['views'] = form_view + [(state, view) for state, view in result.get('views', []) if view != 'form']
            result['res_id'] = pickings.id
        return result

    @api.depends('pick_ids')
    def _compute_incoming_picking_count(self):
        for order in self:
            order.incoming_picking_count = len(order.pick_ids)


class Inheritaccount(models.Model):
    _inherit = "stock.picking"

    stock_id = fields.Many2one('account.move','Stock')
