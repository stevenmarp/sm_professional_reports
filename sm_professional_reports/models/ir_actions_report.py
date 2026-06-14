# -*- coding: utf-8 -*-
"""Post-process generated PDFs: add watermark text + last-page PDF append.

The watermark PDF (background) is handled at the QWeb level via a CSS
``background-image`` so that wkhtmltopdf rasterizes it correctly. The
text watermark and the optional last-page PDF append are applied here
on the final ``pdf_content`` because they require true PDF manipulation.
"""
import io
import logging

from odoo import models

_logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    # Reports rendered by this module use this prefix in their report_name.
    _SM_PRO_PREFIX = 'sm_professional_reports.'

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        pdf_content, report_type = super()._render_qweb_pdf(
            report_ref, res_ids=res_ids, data=data,
        )
        if report_type != 'pdf':
            return pdf_content, report_type

        try:
            report_sudo = self._get_report(report_ref)
        except Exception:
            return pdf_content, report_type

        report_name = report_sudo.report_name or ''
        if not report_name.startswith(self._SM_PRO_PREFIX):
            return pdf_content, report_type

        # Resolve style from first record (single-record print is the common case)
        style = self.env['sm.report.style']
        document = None
        if res_ids:
            try:
                document = self.env[report_sudo.model].browse(res_ids[0])
                style = self.env['sm.report.style'].get_style_for(document)
            except Exception as exc:
                _logger.debug("sm_professional_reports: cannot resolve style: %s", exc)

        if not style:
            return pdf_content, report_type

        try:
            pdf_content = self._sm_pro_postprocess_pdf(pdf_content, style, document)
        except Exception as exc:
            _logger.warning(
                "sm_professional_reports: PDF post-processing failed (%s). "
                "Returning the original PDF.", exc,
            )

        return pdf_content, report_type

    # ------------------------------------------------------------------
    #  PDF post-processing helpers
    # ------------------------------------------------------------------

    def _sm_pro_postprocess_pdf(self, pdf_content, style, document):
        """Apply text watermark and append the last-page PDF."""
        try:
            from PyPDF2 import PdfFileReader, PdfFileWriter
            new_api = False
        except ImportError:
            try:
                from PyPDF2 import PdfReader as PdfFileReader  # type: ignore
                from PyPDF2 import PdfWriter as PdfFileWriter  # type: ignore
                new_api = True
            except ImportError:
                _logger.warning(
                    "sm_professional_reports: PyPDF2 not available, cannot "
                    "post-process PDF.")
                return pdf_content

        # 1) Watermark text -> generate a transparent overlay PDF and merge
        watermark_overlay_bytes = None
        watermark_text = style.render_watermark_text(document)
        if watermark_text:
            watermark_overlay_bytes = self._sm_pro_build_text_watermark(
                watermark_text,
                color=style.watermark_text_color or '#cccccc',
                size=style.watermark_text_size or 64,
            )

        if not watermark_overlay_bytes and not style.last_page_pdf \
                and not style.watermark_pdf:
            return pdf_content

        try:
            base_reader = PdfFileReader(io.BytesIO(pdf_content), strict=False)
            writer = PdfFileWriter()

            text_overlay_page = None
            if watermark_overlay_bytes:
                wm_reader = PdfFileReader(
                    io.BytesIO(watermark_overlay_bytes), strict=False)
                text_overlay_page = (
                    wm_reader.pages[0] if new_api else wm_reader.getPage(0)
                )

            bg_page = None
            if style.watermark_pdf:
                import base64
                bg_bytes = base64.b64decode(style.watermark_pdf)
                bg_reader = PdfFileReader(io.BytesIO(bg_bytes), strict=False)
                bg_page = bg_reader.pages[0] if new_api else bg_reader.getPage(0)

            num_pages = len(base_reader.pages) if new_api else base_reader.getNumPages()
            for i in range(num_pages):
                page = base_reader.pages[i] if new_api else base_reader.getPage(i)

                # Background letterhead: merge the *page* on top of the
                # background to keep the report content visible.
                if bg_page is not None:
                    try:
                        # Copy the background then overlay our page
                        from copy import copy as _copy
                        merged_bg = _copy(bg_page)
                        if new_api:
                            merged_bg.merge_page(page)
                        else:
                            merged_bg.mergePage(page)
                        page = merged_bg
                    except Exception:  # pragma: no cover
                        pass

                if text_overlay_page is not None:
                    try:
                        if new_api:
                            page.merge_page(text_overlay_page)
                        else:
                            page.mergePage(text_overlay_page)
                    except Exception:  # pragma: no cover
                        pass

                if new_api:
                    writer.add_page(page)
                else:
                    writer.addPage(page)

            # Append last-page PDF
            if style.last_page_pdf:
                import base64
                lp_bytes = base64.b64decode(style.last_page_pdf)
                lp_reader = PdfFileReader(io.BytesIO(lp_bytes), strict=False)
                lp_pages = (
                    len(lp_reader.pages) if new_api else lp_reader.getNumPages()
                )
                for i in range(lp_pages):
                    page = lp_reader.pages[i] if new_api else lp_reader.getPage(i)
                    if new_api:
                        writer.add_page(page)
                    else:
                        writer.addPage(page)

            out = io.BytesIO()
            writer.write(out)
            return out.getvalue()
        except Exception as exc:
            _logger.warning(
                "sm_professional_reports: failed to merge watermark/last-page "
                "(%s). Returning original PDF.", exc)
            return pdf_content

    def _sm_pro_build_text_watermark(self, text, color='#cccccc', size=64):
        """Generate a single-page transparent PDF with diagonal watermark text."""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.colors import HexColor
        except ImportError:
            _logger.info(
                "sm_professional_reports: reportlab not installed, "
                "watermark text will be skipped.")
            return None

        try:
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=A4)
            width, height = A4
            try:
                c.setFillColor(HexColor(color))
            except Exception:
                c.setFillColor(HexColor('#cccccc'))
            c.setFont("Helvetica-Bold", size)
            c.saveState()
            c.translate(width / 2, height / 2)
            c.rotate(45)
            c.drawCentredString(0, 0, text)
            c.restoreState()
            c.showPage()
            c.save()
            return buf.getvalue()
        except Exception as exc:
            _logger.debug("watermark text generation failed: %s", exc)
            return None
