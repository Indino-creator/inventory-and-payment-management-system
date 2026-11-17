import os
import sys
import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Add the root project directory to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main_code.database_connections.database_connect import establish_conn, cursor, conn
from main_code.database_connections.Database_end import end_connection
from print_bill import print_invoice

print("--- Payment, Inventory Update & Invoice Generation System ---")

# 1. Gather User Inputs
person_name = input("Enter the name of the person: ").strip()
product_name = input("Enter the product name: ").strip()
product_brand = input("Enter the product brand: ").strip()
quantity_bought = int(input("Enter the quantity purchased: "))

# Prompt for the correct inventory table based on your database schema
print("\nAvailable inventory tables: dairy_products, groceries, household_products")
table_name = input("Enter the table name where this product is located: ").strip().lower()

payment_type = input("Enter type of payment (paid/pending): ").strip()
amount = float(input("Enter the amount of payment: "))
payment_method = input("Enter the method of payment: ").strip()
description = input("Enter the description of the payment: ").strip()

cur = None

try:
    # 2. Insert Payment into Database
    insert_query = """INSERT INTO payments(
        PERSON_NAME,
        PRODUCT_NAME,
        PRODUCT_BRAND,
        PAYMENT_TYPE,
        AMOUNT,
        PAYMENT_METHOD,
        DESCRIPTION
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    insert_values = (
        person_name,
        product_name,
        product_brand,
        payment_type,
        amount,
        payment_method,
        description
    )

    establish_conn()
    target_payment_id = end_connection(insert_query, insert_values)
    print(f"\n[1/4] Payment successfully inserted! Payment ID: {target_payment_id}")

    # 3. Deduct Product Quantity from the Selected Inventory Table (using 'product_quantity')
    update_query = f"""UPDATE {table_name} 
                      SET product_quantity = product_quantity - %s 
                      WHERE product_name = %s AND product_brand = %s"""
    update_values = (quantity_bought, product_name, product_brand)

    establish_conn()
    end_connection(update_query, update_values)
    print(f"[2/4] Stock quantity updated successfully in '{table_name}'.")

    # 4. Fetch the Inserted Record for Invoice Generation
    establish_conn()
    cur = conn.cursor(dictionary=True)
    
    fetch_query = "SELECT * FROM payments WHERE PAYMENT_ID = %s"
    cur.execute(fetch_query, (target_payment_id,))
    record = cur.fetchone()
    
    if not record:
        print(f"\nError: Could not retrieve payment record with ID: {target_payment_id}")
        sys.exit(1)
        
    output_folder = "invoices"
    os.makedirs(output_folder, exist_ok=True)
    filename = os.path.join(output_folder, f"Invoice_{record['PAYMENT_ID']}.pdf")
    
    # 5. Setup PDF Layout & Build Document
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
    
    title_style = ParagraphStyle(
        'InvoiceTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#1E293B'),
        alignment=1,
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
        alignment=2
    )

    story.append(Paragraph("OFFICIAL INVOICE / RECEIPT", title_style))
    story.append(Spacer(1, 10))
    
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
    
    footer_style = ParagraphStyle(
        'InvoiceFooter',
        parent=body_style,
        alignment=1,
        textColor=colors.HexColor('#64748B'),
        fontSize=10
    )
    story.append(Paragraph("Thank you for your business!", footer_style))
    
    doc.build(story)
    print(f"[3/4] PDF Invoice successfully generated and saved as: {filename}")

    # 6. Prompt for printing choice
    print_choice = input("Do you want to print this invoice now? (y/n): ").strip().lower()
    if print_choice in ['y', 'yes']:
        print("[4/4] Sending invoice to printer...")
        print_invoice(filename)
    else:
        print("[4/4] Printing skipped. You can find your PDF anytime in the 'invoices' folder.")

except mysql.connector.Error as err:
    print(f"Database Error: {err}")
    
finally:
    if cur is not None:
        cur.close()
    if conn is not None and conn.is_connected():
        conn.close()