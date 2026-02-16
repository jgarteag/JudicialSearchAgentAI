"""Caso de uso: Buscar radicados en PDF"""
from typing import List
from dataclasses import dataclass
from ..entities import Radicado
from ..ports import JuzgadoRepository, PDFReader


@dataclass
class RadicadoEncontrado:
    radicado: Radicado
    contexto: str


class BuscarRadicadosEnPDF:
    
    def __init__(
        self,
        juzgado_repository: JuzgadoRepository,
        pdf_reader: PDFReader
    ):
        self._juzgado_repo = juzgado_repository
        self._pdf_reader = pdf_reader
    
    def ejecutar(self, nombre_juzgado: str, pdf_path: str) -> List[RadicadoEncontrado]:
        juzgado = self._juzgado_repo.obtener_juzgado(nombre_juzgado)
        if not juzgado:
            raise ValueError(f"Juzgado {nombre_juzgado} no encontrado")
        
        texto_pdf = self._pdf_reader.extraer_texto(pdf_path)
        
        encontrados = []
        for radicado in juzgado.radicados:
            if radicado.numero in texto_pdf:
                idx = texto_pdf.find(radicado.numero)
                inicio = max(0, idx - 50)
                fin = min(len(texto_pdf), idx + len(radicado.numero) + 50)
                contexto = texto_pdf[inicio:fin]
                
                encontrados.append(
                    RadicadoEncontrado(radicado=radicado, contexto=contexto)
                )
        
        return encontrados
