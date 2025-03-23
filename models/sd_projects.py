# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SdHseSdProjects(models.Model):
    _inherit = 'sd_projects.projects'

    project_hse_code = fields.Char(tracking=True,
                                   help="It is required for sd_hse_forms module as qr-code link")

    _sql_constraints = [
        ('unique_project_hse_code', 'UNIQUE(project_hse_code)', 'The "project hse code" must be unique!'),
    ]
