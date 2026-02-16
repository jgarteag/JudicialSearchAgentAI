"""Adaptador MongoDB para JuzgadoRepository"""
from typing import List, Optional
from pymongo import MongoClient
from pymongo.database import Database

from domain.entities import Juzgado, Radicado
from domain.ports import JuzgadoRepository


class MongoDBJuzgadoRepository(JuzgadoRepository):
    
    def __init__(self, mongo_uri: str, database_name: str = "dbestados"):
        self._client = MongoClient(mongo_uri)
        self._db: Database = self._client[database_name]
    
    def obtener_juzgado(self, nombre: str) -> Optional[Juzgado]:
        if nombre not in self._db.list_collection_names():
            return None
        
        collection = self._db[nombre]
        documentos = list(collection.find())
        
        if not documentos:
            return None
        
        radicados = [
            Radicado(
                numero=doc.get('numero', ''),
                ano_estado=doc.get('ano_estado', 0),
                relacion=doc.get('relacion', ''),
                tipo=doc.get('tipo', ''),
                radicado=doc.get('radicado', '')
            )
            for doc in documentos
        ]
        
        return Juzgado(nombre=nombre, radicados=radicados)
    
    def listar_juzgados(self) -> List[str]:
        return self._db.list_collection_names()
    
    def close(self):
        self._client.close()
