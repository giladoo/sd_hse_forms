# -*- coding: utf-8 -*-
{
    'name': "SD HSE Forms",
    'summary': """
        """,
    'description': """
        
    """,
    'author': "Arash Homayounfar",
    'category': 'Service Desk/Service Desk',
    'application': True,
    'version': '18.0.1.0.0',
    'depends': ['base', 'website', ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'data/weather_data.xml',
        # 'data/hazard_types_data.xml',
        'views/hse_form_templates.xml',
        # 'views/records_form.xml',
        'views/views.xml',
    ],
    'assets': {

        'web.assets_frontend': [
            'sd_hse_forms/static/src/components/website/**/*',

        ],
        'web.assets_backend': [
            # 'sd_hse/static/src/css/style.scss',
            # 'sd_hse/static/src/components/web/**/*',
            # 'sd_hse/static/src/js/**/*.js',
            # 'sd_hse/static/src/js/**/*.css',
        ],
        'web.report_assets_common': [
        ],

    },

    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'license': 'LGPL-3',

}
