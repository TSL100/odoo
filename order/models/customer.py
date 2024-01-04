from odoo import fields,models,api
from lxml import etree
class CustomerModel(models.Model):
    _name = "customer.order"
    # _inherit = "manage.order"
    _inherits = {'manage.order':'inhit_id'}
# شوف

    lowyer_id = fields.Many2one('res.users',required=True,readonly=False)
    name = fields.Char(string = 'Name')
    user_id = fields.Many2one('res.partner')
    age = fields.Integer(readonly=False,invisible=False)#invisible
    lowyer_ids = fields.One2many('manage.order','customer_id')
    price = fields.Monetary(currency_field='currency_id', tracking=True)
    currency_id = fields.Many2one('res.currency',related = 'company_id.currency_id')
    company_id = fields.Many2one('res.company',related = 'lowyer_id.company_id')
    reference = fields.Reference(selection = [('res.company','company'),('res.currency','currency')])
    float_field = fields.Float(digits=(5,3), help='help massage',index=True)
    inhit_id = fields.Many2one('manage.order')
    man_ids = fields.Many2many('manage.order')
    customer_count = fields.Integer()
    # company_2_id = fields.Many2one('res.company',related ='res.users.company_id')
    #special treat --> company_id name active state
    active = fields.Boolean()
    note = fields.Text()
    state = fields.Selection([])
    _sql_constraints = [
        ('check_age', 'CHECK(age > 5)', 'The number can\'t be small.'),
        ('unique_name', 'unique(name)', 'The name is duplicate.'),
    ]
    def moaz_j(self):
        print(self.env['res.users'].sudo.search([]))

    def print_record(self):
        domain = [('age','=','0')]
        filiter = self.env['customer.order'].search_count(domain)
        self.customer_count = filiter
        print(filiter)

    def m_create(self):
        record = {
            'name':'moaz',
            'age': 18
        }
        record_2 = {
            'name': 'marwan',
            'age': 16
        }
        self.env['customer.order'].create([record,record_2])
    @api.model
    def create(self,vals):
        print('=============',vals)
        vals['name'] = self.env['ir.sequence'].next_by_code('customer.sequence')
        browse_low = self.env['manage.order'].browse(vals.get('lowyer_id'))
        for r in browse_low:
            r.name = "moooooaaaaz"
        return super(CustomerModel, self).create(vals)

    def print_output(self):
        searched = self.env['manage.order'].search([])
        browsed = self.env['manage.order'].browse(searched)
        # filt_r = searched.filtered('name')
        # filt_y = searched.filtered(lambda rec:rec.field_5 > 0)
        sort_i = searched.sorted('field_5', reverse=True)
        map_o = searched.mapped(lambda x:x.field_5)
        print(searched)
        print(sort_i)
        return
    @api.model
    def fields_view_get(self,view_id = None, view_type='form', toolbar=False, submenu=False):
        res = super(CustomerModel,self).fields_view_get(view_id=view_id,view_type=view_type,toolbar=toolbar,submenu=submenu)
        if view_type == "form":
            doc = etree.XML(res['arch'])
            print(res['arch'])
            age_field = doc.xpath("//field[@name='age']")
            active_field = doc.xpath("//field[@name='active']")
            if age_field:
                age_field[0].set('string','new age')
            res['arch'] = etree.tostring(doc,encoding='unicode')
            if active_field:
                active_field[0].addnext(etree.Element('label',{'string':'new label','name':'label'}))
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res
    @api.depends('man_ids')
    def print_out(self):
        domain = [('customer_id','=',self.id)]
        searched = self.env['manage.order'].search([])
        searched_count = self.env['manage.order'].search_count([])
        grouped_record = self.env['manage.order'].read_group(domain=[],fields=['customer_id'],groupby=['customer_id'])
        print(searched)
        print(searched_count)
        print(grouped_record)
        #unlink for hr.employee model
    def unlink(self):
        lawyer_id = self.mapped('inhit_id')#related field
        super(CustomerModel,self).unlink()
        return lawyer_id.unlink
    def print_button(self):
        current = self.fields_get([])
        band = current['lowyer_id']['readonly']
        record = self.search([])
        print(record)
        rec_read = self.read([])
        print(rec_read)
        for i in record:
           if band == False:
               i.note = 'note false'
           else:
               i.note = 'true note'