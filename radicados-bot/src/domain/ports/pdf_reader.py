"""Port para lector de PDFs"""
from abc import ABC, abstractmethod


class PDFReader(ABC):
    """Interface para extraer texto de PDFs"""
    
    @abstractmethod
    def extraer_texto(self, pdf_path: str) -> str:
        """Extrae texto de un archivo PDF"""
        pass
