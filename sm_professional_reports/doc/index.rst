================================================================
Professional Report Templates — User Guide
================================================================

.. contents:: Table of Contents
   :depth: 2
   :local:

----

1. Overview
===========

The **Professional Report Templates** module replaces the standard, plain
Odoo PDF reports with beautifully designed alternatives for:

- Customer **Invoices** (and Credit Notes / Vendor Bills)
- **Sales Orders** & **Quotations**
- **Purchase Orders** & **RFQs**
- **Delivery Slips** (stock picking)

The look & feel of every report is driven by a single ``Report Style``
record. You can have unlimited styles and assign them per company,
per partner, or per individual document.

----

2. Installation
===============

1. Drop the ``sm_professional_reports`` folder in your Odoo ``addons`` path.
2. Install Python dependencies::

     pip install num2words PyPDF2 reportlab

   ``reportlab`` is only required if you want the *watermark text*
   feature — the rest of the module works without it.
3. Restart Odoo and update the apps list.
4. Install **Professional Report Templates** from the Apps menu.

----

3. Quick Start
==============

Step 1 — Pick a default style
-----------------------------

After installation, three sample styles are created for you:

- **Classic — Default** (purple)
- **Modern — Teal**
- **Slim — Mono**

Go to **Settings → Professional Reports → Default Style**, choose one
and click *Save*. From now on, that style will be used by every
professional report printed by your company.

Step 2 — Print
--------------

Open any invoice, sales order, purchase order or delivery slip and
click **Print → Professional ...** in the action menu. The PDF will
be generated using your selected style.

----

4. Customizing a Style
=======================

Go to **Settings → Technical → Professional Reports → Report Styles**
(or use the *Manage Styles* button in the settings page).

A style controls:

- **Template** — *Classic*, *Modern* or *Slim* layout
- **Theme color**, text colors, header/body/footer font size
- **Font family**
- **Alternate row colors** for line tables (zebra stripes)
- Whether to show **product images** in the lines table
- Whether to print the **amount in words** (13 languages supported)
- A **watermark / letterhead PDF** used as page background
- A **watermark text** overlay (with placeholders, see below)
- A **last-page PDF** appended at the end of the report
  (terms & conditions, brochure, marketing material...)
- A small **footer logo**, tagline, and optional bank details

Watermark text placeholders
---------------------------

The *Watermark Text* field accepts the following placeholders that
will be replaced at print time:

- ``{date}`` → today's date
- ``{time}`` → current time
- ``{company}`` → company name
- ``{user}`` → user printing the report
- ``{partner}`` → partner of the document
- ``{document}`` → document number / name

Example::

    CONFIDENTIAL — {document} — {date}

----

5. Per-Partner Style
=====================

Open any partner (customer or supplier), go to the **Reports** tab and
pick a style. Every professional report addressed to that partner will
use this style instead of the company default.

----

6. Per-Document Style
======================

For a one-off override, open the invoice / sales order / purchase
order / delivery slip and set the *Professional Report Style* field.
This wins over both the partner-level and the company-level setting.

----

7. Adding Your Own Template
============================

The three included templates are deliberately compact and live under
``reports/sm_report_template_*.xml``. They share the same building
blocks (header, partner block, lines table, totals, footer) defined
in ``reports/sm_report_layouts.xml``.

To add a fourth template:

1. Add an entry to ``TEMPLATE_SELECTION`` in
   ``models/sm_report_style.py``
2. Create a new ``reports/sm_report_template_yours.xml`` with a
   ``<template id="sm_pro_template_yours">`` matching that key
3. Add the dispatcher branch to
   ``reports/sm_report_layouts.xml`` (``sm_pro_dispatcher``)
4. Reinstall / upgrade the module

----

8. Compatibility & Limitations
===============================

- Tested on **Odoo 19.0 Community & Enterprise**.
- Python: ``num2words`` and ``PyPDF2`` are required;
  ``reportlab`` is optional (needed only for watermark text).
- Watermark *PDF background* and *last-page PDF* are merged via
  PyPDF2 after wkhtmltopdf has rendered the report.
