import os
from print_bill import print_invoice
import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from payments_insert import loc
import os
import sys

# 1. Add the root project directory ('just a cs project') to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 2. Import your database modules
from main_code.database_connections.database_connect import establish_conn, cursor, conn
from main_code.database_connections.Database_end import end_connection

# 1. Prompt user for the Payment ID at runtime
target_payment_id = loc

connection = None
cursor = None

try:
    establish_conn()
    
    cursor = conn.cursor(dictionary=True)
    
    # 3. Fetch the live record from the database
    query = "SELECT * FROM payments WHERE PAYMENT_ID = %s"
    cursor.execute(query, (target_payment_id,))
    record = cursor.fetchone()
    
    if not record:
        print(f"\nNo payment record found with ID: {target_payment_id}")
    else:
        output_folder = "invoices"  # Or an absolute path like "C:/Users/LENOVO/Desktop/Invoices"
        
        # Create the folder if it doesn't already exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Combine the folder path and filename securely
        filename = os.path.join(output_folder, f"Invoice_{record['PAYMENT_ID']}.pdf")
        
        # Setup document layout
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'InvoiceTitle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#1E293B'),
            alignment=1, # Centered
            spaceAfter=15
        )
        
        body_style = ParagraphStyle(
            'InvoiceBody',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#334155'),
            leading=16
        )
        
        bold_style = ParagraphStyle(
            'InvoiceBold',
            parent=body_style,
            fontName='Helvetica-Bold'
        )
        
        right_bold = ParagraphStyle(
            'RightBold',
            parent=bold_style,
            alignment=2 # Right
        )

        # Header Title
        story.append(Paragraph("OFFICIAL INVOICE / RECEIPT", title_style))
        story.append(Spacer(1, 10))
        
        # Meta info block (Invoice ID & Date)
        meta_data = [
            [Paragraph(f"<b>Payment ID:</b> {record['PAYMENT_ID']}", body_style),
             Paragraph(f"<b>Date:</b> {record['PAYMENT_DATE']}", right_bold)]
        ]
        meta_table = Table(meta_data, colWidths=[3.25 * inch, 3.25 * inch])
        meta_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(meta_table)
        
        # Customer Info block
        cust_data = [
            [Paragraph("<b>Billed To:</b>", bold_style)],
            [Paragraph(f"{record['PERSON_NAME']}", body_style)],
        ]
        cust_table = Table(cust_data, colWidths=[6.5 * inch])
        cust_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('PADDING', (0,0), (-1,-1), 8),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ]))
        story.append(cust_table)
        story.append(Spacer(1, 15))
        
        # Line Items Table Header & Row
        table_data = [
            ["Description / Product Details", "Type / Method", "Amount"],
            [
                Paragraph(f"<b>{record['PRODUCT_NAME']}</b><br/>Brand: {record['PRODUCT_BRAND']}<br/><font color='#64748B'>{record['DESCRIPTION']}</font>", body_style),
                Paragraph(f"{record['PAYMENT_TYPE']}<br/>({record['PAYMENT_METHOD']})", body_style),
                Paragraph(f"${record['AMOUNT']:,.2f}", right_bold)
            ]
        ]
        
        item_table = Table(table_data, colWidths=[3.5 * inch, 1.5 * inch, 1.5 * inch])
        item_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('TOPPADDING', (0,0), (-1,0), 8),
            ('ALIGN', (2,0), (2,-1), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFFFFF')),
            ('PADDING', (0,1), (-1,1), 10),
        ]))
        story.append(item_table)
        story.append(Spacer(1, 15))
        
        # Total Summary Table
        total_data = [
            ["Total Paid:", f"${record['AMOUNT']:,.2f}"]
        ]
        total_table = Table(total_data, colWidths=[5.0 * inch, 1.5 * inch])
        total_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#E2E8F0')),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 11),
            ('ALIGN', (1,0), (1,-1), 'RIGHT'),
            ('PADDING', (0,0), (-1,-1), 8),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ]))
        story.append(total_table)
        story.append(Spacer(1, 40))
        
        # Footer / Thank You note
        footer_style = ParagraphStyle(
            'InvoiceFooter',
            parent=body_style,
            alignment=1,
            textColor=colors.HexColor('#64748B'),
            fontSize=10
        )
        story.append(Paragraph("Thank you for your business!", footer_style))
        
        # Build the PDF and save it locally
        doc.build(story)
        print(f"\nSuccess! PDF saved locally as: {filename}")

        print_invoice(filename)

except mysql.connector.Error as err:
    print(f"Database Error: {err}")
    
finally:
    # Safely close database connections
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()