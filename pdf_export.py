from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from datetime import datetime
import io

def generate_compatibility_pdf(chem1, chem2, category1, category2, status, penjelasan, penyimpanan):
    """
    Generate PDF report untuk hasil analisis kompatibilitas
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#00d4ff'),
        spaceAfter=30,
        alignment=1
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#00d4ff'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    elements.append(Paragraph("FCOT Chemical System PRO", title_style))
    elements.append(Paragraph("Laporan Analisis Kompatibilitas Bahan Kimia", styles['Heading2']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Info Section
    elements.append(Paragraph("Informasi Analisis", heading_style))
    info_data = [
        ['Tanggal Analisis:', datetime.now().strftime("%d-%m-%Y %H:%M:%S")],
        ['Bahan Kimia 1:', chem1],
        ['Kategori 1:', category1],
        ['Bahan Kimia 2:', chem2],
        ['Kategori 2:', category2],
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#16213e')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Status Section
    elements.append(Paragraph("Status Kompatibilitas", heading_style))
    status_text = status.replace('❌ ', '').replace('⚠️ ', '').replace('✅ ', '')
    
    # Determine color based on status
    if "BERBAHAYA" in status:
        status_color = colors.HexColor('#ff006e')
    elif "AMAN" in status:
        status_color = colors.HexColor('#00d97e')
    else:
        status_color = colors.HexColor('#ffa500')
    
    status_para = Paragraph(f"<b>{status_text}</b>", styles['Normal'])
    status_table = Table([[status_para]], colWidths=[6*inch])
    status_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), status_color),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('PADDING', (0, 0), (-1, -1), 20),
    ]))
    elements.append(status_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Explanation
    elements.append(Paragraph("Penjelasan Hasil", heading_style))
    elements.append(Paragraph(penjelasan, styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Storage Recommendation
    elements.append(Paragraph("Rekomendasi Penyimpanan", heading_style))
    elements.append(Paragraph(penyimpanan, styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Footer
    elements.append(Spacer(1, 0.3*inch))
    footer_text = "Aplikasi ini dikembangkan oleh FCOT Chemical System. Untuk operasi industri, konsultasi dengan ahli keselamatan profesional."
    elements.append(Paragraph(footer_text, ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=1
    )))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def generate_history_pdf(df):
    """
    Generate PDF report untuk riwayat analisis
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#00d4ff'),
        spaceAfter=20,
        alignment=1
    )
    
    # Title
    elements.append(Paragraph("LAPORAN RIWAYAT ANALISIS", title_style))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Convert dataframe to table
    data = [df.columns.tolist()] + df.values.tolist()
    table = Table(data, colWidths=[1.2*inch, 1.8*inch, 1.8*inch, 1*inch, 1*inch, 0.8*inch])
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00d4ff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer
