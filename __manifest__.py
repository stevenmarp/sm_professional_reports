# -*- coding: utf-8 -*-
{
    'name': 'Professional Report Templates — Invoice, Sales, Purchase, Delivery',
    'version': '19.0.1.0.0',
    'summary': '30 beautiful PDF templates for Invoices, Sales Orders, Purchase Orders '
               '& Delivery Slips. Theme colors, fonts, watermark PDF, last-page PDF, '
               'amount-in-words & per-partner styles.',
    'description': """
Professional Report Templates for Odoo 19
==========================================

Replace the standard Odoo PDF reports with beautifully designed templates for:

- **Invoices & Credit Notes** (account.move)
- **Sales Orders & Quotations** (sale.order)
- **Purchase Orders & RFQs** (purchase.order)
- **Delivery Slips** (stock.picking)

**30 Templates — Including 5 Structurally Unique Layouts**

- 30 distinct ready-to-use templates: *Classic*, *Modern*, *Slim*, *Retro*, *Bold*, *Elegant*, *Corporate*, *Minimal*, *Accent*, *Executive*, *Striped*, *Formal*, *Rounded*, *Centered*, *Voucher*, *Grid*, *Banner*, *Sidebar*, *Contrast*, *Split*, *Lined*, *Boxed*, *Ribbon*, *Compact*, *Gradient*, *Letter*, *Dashboard*, *Catalog*, *Ledger*, *Ticket*
- **Letter** — formal business letter with greeting, closing & signature block
- **Dashboard** — KPI summary stat cards at top, compact table below
- **Catalog** — card-based line items (no traditional table rows)
- **Ledger** — accounting journal style, serif font, double-ruled borders
- **Ticket** — receipt / kuitansi style with dashed tear lines & dot-leader totals

**Style & Branding**

- Theme color, text color, company & partner name colors
- Font family (8 choices), header / body / footer font sizes
- Zebra-stripe alternate row coloring with custom even-row color
- Optional product image column in line tables
- Optional row numbers
- Prepared-by & Authorized-by signature blocks

**Amount in Words — 13 Languages**

- English, French, German, Spanish, Italian, Portuguese (BR), Russian, Polish, Norwegian, Lithuanian, Latvian, Indian English, Indonesian
- Powered by `num2words`

**Watermark & Last-Page PDF**

- Upload a letterhead PDF as background watermark on every page
- Dynamic watermark text with placeholders (date, partner, document number...)
- Append a "last page" PDF automatically (terms & conditions, brochure...)

**Multi-Level Style Priority**

- Per-company default style
- Per-partner override (assign a specific style to a customer/supplier)
- Per-document override (set a style on a single invoice/order)
- Cascade: document > partner > company

**Footer Customization**

- Custom footer tagline text
- Bank account details (auto from company bank accounts)
- VAT number display
- Optional small footer logo

**Technical**

- Works with Odoo 19 Community & Enterprise
- Clean, well-documented codebase — easy to add your own templates
- Shared building blocks for consistent look across all report types
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
        'reports/sm_report_template_banner.xml',
        'reports/sm_report_template_sidebar.xml',
        'reports/sm_report_template_contrast.xml',
        'reports/sm_report_template_split.xml',
        'reports/sm_report_template_lined.xml',
        'reports/sm_report_template_boxed.xml',
        'reports/sm_report_template_ribbon.xml',
        'reports/sm_report_template_compact.xml',
        'reports/sm_report_template_gradient.xml',
        'reports/sm_report_template_letter.xml',
        'reports/sm_report_template_dashboard.xml',
        'reports/sm_report_template_catalog.xml',
        'reports/sm_report_template_ledger.xml',
        'reports/sm_report_template_ticket.xml',
        'reports/sm_invoice_report.xml',
        'reports/sm_sale_order_report.xml',
        'reports/sm_purchase_order_report.xml',
        'reports/sm_stock_picking_report.xml',
    ],

    'images': ['static/description/banner.gif'],
    'price': 104.48,
    'currency': 'USD',
    'installable': True,
    'application': False,
    'auto_install': False,
}
