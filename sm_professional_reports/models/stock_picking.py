# -*- coding: utf-8 -*-
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sm_report_style_id = fields.Many2one(
        'sm.report.style',
        string='Professional Report Style',
        copy=False,
    )
