import markdown
from fpdf import FPDF
from io import BytesIO


FONT_REGULAR = "/app/bot/services/font/SF-Compact-Text-Regular.otf"  
FONT_BOLD = "/app/bot/services/font/SF-Compact-Text-Bold.otf"       
FONT_ITALIC = "/app/bot/services/font/SF-Compact-Text-RegularItalic.otf"    
FONT_BOLD_ITALIC = "/app/bot/services/font/SF-Compact-Text-BoldItalic.otf"  

class PDF:
    def make_pdf(self, markdown_text: str):
        html_text = markdown.markdown(markdown_text)
        
        pdf = FPDF()

        pdf.add_font("CustomFont", "", FONT_REGULAR, uni=True)
        pdf.add_font("CustomFont", "B", FONT_BOLD, uni=True)
        pdf.add_font("CustomFont", "I", FONT_ITALIC, uni=True)
        pdf.add_font("CustomFont", "BI", FONT_BOLD_ITALIC, uni=True)
        
        
        pdf.set_font("CustomFont", "", 12)

        pdf.add_page()

        
        output_buffer = BytesIO()
        pdf.write_html(html_text)
        pdf.output(output_buffer)
        output_buffer.seek(0)
        return output_buffer.getvalue()


pdf_service = PDF()
