"""
Invoice Generation Service
Handles PDF invoice generation for payments
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
import os
from typing import Dict


class InvoiceService:
    """Service class for generating PDF invoices"""
    
    def __init__(self):
        """Initialize invoice service"""
        self.invoice_dir = "invoices"
        # Create invoices directory if it doesn't exist
        if not os.path.exists(self.invoice_dir):
            os.makedirs(self.invoice_dir)
    
    def generate_invoice(self, payment_data: Dict, user_data: Dict, 
                        subscription_data: Dict) -> Dict:
        """
        Generate a PDF invoice for a payment
        
        Args:
            payment_data: Dictionary containing payment details
            user_data: Dictionary containing user details
            subscription_data: Dictionary containing subscription details
            
        Returns:
            Dictionary with invoice file path and status
        """
        try:
            # Generate unique invoice filename
            invoice_number = f"INV-{payment_data['payment_id']}-{datetime.now().strftime('%Y%m%d')}"
            filename = f"{invoice_number}.pdf"
            filepath = os.path.join(self.invoice_dir, filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1a73e8'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#333333'),
                spaceAfter=12
            )
            
            # Company Header
            elements.append(Paragraph("Exam Preparation Platform", title_style))
            elements.append(Paragraph("INVOICE", styles['Heading2']))
            elements.append(Spacer(1, 0.3*inch))
            
            # Invoice Details
            invoice_info = [
                ["Invoice Number:", invoice_number],
                ["Invoice Date:", datetime.now().strftime("%B %d, %Y")],
                ["Payment ID:", payment_data.get('transaction_id', 'N/A')]
            ]
            
            invoice_table = Table(invoice_info, colWidths=[2*inch, 3*inch])
            invoice_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            elements.append(invoice_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Bill To Section
            elements.append(Paragraph("Bill To:", heading_style))
            bill_to_info = [
                [user_data.get('full_name', 'N/A')],
                [user_data.get('email', 'N/A')],
                [user_data.get('phone_number', 'N/A') if user_data.get('phone_number') else '']
            ]
            
            bill_to_table = Table(bill_to_info, colWidths=[5*inch])
            bill_to_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#666666')),
            ]))
            elements.append(bill_to_table)
            elements.append(Spacer(1, 0.4*inch))
            
            # Subscription Details
            elements.append(Paragraph("Subscription Details:", heading_style))
            
            plan_name = subscription_data.get('plan_type', 'N/A').title() + " Plan"
            
            subscription_details = [
                ['Description', 'Duration', 'Amount'],
                [
                    plan_name,
                    subscription_data.get('duration', 'N/A'),
                    f"₹{payment_data.get('amount', 0):.2f}"
                ]
            ]
            
            subscription_table = Table(subscription_details, colWidths=[3*inch, 1.5*inch, 1.5*inch])
            subscription_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ]))
            elements.append(subscription_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Payment Summary
            discount = subscription_data.get('discount_applied', 0)
            original_amount = subscription_data.get('original_amount', payment_data.get('amount', 0))
            final_amount = payment_data.get('amount', 0)
            
            summary_data = []
            if discount > 0:
                summary_data.append(['Subtotal:', f"₹{original_amount:.2f}"])
                summary_data.append([f'Discount ({discount}%):', f"-₹{(original_amount - final_amount):.2f}"])
            
            summary_data.append(['Total Amount:', f"₹{final_amount:.2f}"])
            summary_data.append(['Payment Status:', payment_data.get('status', 'N/A').upper()])
            
            summary_table = Table(summary_data, colWidths=[4*inch, 2*inch])
            summary_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (0, -2), 'Helvetica'),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('TEXTCOLOR', (0, 0), (-1, -2), colors.HexColor('#333333')),
                ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#1a73e8')),
                ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#1a73e8')),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(summary_table)
            elements.append(Spacer(1, 0.5*inch))
            
            # Footer
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#666666'),
                alignment=TA_CENTER
            )
            
            elements.append(Spacer(1, 0.5*inch))
            elements.append(Paragraph("Thank you for your subscription!", footer_style))
            elements.append(Paragraph("For support, contact: support@examplatform.com", footer_style))
            
            # Build PDF
            doc.build(elements)
            
            return {
                "success": True,
                "invoice_path": filepath,
                "invoice_number": invoice_number,
                "filename": filename
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_invoice_path(self, payment_id: int) -> str:
        """
        Get the file path for an invoice
        
        Args:
            payment_id: Payment ID
            
        Returns:
            File path to the invoice
        """
        # Search for invoice file matching payment_id
        for filename in os.listdir(self.invoice_dir):
            if f"-{payment_id}-" in filename:
                return os.path.join(self.invoice_dir, filename)
        return None


# Create singleton instance
invoice_service = InvoiceService()
