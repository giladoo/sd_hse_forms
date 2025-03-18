# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request, content_disposition
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import datetime
import jdatetime
import logging
import io
from io import BytesIO
import base64
from docx import Document
from jdatetimext import jdatejs

class SdHseFormsContorller(http.Controller):
    @http.route('/sdhseform/<string:project_code>', type='http', website=True, auth="public",)
    def hse_forms(self, project_code,  **kwargs):
        print(f'\n project_code: {project_code} kwargs: {kwargs}')
        data = {}
        project_id = request.env['sd_hse_forms.projects'].sudo().search([('project_code', '=', project_code)])
        if project_id:
            data = {
                'name': project_id.name,
                'id': project_id.id,
                'jdate': jdatejs(format="%Y/%m/%d"),


            }

        print(f'\n data: {data}')
        return http.request.render('sd_hse_forms.form_template', {'props': data})
