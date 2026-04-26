# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


TEMPLATE_SELECTION = [
    ('classic', 'Classic'),
    ('modern', 'Modern'),
    ('slim', 'Slim'),
    ('retro', 'Retro'),
    ('bold', 'Bold'),
    ('elegant', 'Elegant'),
    ('corporate', 'Corporate'),
    ('minimal', 'Minimal'),
    ('accent', 'Accent'),
    ('executive', 'Executive'),
    ('striped', 'Striped'),
]


FONT_FAMILY_SELECTION = [
    ('sans-serif', 'Sans-serif (default)'),
    ('Arial, sans-serif', 'Arial'),
    ('Helvetica, sans-serif', 'Helvetica'),
    ('Calibri, sans-serif', 'Calibri'),
    ('"Times New Roman", serif', 'Times New Roman'),
    ('Georgia, serif', 'Georgia'),
    ('"Courier New", monospace', 'Courier New'),
    ('"Trebuchet MS", sans-serif', 'Trebuchet MS'),
    ('Verdana, sans-serif', 'Verdana'),
    ('Tahoma, sans-serif', 'Tahoma'),
]


AMOUNT_IN_WORDS_LANG = [
    ('en', 'English'),
    ('en_GB', 'British English'),
    ('en_IN', 'Indian English'),
    ('fr', 'French'),
    ('de', 'German'),
    ('es', 'Spanish'),
    ('it', 'Italian'),
    ('pt_BR', 'Brazilian Portuguese'),
    ('ru', 'Russian'),
    ('pl', 'Polish'),
    ('no', 'Norwegian'),
    ('lt', 'Lithuanian'),
    ('lv', 'Latvian'),
    ('id', 'Indonesian'),
]


class SmReportStyle(models.Model):
    _name = 'sm.report.style'
    _description = 'Professional Report Style'
    _order = 'sequence, id'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company,
    )

    # Template
    template = fields.Selection(
        TEMPLATE_SELECTION, string='Template', required=True, default='classic',
        help="Visual layout used to render the document.",
    )

    # Colors
    theme_color = fields.Char(
        string='Theme Color', default='#74495f',
        help="Main brand color used for headers, totals & accents. Hex value (e.g. #74495f).",
    )
    text_color = fields.Char(string='Body Text Color', default='#333333')
    theme_text_color = fields.Char(string='Theme Text Color', default='#ffffff')
    company_name_color = fields.Char(string='Company Name Color', default='#74495f')
    partner_name_color = fields.Char(string='Customer Name Color', default='#74495f')

    # Fonts
    font_family = fields.Selection(
        FONT_FAMILY_SELECTION, string='Font Family', default='sans-serif',
    )
    header_font_size = fields.Integer(string='Header Font Size (px)', default=12)
    body_font_size = fields.Integer(string='Body Font Size (px)', default=11)
    footer_font_size = fields.Integer(string='Footer Font Size (px)', default=9)

    # Table
    zebra_rows = fields.Boolean(string='Alternate Row Colors', default=True)
    odd_row_color = fields.Char(string='Odd Row Color', default='#ffffff')
    even_row_color = fields.Char(string='Even Row Color', default='#f6f0f3')
    show_row_number = fields.Boolean(string='Show Row Number', default=True)
    show_product_image = fields.Boolean(string='Show Product Image', default=True)

    # Amount in words
    amount_in_words = fields.Boolean(string='Show Amount in Words', default=True)
    amount_in_words_lang = fields.Selection(
        AMOUNT_IN_WORDS_LANG, string='Amount in Words Language', default='en',
    )

    # Watermark
    watermark_pdf = fields.Binary(
        string='Watermark / Letterhead PDF',
        help="A PDF (same paper size as your reports) that will be used as the background "
             "of every page.",
    )
    watermark_pdf_filename = fields.Char()
    watermark_text = fields.Char(
        string='Watermark Text',
        help="Optional text printed diagonally on every page. Supports keywords: "
             "{date}, {time}, {company}, {user}, {partner}, {document}.",
    )
    watermark_text_color = fields.Char(string='Watermark Text Color', default='#cccccc')
    watermark_text_size = fields.Integer(string='Watermark Text Size (px)', default=64)

    # Last page PDF
    last_page_pdf = fields.Binary(
        string='Last Page PDF',
        help="A PDF appended at the end of every printed report (terms & conditions, "
             "brochure, advert, etc.). Multi-page PDFs are supported.",
    )
    last_page_pdf_filename = fields.Char()

    # Footer
    show_footer_logo = fields.Boolean(string='Show Footer Logo', default=False)
    footer_logo = fields.Binary(string='Footer Logo (small)')
    footer_tagline = fields.Char(string='Footer Tagline', translate=True)
    show_bank_in_footer = fields.Boolean(string='Show Bank Details In Footer', default=False)

    @api.constrains('header_font_size', 'body_font_size', 'footer_font_size',
                    'watermark_text_size')
    def _check_font_sizes(self):
        for rec in self:
            for fname in ('header_font_size', 'body_font_size',
                          'footer_font_size', 'watermark_text_size'):
                val = rec[fname]
                if val < 1 or val > 200:
                    raise ValidationError(_(
                        "Font size '%s' must be between 1 and 200 pixels."
                    ) % fname)

    @api.constrains('theme_color', 'text_color', 'theme_text_color',
                    'company_name_color', 'partner_name_color',
                    'odd_row_color', 'even_row_color', 'watermark_text_color')
    def _check_colors(self):
        import re
        pattern = re.compile(r'^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')
        for rec in self:
            for fname in ('theme_color', 'text_color', 'theme_text_color',
                          'company_name_color', 'partner_name_color',
                          'odd_row_color', 'even_row_color', 'watermark_text_color'):
                val = rec[fname]
                if val and not pattern.match(val):
                    raise ValidationError(_(
                        "Color '%s' must be a valid hex value like #ffffff or #fff. "
                        "Got: %s"
                    ) % (fname, val))

    # ---- Public API used by QWeb templates ----

    def get_amount_in_words(self, amount, currency=None):
        """Convert a numeric amount to words in the configured language."""
        self.ensure_one()
        if not self.amount_in_words or amount is None:
            return ''
        try:
            from num2words import num2words
        except ImportError:
            return ''
        lang = self.amount_in_words_lang or 'en'
        # num2words doesn't accept locale codes with underscore for all langs
        n2w_lang = lang.split('_')[0]
        try:
            words = num2words(float(amount), lang=n2w_lang).capitalize()
        except (NotImplementedError, Exception):
            try:
                words = num2words(float(amount)).capitalize()
            except Exception:
                return ''
        if currency:
            words = "%s %s" % (words, currency.name or '')
        return words

    def render_watermark_text(self, document=None):
        """Replace placeholders in watermark_text."""
        self.ensure_one()
        if not self.watermark_text:
            return ''
        from datetime import datetime
        ctx = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M'),
            'company': self.env.company.name or '',
            'user': self.env.user.name or '',
            'partner': '',
            'document': '',
        }
        if document is not None:
            partner = getattr(document, 'partner_id', False)
            if partner:
                ctx['partner'] = partner.name or ''
            ctx['document'] = (
                getattr(document, 'name', False)
                or getattr(document, 'display_name', '')
                or ''
            )
        try:
            return self.watermark_text.format(**ctx)
        except (KeyError, IndexError):
            return self.watermark_text

    @api.model
    def get_style_for(self, document):
        """Resolve the style to use for `document`.

        Priority:
            1. Style explicitly set on the document (sm_report_style_id)
            2. Style set on the document's partner
            3. Style set on the company
            4. Any active default style
        """
        if not document:
            return self.env['sm.report.style']

        # Document override
        if 'sm_report_style_id' in document._fields and document.sm_report_style_id:
            return document.sm_report_style_id

        # Partner override
        partner = getattr(document, 'partner_id', False)
        if partner and 'sm_report_style_id' in partner._fields \
                and partner.sm_report_style_id:
            return partner.sm_report_style_id

        # Company default
        company = getattr(document, 'company_id', False) or self.env.company
        if 'sm_report_style_id' in company._fields and company.sm_report_style_id:
            return company.sm_report_style_id

        # Fallback: any active style
        return self.search([('active', '=', True)], limit=1)
