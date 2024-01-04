from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval, datetime


class OdooPlayground(models.Model):
    _name = "odoo.playground"
    _description = "Odoo Playground"

    #  - env: Odoo Environment on which the action is triggered
    #  - self.env: Odoo Environment on which the action is triggered
    #  - self.env.user: return the current user (as instance)
    #  - self.env.is_system: Return whether the current user has group "Settings", or is in superuser mode.
    #  - self.env.is_admin: Return whether the current user has group "Access Rights", or is in superuser mode.
    #  - self.env.is_superuser: Return whether the environment is in superuser mode.
    #  - self.env.company: Return the current company (as an instance).
    #  - self.env.companies: Return a recordset of the enabled companies by the user.
    #  - self.env.lang: Return the current language code.
    #  - self.env.cr:cursor
    #  - self.env.context:return information like id,lang



    model_id = fields.Many2one('ir.model', string="Model")
    code = fields.Text(string="Code")
    result = fields.Text(string="Result")

    def action_execute(self):
        try:
            if self.model_id:
                model = self.env[self.model_id.model]
            else:
                model = self
            self.result = safe_eval(self.code.strip(), {'self': model})
        except Exception as e:
            self.result = str(e)

    def clear(self):
        for rec in self:
            rec.result = " "
            rec.code = " "

