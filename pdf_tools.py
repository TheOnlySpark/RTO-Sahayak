"""
PDF Tools module for RTO Sahayak.

Generates structured citizen consultation handoff summary PDFs using ReportLab.
Adheres to project rules:
- Strictly synthetic citizen data.
- Top banner: "DRAFT - for citizen review and officer verification".
- Mandatory sections: citizen summary (SYNTHETIC), checklist status,
  document mismatches (facts only), estimated fees (marked as estimates),
  rule sources, next steps.
- Footer on every page: "Final decision rests with the RTO officer."
- Mask ID numbers (Aadhaar, PAN, DL, Voter ID, etc.).
- Saves generated PDF to outputs/.
"""

from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

MANDATORY_BANNER = "DRAFT - for citizen review and officer verification"
MANDATORY_FOOTER = "Final decision rests with the RTO officer."
SYNTHETIC_LABEL = "SYNTHETIC"


def mask_id_number(val: Any) -> str:
    """
    Mask sensitive citizen identification numbers to preserve privacy.
    Preserves at most the final 4 alphanumeric characters, masking preceding
    characters with 'X'. Handles Aadhaar, PAN, DL, EPIC, and generic IDs.
    """
    if val is None:
        return ""
    raw = str(val).strip()
    if not raw or len(raw) <= 4:
        return raw

    # 1. Formatted Aadhaar: XXXX-XXXX-1234 or XXXX XXXX 1234
    m_aadhaar = re.match(r'^(\d{4})([\s\-])(\d{4})([\s\-])(\d{4})$', raw)
    if m_aadhaar:
        sep1, sep2, last4 = m_aadhaar.group(2), m_aadhaar.group(4), m_aadhaar.group(5)
        return f"XXXX{sep1}XXXX{sep2}{last4}"

    # 2. Raw 12-digit Aadhaar: 123456781234
    if re.match(r'^\d{12}$', raw):
        return f"XXXX-XXXX-{raw[-4:]}"

    # 3. Standard Indian PAN: 5 uppercase letters + 4 digits + 1 letter (e.g. ABCDE1234F)
    m_pan = re.match(r'^([A-Z]{5})(\d{4})([A-Z])$', raw, re.IGNORECASE)
    if m_pan:
        return f"XXXXX{m_pan.group(2)}{m_pan.group(3).upper()}"

    # 4. Prefixed fake IDs like FAKE-DL-DL04-20150001 or FAKE-UID-9999-8888-7777
    if "FAKE-" in raw.upper():
        parts = raw.split("-")
        if len(parts) >= 2:
            last_part = parts[-1]
            masked_middle = "-".join(["XXXX" for _ in parts[1:-1]])
            if masked_middle:
                return f"{parts[0]}-{masked_middle}-{last_part}"
            return f"{parts[0]}-XXXX-{last_part}"

    # 5. Generic alphanumeric ID with hyphens or spaces
    clean_chars = [c for c in raw if c.isalnum()]
    if len(clean_chars) >= 8:
        # Keep last 4 alphanumeric characters, mask earlier characters
        keep_last = 4
        seen_from_end = 0
        masked_chars = []
        for c in reversed(raw):
            if c.isalnum():
                seen_from_end += 1
                if seen_from_end <= keep_last:
                    masked_chars.append(c)
                else:
                    masked_chars.append("X")
            else:
                masked_chars.append(c)
        return "".join(reversed(masked_chars))

    # Short ID: mask all but last 2
    if len(raw) > 4:
        return ("X" * (len(raw) - 4)) + raw[-4:]
    return raw


def _find_outputs_dir() -> Path:
    """Resolve and ensure the outputs/ directory exists."""
    here = Path(__file__).resolve().parent
    outputs_dir = here / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    return outputs_dir


# Try importing ReportLab
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
        KeepTogether,
        HRFlowable,
    )
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class _NumberedCanvas:
    """Canvas wrapper that adds running header banner and mandatory footer to every page."""

    def __init__(self, *args, **kwargs):
        pass


def _generate_with_reportlab(summary: dict, output_path: Path) -> str:
    """Generate high-quality PDF using ReportLab Flowables."""
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=45,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#475569"),
        spaceAfter=10,
    )
    section_h_style = ParagraphStyle(
        "SectionH",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=8,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1e293b"),
    )
    body_bold = ParagraphStyle(
        "DocBodyBold",
        parent=body_style,
        fontName="Helvetica-Bold",
    )
    notice_style = ParagraphStyle(
        "DocNotice",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=4,
    )

    story = []

    # 1. Top Banner Flowable
    banner_data = [[Paragraph(f"<b>*** {MANDATORY_BANNER} ***</b>", ParagraphStyle(
        "BannerText",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        textColor=colors.white,
        alignment=1,
    ))]]
    banner_table = Table(banner_data, colWidths=[540])
    banner_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#991b1b")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 8))

    # Header Title
    service_title = summary.get("service_name", summary.get("service", "RTO Consultation & Verification"))
    story.append(Paragraph("RTO Sahayak — Citizen Consultation & Handoff Summary", title_style))
    ref_id = mask_id_number(summary.get("reference_id", summary.get("ref_id", "SYNTH-CONSULT-001")))
    created_at = summary.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M"))
    story.append(Paragraph(
        f"<b>Service:</b> {service_title} | <b>Reference ID:</b> {ref_id} | <b>Generated:</b> {created_at} | <b>Status:</b> DRAFT",
        subtitle_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=8))

    # =========================================================================
    # SECTION 1: CITIZEN SUMMARY (SYNTHETIC)
    # =========================================================================
    story.append(Paragraph(f"1. Citizen Summary ({SYNTHETIC_LABEL})", section_h_style))
    story.append(Paragraph("All data presented below is purely synthetic for demonstration and testing purposes.", notice_style))

    c_sum = summary.get("citizen_summary", {})
    if not isinstance(c_sum, dict):
        c_sum = {}

    name = summary.get("citizen_name", c_sum.get("name", c_sum.get("full_name", "Rahul Kumar Sharma")))
    dob = c_sum.get("dob", c_sum.get("date_of_birth", "1995-05-15"))
    father = c_sum.get("father_name", c_sum.get("father", "Suresh Kumar Sharma"))
    address = c_sum.get("address", "123, Gandhi Marg, Synthetic City, New Delhi - 110001")
    raw_id = c_sum.get("id_number", c_sum.get("document_number", summary.get("id_number", "FAKE-DL-DL04-20150001")))
    masked_id = mask_id_number(raw_id)

    cit_rows = [
        [Paragraph("<b>Full Name:</b>", body_style), Paragraph(f"{name} ({SYNTHETIC_LABEL})", body_style),
         Paragraph("<b>Date of Birth:</b>", body_style), Paragraph(str(dob), body_style)],
        [Paragraph("<b>Father's Name:</b>", body_style), Paragraph(str(father), body_style),
         Paragraph("<b>Document ID (Masked):</b>", body_style), Paragraph(masked_id, body_style)],
        [Paragraph("<b>Address:</b>", body_style), Paragraph(str(address), body_style),
         Paragraph("<b>Record Type:</b>", body_style), Paragraph(f"Synthetic Mock Record", body_style)],
    ]
    cit_table = Table(cit_rows, colWidths=[100, 170, 130, 140])
    cit_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(cit_table)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 2: CHECKLIST STATUS
    # =========================================================================
    story.append(Paragraph("2. Checklist Status", section_h_style))
    checklist = summary.get("checklist", [
        {"document": "Application Form 2", "status": "Submitted", "note": "Synthetic submission"},
        {"document": "Proof of Age (Aadhaar / Birth Certificate)", "status": "Submitted", "note": "Synthetic mock"},
        {"document": "Proof of Address", "status": "Submitted", "note": "Synthetic mock"},
        {"document": "Medical Fitness (Form 1 / 1A)", "status": "Pending", "note": "Required for transport or age > 40"},
    ])

    chk_rows = [[
        Paragraph("<b>Document / Item</b>", body_bold),
        Paragraph("<b>Status</b>", body_bold),
        Paragraph("<b>Remarks</b>", body_bold),
    ]]
    for item in checklist:
        doc_name = item.get("document", item.get("name", "Document"))
        status = item.get("status", "Verified")
        remarks = item.get("remarks", item.get("note", "Factual item status"))
        chk_rows.append([
            Paragraph(str(doc_name), body_style),
            Paragraph(f"<b>{status}</b>", body_style),
            Paragraph(str(remarks), body_style),
        ])

    chk_table = Table(chk_rows, colWidths=[200, 100, 240])
    chk_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(chk_table)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 3: DOCUMENT MISMATCHES (FACTS ONLY)
    # =========================================================================
    story.append(Paragraph("3. Document Discrepancy Analysis (Factual Comparison Only)", section_h_style))
    story.append(Paragraph(
        "Factual record comparison across presented documents. Does not declare eligibility or document validity. "
        "Final decision rests with the RTO officer.",
        notice_style,
    ))

    mismatches = summary.get("mismatches", [])
    if mismatches:
        mis_rows = [[
            Paragraph("<b>Field Name</b>", body_bold),
            Paragraph("<b>Document A</b>", body_bold),
            Paragraph("<b>Value in Doc A</b>", body_bold),
            Paragraph("<b>Document B</b>", body_bold),
            Paragraph("<b>Value in Doc B</b>", body_bold),
        ]]
        for m in mismatches:
            f_name = m.get("field", "Attribute")
            d_a = m.get("doc_a", "Document 1")
            v_a = mask_id_number(m.get("value_a", "")) if "id" in str(f_name).lower() or "number" in str(f_name).lower() else m.get("value_a", "")
            d_b = m.get("doc_b", "Document 2")
            v_b = mask_id_number(m.get("value_b", "")) if "id" in str(f_name).lower() or "number" in str(f_name).lower() else m.get("value_b", "")
            mis_rows.append([
                Paragraph(str(f_name), body_style),
                Paragraph(str(d_a), body_style),
                Paragraph(str(v_a), body_style),
                Paragraph(str(d_b), body_style),
                Paragraph(str(v_b), body_style),
            ])
        mis_table = Table(mis_rows, colWidths=[110, 100, 115, 100, 115])
        mis_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#fef2f2")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#fca5a5")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#fee2e2")),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        story.append(mis_table)
    else:
        story.append(Paragraph("Zero factual document discrepancies identified across citizen documents.", body_style))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 4: ESTIMATED FEES (MARKED AS ESTIMATES)
    # =========================================================================
    story.append(Paragraph("4. Estimated Fees (Placeholder Estimates)", section_h_style))
    story.append(Paragraph("ESTIMATE ONLY — Placeholder figures subject to human verification and official RTO fee schedule.", notice_style))

    est_fees = summary.get("estimated_fees", {})
    fee_items = []
    total_val = "₹0"
    if isinstance(est_fees, dict):
        fee_items = est_fees.get("items", [
            {"service": "Application / Form Fee", "amount": "₹200 (ESTIMATE)"},
            {"service": "Test / Verification Fee", "amount": "₹300 (ESTIMATE)"},
            {"service": "Smart Card / Processing Fee", "amount": "₹200 (ESTIMATE)"},
        ])
        total_val = est_fees.get("total", "₹700 (ESTIMATE)")
    elif isinstance(est_fees, list):
        fee_items = est_fees

    fee_rows = [[
        Paragraph("<b>Fee Component / Service</b>", body_bold),
        Paragraph("<b>Estimated Amount</b>", body_bold),
        Paragraph("<b>Status / Verification Notice</b>", body_bold),
    ]]
    for item in fee_items:
        s_name = item.get("service", item.get("name", "Service Component"))
        amt = item.get("amount", "₹200 (ESTIMATE)")
        fee_rows.append([
            Paragraph(str(s_name), body_style),
            Paragraph(str(amt), body_style),
            Paragraph("PLACEHOLDER: verify against official sources", notice_style),
        ])
    fee_rows.append([
        Paragraph("<b>Total Estimated Outlay:</b>", body_bold),
        Paragraph(f"<b>{total_val}</b>", body_bold),
        Paragraph("Payable at authorized RTO counter only", notice_style),
    ])

    fee_table = Table(fee_rows, colWidths=[240, 130, 170])
    fee_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(fee_table)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 5: RULE SOURCES
    # =========================================================================
    story.append(Paragraph("5. Rule Sources & References", section_h_style))
    sources = summary.get("rule_sources", [
        "data/rules/ll_to_dl_process.md",
        "data/rules/documents_checklist.md",
        "data/rules/fees_overview.md",
    ])
    for src in sources:
        story.append(Paragraph(f"• Cites reference rule file: <code>{src}</code>", body_style))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 6: NEXT STEPS
    # =========================================================================
    story.append(Paragraph("6. Next Steps for Citizen", section_h_style))
    next_steps = summary.get("next_steps", [
        "Book an appointment slot at the designated RTO through Parivahan Sewa.",
        "Bring original physical documents and identity cards for officer in-person verification.",
        "Complete biometric authentication and required evaluation at the RTO center.",
        "Pay statutory official fees directly at the authorized RTO payment counter.",
    ])
    for idx, step in enumerate(next_steps, 1):
        story.append(Paragraph(f"{idx}. {step}", body_style))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=6))
    story.append(Paragraph(
        f"<b>IMPORTANT NOTICE:</b> This summary is an automated informational draft prepared for citizen review. "
        f"It does not constitute government approval or formal application filing. "
        f"<b>{MANDATORY_FOOTER}</b>",
        notice_style,
    ))

    # Page callback function for header and footer on every page
    def _draw_page_decorations(canvas_obj, document):
        canvas_obj.saveState()
        canvas_obj.setFont("Helvetica-Bold", 8)
        canvas_obj.setFillColor(colors.HexColor("#991b1b"))
        # Top banner text (running)
        canvas_obj.drawCentredString(letter[0] / 2.0, letter[1] - 25, f"*** {MANDATORY_BANNER} ***")

        # Thin footer rule
        canvas_obj.setStrokeColor(colors.HexColor("#94a3b8"))
        canvas_obj.setLineWidth(0.5)
        canvas_obj.line(36, 32, letter[0] - 36, 32)

        # Footer text
        canvas_obj.setFont("Helvetica-Oblique", 8)
        canvas_obj.setFillColor(colors.HexColor("#475569"))
        canvas_obj.drawString(36, 20, MANDATORY_FOOTER)

        page_str = f"Page {document.page}"
        canvas_obj.drawRightString(letter[0] - 36, 20, page_str)
        canvas_obj.restoreState()

    doc.build(story, onFirstPage=_draw_page_decorations, onLaterPages=_draw_page_decorations)
    return str(output_path)


def _generate_pure_python_fallback_pdf(summary: dict, output_path: Path) -> str:
    """
    Self-contained pure-Python standard PDF generator used if ReportLab is missing.
    Produces authentic, valid %PDF-1.4 binary file with banner, all 6 sections,
    masked ID numbers, and mandatory footer.
    """
    service_title = summary.get("service_name", summary.get("service", "RTO Consultation Summary"))
    ref_id = mask_id_number(summary.get("reference_id", summary.get("ref_id", "SYNTH-REF-001")))
    c_sum = summary.get("citizen_summary", {})
    name = summary.get("citizen_name", c_sum.get("name", c_sum.get("full_name", "Rahul Kumar Sharma")))
    dob = c_sum.get("dob", c_sum.get("date_of_birth", "1995-05-15"))
    father = c_sum.get("father_name", c_sum.get("father", "Suresh Kumar Sharma"))
    raw_id = c_sum.get("id_number", c_sum.get("document_number", "FAKE-DL-DL04-20150001"))
    masked_id = mask_id_number(raw_id)

    lines = [
        f"*** {MANDATORY_BANNER} ***",
        "",
        "RTO Sahayak - Citizen Consultation & Handoff Summary",
        f"Service: {service_title} | Ref: {ref_id} | Status: DRAFT",
        "--------------------------------------------------------------------------------",
        f"1. Citizen Summary ({SYNTHETIC_LABEL})",
        f"   Full Name: {name} ({SYNTHETIC_LABEL})",
        f"   Date of Birth: {dob}",
        f"   Father's Name: {father}",
        f"   Document ID (Masked): {masked_id}",
        "",
        "2. Checklist Status",
    ]

    for item in summary.get("checklist", [{"document": "Application Form 2", "status": "Submitted"}]):
        d = item.get("document", "Doc")
        s = item.get("status", "Submitted")
        lines.append(f"   - {d}: {s}")

    lines.extend([
        "",
        "3. Document Discrepancy Analysis (Factual Comparison Only)",
    ])
    mismatches = summary.get("mismatches", [])
    if mismatches:
        for m in mismatches:
            fld = m.get("field", "Field")
            v_a = mask_id_number(m.get("value_a", "")) if "id" in str(fld).lower() else m.get("value_a", "")
            v_b = mask_id_number(m.get("value_b", "")) if "id" in str(fld).lower() else m.get("value_b", "")
            lines.append(f"   - Discrepancy on '{fld}': {m.get('doc_a')}='{v_a}' vs {m.get('doc_b')}='{v_b}'")
    else:
        lines.append("   Zero document discrepancies identified across citizen documents.")

    lines.extend([
        "",
        "4. Estimated Fees (Placeholder Estimates)",
        "   ESTIMATE ONLY - Placeholder figures subject to official RTO schedule.",
    ])
    est_fees = summary.get("estimated_fees", {})
    if isinstance(est_fees, dict):
        items = est_fees.get("items", [{"service": "Application Fee", "amount": "₹200 (ESTIMATE)"}])
        for it in items:
            lines.append(f"   - {it.get('service')}: {it.get('amount')}")
        lines.append(f"   Total Estimated Outlay: {est_fees.get('total', '₹700 (ESTIMATE)')}")

    lines.extend([
        "",
        "5. Rule Sources & References",
    ])
    for src in summary.get("rule_sources", ["data/rules/ll_to_dl_process.md"]):
        lines.append(f"   - {src}")

    lines.extend([
        "",
        "6. Next Steps for Citizen",
    ])
    for idx, st in enumerate(summary.get("next_steps", ["Book appointment slot", "Bring original documents"]), 1):
        lines.append(f"   {idx}. {st}")

    lines.extend([
        "",
        "--------------------------------------------------------------------------------",
        f"Notice: {MANDATORY_FOOTER}",
    ])

    # Assemble PDF text stream with PDF font operators
    stream_lines = ["BT", "/F1 9 Tf", "40 760 Td", "12 TL"]
    for l in lines:
        safe_l = l.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream_lines.append(f"({safe_l}) '")
    stream_lines.append("ET")
    content_stream = "\n".join(stream_lines).encode("latin1")

    objects = []
    # Obj 1: Catalog
    objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    # Obj 2: Pages
    objects.append(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
    # Obj 3: Page
    objects.append(b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n")
    # Obj 4: Content stream
    stream_len = len(content_stream)
    obj4 = f"4 0 obj\n<< /Length {stream_len} >>\nstream\n".encode("latin1") + content_stream + b"\nendstream\nendobj\n"
    objects.append(obj4)
    # Obj 5: Font
    objects.append(b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")

    # Build PDF with xref table
    header = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
    offsets = [len(header)]
    body = b""
    for obj in objects:
        offsets.append(offsets[-1] + len(obj))
        body += obj

    xref_offset = offsets[-1]
    xref = f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("latin1")
    for off in offsets[:-1]:
        xref += f"{off:010d} 00000 n \n".encode("latin1")

    trailer = f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("latin1")

    pdf_bytes = header + body + xref + trailer
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)

    return str(output_path)


def generate_handoff_pdf(summary: dict) -> Dict[str, str]:
    """
    Generate a citizen consultation handoff summary PDF.

    Args:
        summary: Dictionary with keys:
            - citizen_name: str
            - service_name: str (optional)
            - citizen_summary: dict (full_name, dob, father_name, address, id_number)
            - checklist: list of dicts (document, status)
            - mismatches: list of dicts (field, doc_a, value_a, doc_b, value_b)
            - estimated_fees: dict (items, total)
            - rule_sources: list of str
            - next_steps: list of str
            - output_filename: str (optional)

    Returns:
        Dict: {"pdf_path": <resolved_file_path_string>}
    """
    outputs_dir = _find_outputs_dir()

    custom_name = summary.get("output_filename")
    if custom_name and isinstance(custom_name, str) and custom_name.strip():
        safe_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', custom_name.strip())
        if not safe_name.endswith(".pdf"):
            safe_name += ".pdf"
        target_path = outputs_dir / safe_name
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_path = outputs_dir / f"handoff_summary_{timestamp}.pdf"

    if REPORTLAB_AVAILABLE:
        try:
            pdf_path_str = _generate_with_reportlab(summary, target_path)
            return {"pdf_path": str(Path(pdf_path_str).resolve())}
        except Exception:
            # Graceful fallback to pure-python engine if ReportLab encounters a runtime environment issue
            pdf_path_str = _generate_pure_python_fallback_pdf(summary, target_path)
            return {"pdf_path": str(Path(pdf_path_str).resolve())}
    else:
        pdf_path_str = _generate_pure_python_fallback_pdf(summary, target_path)
        return {"pdf_path": str(Path(pdf_path_str).resolve())}


if __name__ == "__main__":
    sample_summary = {
        "citizen_name": "Rahul Kumar Sharma",
        "service_name": "Learner Licence to Driving Licence",
        "citizen_summary": {
            "full_name": "Rahul Kumar Sharma",
            "date_of_birth": "1995-05-15",
            "father_name": "Suresh Kumar Sharma",
            "address": "123, Gandhi Marg, Synthetic City, New Delhi - 110001",
            "id_number": "FAKE-DL-DL04-20150001",
        },
        "checklist": [
            {"document": "Form 2 Application", "status": "Submitted"},
            {"document": "Learner Licence Copy", "status": "Submitted"},
            {"document": "Medical Fitness Certificate", "status": "Pending"},
        ],
        "mismatches": [
            {
                "field": "date_of_birth",
                "doc_a": "Driving Licence",
                "value_a": "1995-05-15",
                "doc_b": "Aadhaar Card",
                "value_b": "1993-05-15",
            }
        ],
        "estimated_fees": {
            "items": [
                {"service": "Application Fee", "amount": "₹200 (ESTIMATE)"},
                {"service": "Driving Test Fee", "amount": "₹300 (ESTIMATE)"},
                {"service": "Smart Card Fee", "amount": "₹200 (ESTIMATE)"},
            ],
            "total": "₹700 (ESTIMATE)",
        },
        "rule_sources": [
            "data/rules/ll_to_dl_process.md",
            "data/rules/documents_checklist.md",
            "data/rules/fees_overview.md",
        ],
        "next_steps": [
            "Book an appointment slot at RTO Synthetic Zone 04.",
            "Bring physical original identity documents for officer verification.",
            "Pay statutory fee at authorized RTO counter.",
        ],
        "output_filename": "sample_handoff.pdf",
    }
    res = generate_handoff_pdf(sample_summary)
    print("Generated PDF:", res)
