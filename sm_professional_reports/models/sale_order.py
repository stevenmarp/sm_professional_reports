# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sm_report_style_id = fields.Many2one(
        'sm.report.style',
        string='Professional Report Style',
        copy=False,
    )
