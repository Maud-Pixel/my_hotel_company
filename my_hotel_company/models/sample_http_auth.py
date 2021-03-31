from odoo import models,exceptions
from odoo.http import request

class IrHttp(models.Model):
    _inherit = "ir.http"

    @classmethod
    def _auth_method_base_group_user(cls):
        cls._auth_method_user()
        if not request.env.user.has_group('base.group_user'):
            raise exceptions.AccessDenied()
