from odoo import fields, models, api


class Invoicing(models.Model):
    _inherit = 'account.move'

    picking_ids = fields.One2many('stock.picking', 'sale_id')
    pick_ids = fields.Many2many('stock.picking', compute='_compute_picking_ids', string='Receptions', copy=False, store=True)
    move_ids = fields.One2many('stock.move', 'purchase_line_id', string='Reservation', readonly=True, copy=False)
    delivery_count = fields.Integer(string='Delivery Orders', compute='_compute_picking_ids')
    incoming_picking_count = fields.Integer("Incoming Shipment count", compute='_compute_incoming_picking_count')


    def _get_action_view_picking(self, pickings):
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        picking_id = pickings.filtered(lambda l: l.picking_type_id.code == 'outgoing')
        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = pickings[0]
        action['context'] = dict(self._context, default_partner_id=self.partner_id.id,
                                 default_picking_type_id=picking_id.picking_type_id.id, default_origin=self.name,
                                 default_group_id=picking_id.group_id.id)
        return action

    def _get_action_view_pick(self, pickings):
        self.ensure_one()
        result = self.env["ir.actions.actions"]._for_xml_id('stock.action_picking_tree_all')
        result['context'] = {'default_partner_id': self.partner_id.id, 'default_origin': self.name, 'default_picking_type_id': self.picking_type_id.id}
        if not pickings or len(pickings) > 1:
            result['domain'] = [('id', 'in', pickings.ids)]
        elif len(pickings) == 1:
            res = self.env.ref('stock.view_picking_form', False)
            form_view = [(res and res.id or False, 'form')]
            result['views'] = form_view + [(state, view) for state, view in result.get('views', []) if view != 'form']
            result['res_id'] = pickings.id
        return result

    def action_view_delivery(self):
        return self._get_action_view_picking(self.picking_ids)

    def action_view_picking(self):
        return self._get_action_view_picking(self.pick_ids)

    @api.depends('move_ids.picking_id')
    def _compute_picking_ids(self):
        for order in self:
            order.pick_ids = order.move_ids.picking_id

    @api.depends('pick_ids')
    def _compute_picking_ids(self):
        for order in self:
            order.delivery_count = len(order.pick_ids)

    @api.depends('pick_ids')
    def _compute_incoming_picking_count(self):
        for order in self:
            order.incoming_picking_count = len(order.pick_ids)

class Inheritaccount(models.Model):
    _inherit = "stock.picking"
    sale_id = fields.Many2one('sale.order')
    purchase_line_id = fields.Many2one(
        'purchase.order.line', 'Purchase Order Line',
        ondelete='set null', index='btree_not_null', readonly=True)
