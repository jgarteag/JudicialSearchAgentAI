"""Adaptador Telegram Bot"""
import os
import logging
from typing import Callable
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class TelegramBot:
    
    def __init__(self, token: str):
        self._token = token
        self._app = Application.builder().token(token).build()
        self._temp_dir = "temp_pdfs"
        os.makedirs(self._temp_dir, exist_ok=True)
    
    def registrar_comando_start(self, handler: Callable):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await handler(update, context)
        self._app.add_handler(CommandHandler("start", wrapper))
    
    def registrar_comando_juzgados(self, handler: Callable):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await handler(update, context)
        self._app.add_handler(CommandHandler("juzgados", wrapper))
    
    def registrar_comando_buscar(self, handler: Callable):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await handler(update, context)
        self._app.add_handler(CommandHandler("buscar", wrapper))
    
    def registrar_handler_texto(self, handler: Callable):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await handler(update, context)
        self._app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, wrapper)
        )
    
    def registrar_handler_documento(self, handler: Callable):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await handler(update, context, self._temp_dir)
        self._app.add_handler(MessageHandler(filters.Document.PDF, wrapper))
    
    def iniciar(self):
        print("Bot iniciado...")
        self._app.run_polling()
