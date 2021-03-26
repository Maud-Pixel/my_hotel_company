from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BedroomCategory(models.Model):
    _name = "bedroom.categ"
    _description = "Model to categorize booking of bedrooms"
    name = fields.Char("Category")

    _parent_store = True
    _parent_name = "parent_id"

    description= fields.Text("Description")
    parent_path = fields.Char(index=True)
    parent_id = fields.Many2one("bedroom.categ", string="Parent Category", ondelete="restrict", index=True)
    child_ids = fields.One2many("bedroom.categ", "parent_id", string="Child Categories")

    @api.constrains("parent_id")
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError("Looping exception. You cannot create recursive categories")

    def create_categories(self):
        catego1 = {
            "name": "catego1",
            "description": "description for child1"
        }
        catego2= {
            "name": "catego2",
            "description":"description for child2"
        }
        parent_catego_val={
            "name": "parent_catego_val",
            "email": 'email of the parent catego',
            "child_ids": [
                (0,0,catego1),
                (0,0,catego2),
            ]
        }
        record = self.env["bedroom.categ"].create(parent_catego_val)