"""Generate professional PDF prescription analysis reports."""
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# ── Palette ───────────────────────────────────────────────────────────────────
TEAL       = colors.HexColor('#0B6E72')
TEAL_LIGHT = colors.HexColor('#E6F4F5')
TEAL_MID   = colors.HexColor('#1A9BA1')
AMBER      = colors.HexColor('#F59E0B')
RED_WARN   = colors.HexColor('#DC2626')
ORANGE_MED = colors.HexColor('#EA580C')
BLUE_INFO  = colors.HexColor('#2563EB')
GREY_LINE  = colors.HexColor('#D1D5DB')
GREY_TEXT  = colors.HexColor('#6B7280')
DARK       = colors.HexColor('#111827')
WHITE      = colors.white


def _styles():
    base = getSampleStyleSheet()
    custom = {
        'title': ParagraphStyle('Title2', parent=base['Normal'],
                                fontSize=22, textColor=WHITE,
                                fontName='Helvetica-Bold', leading=28, alignment=TA_CENTER),
        'subtitle': ParagraphStyle('Subtitle', parent=base['Normal'],
                                   fontSize=10, textColor=colors.HexColor('#CBD5E1'),
                                   fontName='Helvetica', leading=14, alignment=TA_CENTER),
        'section_head': ParagraphStyle('SectionHead', parent=base['Normal'],
                                       fontSize=12, textColor=TEAL,
                                       fontName='Helvetica-Bold', leading=16,
                                       spaceAfter=4),
        'body': ParagraphStyle('Body', parent=base['Normal'],
                               fontSize=9, textColor=DARK,
                               fontName='Helvetica', leading=13),
        'small': ParagraphStyle('Small', parent=base['Normal'],
                                fontSize=8, textColor=GREY_TEXT,
                                fontName='Helvetica', leading=11),
        'warn_high': ParagraphStyle('WarnHigh', parent=base['Normal'],
                                    fontSize=9, textColor=RED_WARN,
                                    fontName='Helvetica-Bold', leading=13),
        'warn_med': ParagraphStyle('WarnMed', parent=base['Normal'],
                                   fontSize=9, textColor=ORANGE_MED,
                                   fontName='Helvetica-Bold', leading=13),
        'warn_info': ParagraphStyle('WarnInfo', parent=base['Normal'],
                                    fontSize=9, textColor=BLUE_INFO,
                                    fontName='Helvetica', leading=13),
        'label': ParagraphStyle('Label', parent=base['Normal'],
                                fontSize=8, textColor=GREY_TEXT,
                                fontName='Helvetica', leading=10),
        'value': ParagraphStyle('Value', parent=base['Normal'],
                                fontSize=9, textColor=DARK,
                                fontName='Helvetica-Bold', leading=13),
        'diet_item': ParagraphStyle('DietItem', parent=base['Normal'],
                                    fontSize=9, textColor=DARK,
                                    fontName='Helvetica', leading=13,
                                    leftIndent=12),
    }
    return custom


def _section_header(title: str, styles: dict) -> list:
    return [
        Spacer(1, 0.3*cm),
        Paragraph(title, styles['section_head']),
        HRFlowable(width='100%', thickness=1, color=TEAL_LIGHT, spaceAfter=4),
    ]


def generate_report(
    patient_info: dict,
    medicines: list[dict],
    disease_result: dict,
    diet: dict,
    interactions: list[dict],
    dosage_warnings: list[dict],
    raw_text: str,
    output_path: str
) -> str:
    """Generate and save a PDF report. Returns the output path."""
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=1.5*cm, bottomMargin=2*cm,
    )
    styles = _styles()
    story = []

    # ── Header Banner (simulated with a table) ────────────────────────────────
    header_data = [[
        Paragraph('RxClear', styles['title']),
    ]]
    sub_data = [[Paragraph('AI-Powered Prescription Analysis Report', styles['subtitle'])]]
    banner = Table(
        [header_data[0], sub_data[0]],
        colWidths=['100%'],
        rowHeights=[30, 18]
    )
    banner.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), TEAL),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 10),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    story.append(banner)
    story.append(Spacer(1, 0.4*cm))

    # ── Meta row: generated date + disclaimer ─────────────────────────────────
    meta = Table([[
        Paragraph(f"Generated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}", styles['small']),
        Paragraph('⚕ For informational purposes only. Consult your doctor.', styles['small']),
    ]], colWidths=['50%', '50%'])
    meta.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
    ]))
    story.append(meta)
    story.append(Spacer(1, 0.3*cm))

    # ── Patient Info ─────────────────────────────────────────────────────────
    story += _section_header('👤  Patient Information', styles)
    pi = patient_info
    info_data = [
        [Paragraph('Name', styles['label']), Paragraph(pi.get('patient_name', '—'), styles['value']),
        Paragraph('Age', styles['label']), Paragraph(pi.get('age', '—'), styles['value']),
        Paragraph('Gender', styles['label']), Paragraph(pi.get('gender', '—'), styles['value'])],

        [Paragraph('Date', styles['label']), Paragraph(pi.get('date', '—'), styles['value']),
        Paragraph('Prescriber', styles['label']), Paragraph(pi.get('prescriber', '—'), styles['value']),
        Paragraph('Refills', styles['label']), Paragraph(pi.get('refills', '0'), styles['value'])],

        [Paragraph('Registration No', styles['label']),
        Paragraph(pi.get('registration_no', '—'), styles['value']),
        Paragraph('Follow-up', styles['label']),
        Paragraph(pi.get('follow_up', '—'), styles['value']),
        '', ''],

        [Paragraph('Diagnosis', styles['label']),
        Paragraph(pi.get('diagnosis', '—'), styles['value']),
        '', '', '', ''],
    ]
    info_table = Table(info_data, colWidths=['12%', '20%', '10%', '22%', '10%', '26%'])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), TEAL_LIGHT),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [TEAL_LIGHT, colors.HexColor('#F0FAFB')]),
        ('GRID', (0, 0), (-1, -1), 0.3, GREY_LINE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)

    # ── Medicines Table ───────────────────────────────────────────────────────
    story += _section_header('💊  Prescription Medicines', styles)
    if medicines:
        col_headers = ['Medicine', 'Dosage', 'Frequency', 'Timing', 'Duration', 'Category']
        med_rows = [col_headers]
        for m in medicines:
            med_rows.append([
                m.get('name', '—'),
                m.get('dosage', '—'),
                m.get('frequency', '—'),
                m.get('timing', '—'),
                m.get('duration', '—'),
                m.get('category', '—'),
            ])
        med_table = Table(med_rows, colWidths=['22%', '12%', '22%', '15%', '12%', '17%'])
        med_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), TEAL),
            ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, TEAL_LIGHT]),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.3, GREY_LINE),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(med_table)
    else:
        story.append(Paragraph('No medicines extracted.', styles['body']))

    # ── Medicine Details ──────────────────────────────────────────────────────
    if medicines:
        story += _section_header('🔬  Medicine Details', styles)
        for m in medicines:
            block = KeepTogether([
                Paragraph("<b>{}</b> {}".format(m['name'], "({})".format(m['generic_name']) if m.get('generic_name') else ''), styles['body']),
                Paragraph(f"Uses: {m.get('uses', '—')}  |  Side Effects: {m.get('side_effects', '—')}", styles['small']),
                Paragraph(f"Max adult dose: {m.get('max_adult_dose', '—')}  |  Max child dose: {m.get('max_child_dose', '—')}", styles['small']),
                Paragraph(f"Contraindications: {m.get('contraindications', '—')}", styles['small']),
                Spacer(1, 0.15*cm),
            ])
            story.append(block)

    # ── Disease Prediction ────────────────────────────────────────────────────
    story += _section_header('🔎  Disease Prediction', styles)
    dr = disease_result
    pred_data = [[
        Paragraph(str(dr.get('top_disease') or 'Not Predicted'), ParagraphStyle('PredName', fontSize=13,
                   fontName='Helvetica-Bold', textColor=TEAL)),
        Paragraph(f"{dr.get('confidence') or 0}% confidence", ParagraphStyle('Conf', fontSize=11,
                   fontName='Helvetica-Bold', textColor=AMBER, alignment=TA_RIGHT)),
    ]]
    pred_table = Table(pred_data, colWidths=['60%', '40%'])
    pred_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), TEAL_LIGHT),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (0, 0), 10),
        ('RIGHTPADDING', (1, 0), (1, 0), 10),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    story.append(pred_table)
    story.append(Spacer(1, 0.2*cm))

    if dr.get('predictions') and len(dr['predictions']) > 1:
        story.append(Paragraph('Other possibilities:', styles['label']))
        for p in dr['predictions'][1:]:
            story.append(Paragraph(f"• {p['disease']} ({p['confidence']:.1f}%)", styles['small']))

    # ── Warnings ──────────────────────────────────────────────────────────────
    all_warnings = interactions + dosage_warnings
    if all_warnings:
        story += _section_header('⚠️  Warnings & Alerts', styles)
        for w in all_warnings:
            sev = w.get('severity', 'INFO')
            style = styles['warn_high'] if sev == 'HIGH' else (
                styles['warn_med'] if sev == 'MEDIUM' else styles['warn_info']
            )
            story.append(Paragraph(w['message'], style))
            story.append(Spacer(1, 0.1*cm))

    # ── Diet Recommendations ──────────────────────────────────────────────────
    story += _section_header('🥗  Diet & Lifestyle Recommendations', styles)
    eat_items = diet.get('eat', [])
    avoid_items = diet.get('avoid', [])
    lifestyle_items = diet.get('lifestyle', [])

    diet_data = []
    max_rows = max(len(eat_items), len(avoid_items), len(lifestyle_items))
    for i in range(max_rows):
        diet_data.append([
            Paragraph(f"✓ {eat_items[i]}" if i < len(eat_items) else '', styles['diet_item']),
            Paragraph(f"✗ {avoid_items[i]}" if i < len(avoid_items) else '', styles['diet_item']),
            Paragraph(f"→ {lifestyle_items[i]}" if i < len(lifestyle_items) else '', styles['diet_item']),
        ])

    if diet_data:
        header_row = [
            Paragraph('✅ Eat', ParagraphStyle('DH', fontName='Helvetica-Bold', fontSize=9,
                       textColor=colors.HexColor('#166534'))),
            Paragraph('❌ Avoid', ParagraphStyle('DH2', fontName='Helvetica-Bold', fontSize=9,
                        textColor=RED_WARN)),
            Paragraph('💪 Lifestyle', ParagraphStyle('DH3', fontName='Helvetica-Bold', fontSize=9,
                        textColor=BLUE_INFO)),
        ]
        diet_table = Table([header_row] + diet_data, colWidths=['33%', '33%', '34%'])
        diet_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F0FFF4')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, colors.HexColor('#FAFAFA')]),
            ('GRID', (0, 0), (-1, -1), 0.3, GREY_LINE),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(diet_table)

    # ── OCR Text ──────────────────────────────────────────────────────────────
    if raw_text:
        story += _section_header('📄  Extracted Prescription Text (OCR)', styles)
        ocr_para = Paragraph(raw_text.replace('\n', '<br/>'), styles['small'])
        ocr_box = Table([[ocr_para]], colWidths=['100%'])
        ocr_box.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')),
            ('BOX', (0, 0), (-1, -1), 0.5, GREY_LINE),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(ocr_box)

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    footer_line = HRFlowable(width='100%', thickness=0.5, color=GREY_LINE)
    story.append(footer_line)
    story.append(Paragraph(
        'This report is AI-generated and is for informational purposes only. '
        'It does not replace professional medical advice, diagnosis, or treatment. '
        'Always consult a licensed healthcare provider.',
        styles['small']
    ))

    doc.build(story)
    return output_path
