# -*- coding: utf-8 -*-
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sm_report_style_id = fields.Many2one(
        'sm.report.style',
        string='Professional Report Style',
        copy=False,
    )
