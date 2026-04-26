# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sm_report_style_id = fields.Many2one(
        'sm.report.style',
        string='Default Professional Report Style',
        domain="['|', ('company_id', '=', False), ('company_id', '=', id)]",
        help="Style applied to professional reports by default for this company. "
             "Can be overridden per partner or per document.",
    )
