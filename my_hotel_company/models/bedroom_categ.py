from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BedroomCategory(models.Model):
    _name = "bedroom.categ"
    _description = "Model to categorize booking of bedrooms"
    name = fields.Char("Category")

    _parent_store = True
    _parent_name = "parent_id"

    parent_path = fields.Char(index=True)
    parent_id = fields.Many2one("bedroom.categ", string="Parent Category", ondelete="restrict", index=True)
    child_ids = fields.One2many("bedroom.categ", "parent_id", string="Child Categories")

    @api.constrains("parent_id")
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError("Looping exception. You cannot create recursive categories")