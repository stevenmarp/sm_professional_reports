# -*- coding: utf-8 -*-
{
    'name': 'Professional Report Templates — Invoice, Sales, Purchase, Delivery',
    'version': '19.0.1.0.0',
    'summary': '16 beautiful PDF templates for Invoices, Sales Orders, Purchase Orders '
               '& Delivery Slips. Theme colors, fonts, watermark PDF, last-page PDF, '
               'amount-in-words & per-partner styles.',
    'description': """
Professional Report Templates for Odoo 19
==========================================

Replace the standard Odoo PDF reports with beautifully designed templates for:

- **Invoices** (account.move)
- **Sales Orders & Quotations** (sale.order)
- **Purchase Orders & RFQs** (purchase.order)
- **Delivery Slips** (stock.picking)

**Key Features**

- 16 distinct ready-to-use templates: *Classic*, *Modern*, *Slim*, *Retro*, *Bold*, *Elegant*, *Corporate*, *Minimal*, *Accent*, *Executive*, *Striped*, *Formal*, *Rounded*, *Centered*, *Voucher*, *Grid*
- Pick a theme color, font family, font size for header/body/footer
- Per-company default style
- Per-partner override (assign a specific style to a customer/supplier)
- Per-document override (set a style on a single invoice/order)
- Alternate row coloring (zebra stripes) for line tables
- Optional product image column
- Optional amount-in-words (13 languages via num2words)
- Watermark PDF (background letterhead) + dynamic watermark text
- Append a "last page" PDF (terms & conditions, brochure...) automatically
- Custom footer with bank details, VAT, tagline & small logo
- Clean, well-documented codebase — easy to add your own templates
    """,
    'author': 'Steven Marp',
    'website': 'https://apps.odoo.com/apps/browse?repo_maintainer_id=512936',
    'category': 'Accounting/Accounting',
    'license': 'OPL-1',

    'depends': [
        'base',
        'web',
        'mail',
        'account',
        'sale_management',
        'purchase',
        'stock',
    ],

    'external_dependencies': {
        'python': ['num2words', 'PyPDF2'],
    },

    'data': [
        # Security
        'security/sm_professional_reports_security.xml',
        'security/ir.model.access.csv',

        # Data
        'data/sm_report_paperformat_data.xml',
        'data/sm_report_style_data.xml',

        # Views
        'views/sm_report_style_views.xml',
        'views/res_partner_views.xml',
        'views/account_move_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'views/res_config_settings_views.xml',
        'views/menu.xml',

        # Reports — layouts first, then actions
        'reports/sm_report_layouts.xml',
        'reports/sm_report_template_classic.xml',
        'reports/sm_report_template_modern.xml',
        'reports/sm_report_template_slim.xml',
        'reports/sm_report_template_retro.xml',
        'reports/sm_report_template_bold.xml',
        'reports/sm_report_template_elegant.xml',
        'reports/sm_report_template_corporate.xml',
        'reports/sm_report_template_minimal.xml',
        'reports/sm_report_template_accent.xml',
        'reports/sm_report_template_executive.xml',
        'reports/sm_report_template_striped.xml',
        'reports/sm_report_template_formal.xml',
        'reports/sm_report_template_rounded.xml',
        'reports/sm_report_template_centered.xml',
        'reports/sm_report_template_voucher.xml',
        'reports/sm_report_template_grid.xml',
        'reports/sm_invoice_report.xml',
        'reports/sm_sale_order_report.xml',
        'reports/sm_purchase_order_report.xml',
        'reports/sm_stock_picking_report.xml',
    ],

    'images': ['static/description/banner.gif'],
    'price': 644.48,
    'currency': 'USD',
    'installable': True,
    'application': False,
    'auto_install': False,
}
