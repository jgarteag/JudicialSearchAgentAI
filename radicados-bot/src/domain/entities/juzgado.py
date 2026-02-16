"""Entidad Juzgado - Core del dominio"""
from dataclasses import dataclass
from typing import List
from .radicado import Radicado


@dataclass
class Juzgado:
    """Representa un juzgado con sus radicados"""
    nombre: str
    radicados: List[Radicado]
    
    def obtener_numeros(self) -> List[str]:
        """Retorna lista de números de radicados"""
        return [r.numero for r in self.radicados]
