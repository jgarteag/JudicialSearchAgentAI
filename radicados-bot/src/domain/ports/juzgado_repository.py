"""Port para repositorio de juzgados"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities import Juzgado


class JuzgadoRepository(ABC):
    """Interface para acceder a datos de juzgados"""
    
    @abstractmethod
    def obtener_juzgado(self, nombre: str) -> Optional[Juzgado]:
        """Obtiene un juzgado por nombre"""
        pass
    
    @abstractmethod
    def listar_juzgados(self) -> List[str]:
        """Lista todos los nombres de juzgados disponibles"""
        pass
