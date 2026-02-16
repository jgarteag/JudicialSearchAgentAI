"""Entry point - Dependency Injection"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))

from domain.use_cases import BuscarRadicadosEnPDF
from infrastructure.mongodb_juzgado_repository import MongoDBJuzgadoRepository
from infrastructure.pypdf_reader import PyPDFReader
from infrastructure.telegram_bot import TelegramBot
from application.bot_service import BotService


def main():
    load_dotenv()
    
    mongo_uri = os.getenv("MONGODB_URI")
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not mongo_uri or not telegram_token:
        raise ValueError("Faltan variables de entorno. Revisa tu archivo .env")
    
    juzgado_repo = MongoDBJuzgadoRepository(mongo_uri)
    pdf_reader = PyPDFReader()
    
    buscar_radicados_use_case = BuscarRadicadosEnPDF(
        juzgado_repository=juzgado_repo,
        pdf_reader=pdf_reader
    )
    
    bot_service = BotService(
        buscar_radicados_use_case=buscar_radicados_use_case,
        juzgado_repository=juzgado_repo
    )
    
    telegram_bot = TelegramBot(telegram_token)
    
    telegram_bot.registrar_comando_start(bot_service.handle_start)
    telegram_bot.registrar_comando_juzgados(bot_service.handle_juzgados)
    telegram_bot.registrar_comando_buscar(bot_service.handle_comando_buscar)
    telegram_bot.registrar_handler_documento(bot_service.handle_documento)
    telegram_bot.registrar_handler_texto(bot_service.handle_texto)
    
    print("🤖 Bot de radicados iniciado...")
    telegram_bot.iniciar()


if __name__ == "__main__":
    main()
