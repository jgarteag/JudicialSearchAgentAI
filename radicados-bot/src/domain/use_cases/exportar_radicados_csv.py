"""Caso de uso: Exportar radicados a CSV"""
import csv
from io import StringIO
from typing import List
from ..ports import JuzgadoRepository


class ExportarRadicadosCSV:
    
    def __init__(self, juzgado_repository: JuzgadoRepository):
        self._juzgado_repo = juzgado_repository
    
    def ejecutar(self) -> str:
        """
        Exporta todos los radicados de todas las colecciones a CSV
        
        Returns:
            String con el contenido del CSV
        """
        output = StringIO()
        writer = csv.writer(output)
        
        # Escribir encabezados
        writer.writerow(['Juzgado', 'Radicado', 'Número', 'Relación', 'Año', 'Tipo'])
        
        # Obtener todos los juzgados
        juzgados_nombres = self._juzgado_repo.listar_juzgados()
        
        # Iterar por cada juzgado y sus radicados
        for nombre_juzgado in juzgados_nombres:
            juzgado = self._juzgado_repo.obtener_juzgado(nombre_juzgado)
            
            if juzgado and juzgado.radicados:
                for radicado in juzgado.radicados:
                    writer.writerow([
                        nombre_juzgado,
                        radicado.radicado,
                        radicado.numero,
                        radicado.relacion,
                        radicado.ano_estado,
                        radicado.tipo
                    ])
        
        return output.getvalue()
