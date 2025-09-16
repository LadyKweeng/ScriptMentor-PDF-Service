import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import tempfile
import os
import logging

logger = logging.getLogger(__name__)

class FDXToPDFConverter:
    """Convert FDX files to PDF for hybrid processing"""
    
    def __init__(self):
        # Set up PDF styles that mimic screenplay formatting
        self.styles = getSampleStyleSheet()
        
        # Scene heading style
        self.scene_style = ParagraphStyle(
            'SceneHeading',
            parent=self.styles['Normal'],
            fontName='Courier-Bold',
            fontSize=12,
            spaceAfter=12,
            leftIndent=0
        )
        
        # Character name style
        self.character_style = ParagraphStyle(
            'Character',
            parent=self.styles['Normal'],
            fontName='Courier-Bold',
            fontSize=12,
            leftIndent=2.5*inch,
            spaceAfter=0
        )
        
        # Dialogue style
        self.dialogue_style = ParagraphStyle(
            'Dialogue',
            parent=self.styles['Normal'],
            fontName='Courier',
            fontSize=12,
            leftIndent=1.5*inch,
            rightIndent=1*inch,
            spaceAfter=12
        )
        
        # Action style
        self.action_style = ParagraphStyle(
            'Action',
            parent=self.styles['Normal'],
            fontName='Courier',
            fontSize=12,
            leftIndent=0,
            spaceAfter=12
        )
    
    def convert_to_pdf(self, fdx_path: str) -> str:
        """
        Convert FDX file to PDF
        Returns path to generated PDF file
        """
        logger.info(f"Converting FDX to PDF: {fdx_path}")
        
        # Parse FDX XML
        tree = ET.parse(fdx_path)
        root = tree.getroot()
        
        # Create temporary PDF file
        pdf_fd, pdf_path = tempfile.mkstemp(suffix='.pdf')
        os.close(pdf_fd)
        
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                pdf_path,
                pagesize=letter,
                topMargin=1*inch,
                bottomMargin=1*inch,
                leftMargin=1.5*inch,
                rightMargin=1*inch
            )
            
            story = []
            
            # Extract title page info
            title_page = root.find('.//TitlePage')
            if title_page is not None:
                content_elements = title_page.findall('.//Content')
                for content in content_elements:
                    content_type = content.get('Type')
                    text = content.text or ''
                    
                    if content_type == 'Title' and text:
                        story.append(Paragraph(text, self.styles['Title']))
                        story.append(Spacer(1, 0.5*inch))
                    elif content_type == 'Author' and text:
                        story.append(Paragraph(f"Written by {text}", self.styles['Normal']))
                        story.append(Spacer(1, 1*inch))
            
            # Process screenplay content
            content = root.find('.//Content')
            if content is not None:
                paragraphs = content.findall('.//Paragraph')
                
                for para in paragraphs:
                    para_type = para.get('Type')
                    text_elements = para.findall('.//Text')
                    
                    # Combine text from all Text elements
                    full_text = ' '.join(elem.text or '' for elem in text_elements).strip()
                    
                    if not full_text:
                        continue
                    
                    # Apply appropriate style based on paragraph type
                    if para_type == 'Scene Heading':
                        story.append(Paragraph(full_text.upper(), self.scene_style))
                    elif para_type == 'Character':
                        story.append(Paragraph(full_text.upper(), self.character_style))
                    elif para_type == 'Dialogue':
                        story.append(Paragraph(full_text, self.dialogue_style))
                    elif para_type == 'Action':
                        story.append(Paragraph(full_text, self.action_style))
                    elif para_type == 'Parenthetical':
                        story.append(Paragraph(f"({full_text})", self.dialogue_style))
                    else:
                        # Default to action style for unknown types
                        story.append(Paragraph(full_text, self.action_style))
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"Successfully converted FDX to PDF: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(pdf_path):
                os.unlink(pdf_path)
            logger.error(f"Error converting FDX to PDF: {str(e)}")
            raise