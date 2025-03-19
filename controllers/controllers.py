# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request, content_disposition, Response
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
import socket
import uuid
from icecream import ic

class SdHseFormsContorller(http.Controller):
    @http.route('/sdhseform/<string:project_code>', type='http', website=True, auth="public",)
    def hse_forms(self, project_code,  **kwargs):
        # logging.info(f"\nREMOTE_ADDR{request.httprequest.environ['HTTP_X_REAL_IP']}\n")
        ic(request)
        ic(dict(request.session))
        data = {
            'name':'',
            'id': 0,
            'jdate': jdatejs(format="%Y/%m/%d"),
            'uu_id': 0,
        }
        project_id = request.env['sd_hse_forms.projects'].sudo().search([('project_code', '=', project_code)])
        if project_id:
            # todo: It needed to make sure there is no brut force from one ip address
            #  It can done by counting for the same ip address in last 2 minutes.
            #  If it is more than 4, it means that some one is going to send alot of request.

            # todo: I need a blacklist
            uu_id = uuid.uuid4().hex
            request.env['sd_hse_forms.stop_card'].sudo().create({
                'uu_id': uu_id,
                'ip_address': request.httprequest.environ['HTTP_X_REAL_IP'],
                'project_name': project_id.id,
            })
            data = {
                'name': project_id.name,
                'link_address': project_id.link_address,
                'id': project_id.id,
                'jdate': jdatejs(format="%Y/%m/%d"),
                'uu_id': uu_id,
            }

        return http.request.render('sd_hse_forms.form_template', {'props': data})

    @http.route('/sdhseformsdata', type='json', website=True, auth="public",csrf=False)
    def hse_forms_data(self,  **post):
        # data = request.httprequest.get_data()
        ic('sdhse forms data', post)
        ip_address = request.httprequest.environ['HTTP_X_REAL_IP']
        uu_id = post.get('uu_id').get('value', False)
        subject = post.get('subject').get('value')
        actions = post.get('actions').get('value')

        # todo: ignore if there is a private address. It forces the user to use mobile phone internet access to send
        #  the form. But the consequence would be prevention of pc users to send stop card.

        if uu_id:
            record = request.env['sd_hse_forms.stop_card'].sudo().search([('uu_id', '=', uu_id),
                                                                          ('is_new', '=', True), ], order='id desc',)
            if len(record) == 0 or len(record) > 3:
                logging.error(f"[ERROR]The [{uu_id}] count: [{len(record)}]")
                res = False
            elif len(subject) < 6 or len(actions) < 6 :
                logging.error(f"[ERROR]subject:[{subject}] len:[{len(subject)}]\nactions:[{actions}] len:[{len(actions)}]")
                res = False
            else:
                record[0].sudo().write({
                    'subject': subject,
                    'actions': actions,
                    'is_new': False,
                    'health': post.get('health').get('value'),
                    'safety': post.get('safety').get('value'),
                    'environment': post.get('environment').get('value'),
                    'observer_name': post.get('observer_name').get('value'),
                    'observer_job_title': post.get('observer_job_title').get('value'),
                    'observer_mobile': post.get('observer_mobile').get('value'),
                })
                res = True
        else:
            logging.error(f"[ERROR]The [{ip_address}] without UUID")
            res = False

        return res




    @http.route(['/sdhseformsent', '/sdhseformsent/<string:uu_id>'], type='http',
                website=True, auth="public", methods=['POST'],csrf=False )
    def hse_form_sent(self, uu_id=0, **post):
        props = False

        ic('sdhse form sent 1',uu_id, post)
        record = request.env['sd_hse_forms.stop_card'].sudo().search([('uu_id', '=', uu_id),
                                                                      ('is_new', '=', False), ],
                                                                     order='id desc', limit=1 )
        if record:
            props = {
                'subject': record.subject,
                'actions': record.actions,
                'link_address': record.project_name.link_address,
                'project_name': record.project_name.name,
                'uu_id': uu_id,
            }

        ic('sdhse form sent 2',record, props)
        return http.request.render('sd_hse_forms.form_sent_template', {'props': props})

