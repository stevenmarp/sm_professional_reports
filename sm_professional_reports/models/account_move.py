# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    sm_report_style_id = fields.Many2one(
        'sm.report.style',
        string='Professional Report Style',
        copy=False,
        help="Override the partner/company default style for this document.",
    )
