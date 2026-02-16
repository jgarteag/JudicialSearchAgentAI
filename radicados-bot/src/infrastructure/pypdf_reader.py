"""Adaptador PyPDF2 para PDFReader"""
from PyPDF2 import PdfReader
from domain.ports import PDFReader


class PyPDFReader(PDFReader):
    
    def extraer_texto(self, pdf_path: str) -> str:
        try:
            reader = PdfReader(pdf_path)
            texto = ""
            
            for page in reader.pages:
                texto += page.extract_text() + "\n"
            
            return texto
        except Exception as e:
            raise ValueError(f"Error al leer PDF: {str(e)}")
