import base64
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
import qrcode


def generate_pdf_report(profile, report_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('title', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#6E64FF'), spaceAfter=14)
    subtitle_style = ParagraphStyle('subtitle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#9AA3C3'), leading=18)
    normal_style = styles['BodyText']
    normal_style.spaceAfter = 10

    elements = []
    elements.append(Paragraph('CareerForge AI Pro Report', title_style))
    elements.append(Paragraph(f"Candidate: {profile.get('name', 'N/A')}", subtitle_style))
    elements.append(Paragraph(f"Target Role: {profile.get('role', 'N/A')}", subtitle_style))
    elements.append(Spacer(1, 20))

    summary_items = [
        ['Overall Readiness', f"{report_data.get('overall_score', 0)} / 100"],
        ['Dream Company Score', f"{report_data.get('dream_company_readiness', 0)} / 100"],
        ['Success Probability', f"{report_data.get('success_probability', 0)}%"],
        ['Days to Ready', f"{report_data.get('days_to_ready', 0)}"],
    ]

    summary_table = Table(summary_items, colWidths=[170, 220])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#111827')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#334155')),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 22))
    elements.append(Paragraph('Top Recommendations', styles['Heading3']))
    for recommendation in report_data.get('recommendations', []):
        elements.append(Paragraph(f"• {recommendation}", normal_style))

    elements.append(Spacer(1, 16))
    elements.append(Paragraph('Skill Badges', styles['Heading3']))
    badges = report_data.get('skill_badges', [])
    if badges:
        for badge in badges:
            elements.append(Paragraph(f"• {badge}", normal_style))

    elements.append(Spacer(1, 16))
    elements.append(Paragraph('Recruiter Summary', styles['Heading3']))
    summary = report_data.get('summary', {})
    elements.append(Paragraph(f"Level: {summary.get('level', 'N/A')}", normal_style))
    elements.append(Paragraph(f"Recommendation: {summary.get('recommendation', '')}", normal_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_qr_code_data_uri(text):
    qr = qrcode.QRCode(box_size=8, border=1)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    encoded = base64.b64encode(buffer.getvalue()).decode('ascii')
    return f'data:image/png;base64,{encoded}'
