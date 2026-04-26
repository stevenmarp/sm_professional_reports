# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sm_report_style_id = fields.Many2one(
        related='company_id.sm_report_style_id',
        string='Default Professional Report Style',
        readonly=False,
    )
