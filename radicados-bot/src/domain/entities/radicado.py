"""Entidad Radicado - Core del dominio"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Radicado:
    """Representa un radicado judicial"""
    numero: str
    ano_estado: int
    relacion: str
    tipo: str
    radicado: str
    
    def __str__(self) -> str:
        return f"Radicado {self.radicado} de {self.relacion}"
