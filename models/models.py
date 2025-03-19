# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import qrcode
import base64
from io import BytesIO

class SdHseFormsProjects(models.Model):
    _name = "sd_hse_forms.projects"
    _description = "Projects"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    project_code = fields.Char()
    base_address = fields.Char(compute="_base_address")
    link_address = fields.Char(compute="_base_address")
    qr_code = fields.Binary("QR Code", compute='generate_qr_code')

    def generate_qr_code(self):
        for rec in self:
            if qrcode and base64:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=15,
                    border=4,
                )
                qr.add_data(rec.base_address + rec.project_code)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.update({'qr_code': qr_image})


    def _base_address(self):
        base_address = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/sdhseform/'
        for rec in self:
            rec.base_address = base_address
            rec.link_address = base_address + rec.project_code


class SdHseFormsStopCard(models.Model):
    _name = "sd_hse_forms.stop_card"
    _description = "Stop Card"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    uu_id = fields.Char(required=True)
    subject = fields.Text()
    actions = fields.Text()
    observer_name = fields.Char()
    observer_job_title = fields.Char()
    observer_mobile = fields.Char()
    ip_address = fields.Char()
    active = fields.Boolean(default=True)
    is_new = fields.Boolean(default=True)
    project_name = fields.Many2one('sd_hse_forms.projects')
    safety = fields.Boolean(default=False)
    health = fields.Boolean(default=False)
    environment = fields.Boolean(default=False)
