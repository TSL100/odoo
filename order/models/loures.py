from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
from datetime import date,datetime


class Manage(models.Model):
    _name = "manage.order"
    _description="order manage model"
    _order="id desc"
    _rec_name = "name"
    name = fields.Char()
    new_field = fields.Text()
    field_0 = fields.Selection([("male","Male")])
    field_1 = fields.Boolean()
    field_2 = fields.Html()
    field_3 = fields.Image()
    field_4 = fields.Binary()
    field_5 = fields.Integer()
    field_6 = fields.Date()
    field_7 = fields.Datetime(default=datetime.now())
    age = fields.Integer(cmpute="get_age")
    customer_id = fields.Many2one('customer.order')
    customer_ids = fields.Many2many('customer.order')
    sequence_id = fields.Many2one('ir.sequence')
    state = fields.Selection([('draft','Draft'),('done','Done')], string="State")
    @api.depends('field_6')
    def get_age(self):
        for rec in self:
            currdate = date.today()
            if rec.field_6:
                rec.age = currdate.year - rec.field_6.year
            else:
                rec.age = 1

    @api.constrains('field_5')
    def check_age(self):
        if self.field_5 < 21:
            raise ValidationError('this age is not a')

    def name_get(self):
        for rec in self:
            return [(rec.id, "[%s] (%s)"%(rec.new_field, rec.name ))]

#          abstractmodel == للكلاسات اللي عامل
    @api.model
    def default_get(self,fields):
        res = super(Manage,self).default_get(fields)
        print(fields)
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|',('field_5',operator,name),('field_6',operator,name)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
    @api.model
    def write(self,vals):
        vals['field_5'] = 55
        print(vals)
        return super(Manage,self).write(vals)
    @api.returns('self', lambda x : x.id)
    def copy(self,default=None):
        raise ValidationError(_("can not duplicate"))
        # if not default:
        #     default = {}
        #     default['name'] = self.name = "copy"
        # return super(Manage,self).copy(default=default)
    # @api.model
    # def create(self,vals):
    #     if not vals['ir.sequence']:
    #        lawer = self.env['manage.order'].browse(vals['lawyer_id'])
    #        vals['ir.sequence'] = self.env['ir.sequence'].sudo.create([])

