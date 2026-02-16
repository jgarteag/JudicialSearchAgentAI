"""Servicio de aplicación para el bot"""
import os
from typing import Dict
from telegram import Update
from telegram.ext import ContextTypes

from domain.use_cases import BuscarRadicadosEnPDF, ExportarRadicadosCSV
from domain.ports import JuzgadoRepository


class BotService:
    """Servicio que coordina la lógica del bot"""
    
    def __init__(
        self,
        buscar_radicados_use_case: BuscarRadicadosEnPDF,
        exportar_csv_use_case: ExportarRadicadosCSV,
        juzgado_repository: JuzgadoRepository
    ):
        self._buscar_radicados = buscar_radicados_use_case
        self._exportar_csv = exportar_csv_use_case
        self._juzgado_repo = juzgado_repository
        self._user_states: Dict[int, dict] = {}
    
    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "¡Hola! 👋 Soy tu asistente para buscar radicados.\n\n"
            "📋 Comandos disponibles:\n"
            "• Envía PDFs para buscar radicados\n"
            "• /buscar - Ver juzgados y buscar\n"
            "• /consulta - Descargar CSV con todos los radicados\n\n"
            "💡 Tip: Puedes enviar varios PDFs antes de buscar"
        )
    
    async def handle_juzgados(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.handle_comando_buscar(update, context)
    
    async def handle_documento(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        temp_dir: str
    ):
        user_id = update.effective_user.id
        
        file = await update.message.document.get_file()
        pdf_filename = update.message.document.file_name
        pdf_path = os.path.join(temp_dir, f"{user_id}_{file.file_id}.pdf")
        await file.download_to_drive(pdf_path)
        
        if user_id not in self._user_states:
            self._user_states[user_id] = {"pdfs": []}
        
        self._user_states[user_id]["pdfs"].append({
            "path": pdf_path,
            "filename": pdf_filename
        })
        
        num_pdfs = len(self._user_states[user_id]["pdfs"])
        await update.message.reply_text(f"✅ PDF recibido ({num_pdfs} total)")
    
    async def handle_comando_buscar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in self._user_states or not self._user_states[user_id].get("pdfs"):
            await update.message.reply_text(
                "⚠️ Primero envíame uno o más PDFs para buscar."
            )
            return
        
        juzgados = self._juzgado_repo.listar_juzgados()
        num_pdfs = len(self._user_states[user_id]["pdfs"])
        
        mensaje = f"📁 Tienes {num_pdfs} PDF(s) listos.\n\n"
        mensaje += "Selecciona un juzgado a buscar (escribe el número):\n\n"
        for idx, juzgado in enumerate(juzgados, 1):
            mensaje += f"{idx}. {juzgado}\n"
        
        await update.message.reply_text(mensaje)
    
    async def handle_texto(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        texto = update.message.text.strip()
        
        if user_id not in self._user_states:
            await update.message.reply_text(
                "Primero envíame uno o más PDFs.\n"
                "Luego usa /buscar para buscar."
            )
            return
        
        pdfs = self._user_states[user_id].get("pdfs", [])
        
        if not pdfs:
            await update.message.reply_text("No encontré tus PDFs. Envíalos de nuevo.")
            return
        
        juzgados = self._juzgado_repo.listar_juzgados()
        juzgado_nombre = None
        
        if texto.isdigit():
            idx = int(texto) - 1
            if 0 <= idx < len(juzgados):
                juzgado_nombre = juzgados[idx]
            else:
                await update.message.reply_text(
                    "Número inválido. Usa /buscar para ver las opciones."
                )
                return
        else:
            if texto in juzgados:
                juzgado_nombre = texto
            else:
                await update.message.reply_text(
                    "Juzgado no encontrado. Usa /buscar para ver las opciones."
                )
                return
        
        await update.message.reply_text(
            f"🔍 Buscando en {len(pdfs)} PDF(s) del juzgado {juzgado_nombre}..."
        )
        
        try:
            todos_encontrados = []
            
            for pdf_info in pdfs:
                pdf_path = pdf_info["path"]
                pdf_filename = pdf_info["filename"]
                
                if not os.path.exists(pdf_path):
                    continue
                    
                encontrados = self._buscar_radicados.ejecutar(juzgado_nombre, pdf_path)
                
                if encontrados:
                    todos_encontrados.extend([
                        (pdf_filename, item) for item in encontrados
                    ])
            
            if not todos_encontrados:
                await update.message.reply_text(
                    f"❌ No encontré radicados de {juzgado_nombre} en ningún PDF."
                )
            else:
                if len(todos_encontrados) == 1:
                    encabezado = "🎉 ¡Encontré 1 radicado!\n\n"
                else:
                    encabezado = f"🎉 ¡Encontré {len(todos_encontrados)} radicados!\n\n"
                
                mensaje = encabezado
                for idx, (pdf_name, item) in enumerate(todos_encontrados, 1):
                    mensaje += (
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"📌 Radicado #{idx}\n"
                        f"🔢 {item.radicado.radicado}\n"
                        f"📄 Archivo: {pdf_name}\n"
                        f"👤 De: {item.radicado.relacion}\n"
                        f"📅 Año: {item.radicado.ano_estado}\n\n"
                    )
                
                mensaje += "━━━━━━━━━━━━━━━━━━━━\n"
                mensaje += "✅ Búsqueda completada"
                
                await update.message.reply_text(mensaje)
            
            for pdf_info in pdfs:
                if os.path.exists(pdf_info["path"]):
                    os.remove(pdf_info["path"])
            del self._user_states[user_id]
            
        except ValueError as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
        except Exception as e:
            await update.message.reply_text(f"❌ Error al procesar los PDFs: {str(e)}")


    async def handle_consulta(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para comando /consulta - exporta todos los radicados a CSV"""
        await update.message.reply_text("📊 Generando reporte CSV de todos los radicados...")
        
        try:
            csv_content = self._exportar_csv.ejecutar()
            
            # Crear archivo temporal
            temp_file = f"temp_radicados_{update.effective_user.id}.csv"
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(csv_content)
            
            # Enviar archivo
            with open(temp_file, 'rb') as f:
                await update.message.reply_document(
                    document=f,
                    filename="radicados_consolidado.csv",
                    caption="✅ Reporte consolidado de todos los radicados"
                )
            
            # Eliminar archivo temporal
            os.remove(temp_file)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error al generar el reporte: {str(e)}")
