# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sm_report_style_id = fields.Many2one(
        'sm.report.style',
        string='Professional Report Style',
        help="Override the company's default professional report style for this "
             "partner (customer/supplier).",
    )
