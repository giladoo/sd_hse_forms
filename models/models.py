# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SdHseFormsProjects(models.Model):
    _name = "sd_hse_forms.projects"
    _description = "Projects"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    project_code = fields.Char()

