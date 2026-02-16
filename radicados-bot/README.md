# Bot de Búsqueda de Radicados

Bot de Telegram para buscar radicados judiciales en PDFs usando arquitectura hexagonal.

## Características

- Búsqueda de radicados en múltiples PDFs simultáneamente
- Selección de juzgados por número o nombre
- Arquitectura hexagonal (clean architecture)
- Soporte para PDFs encriptados

## Instalación

```bash
cd radicados-bot
pip install -r requirements.txt
```

## Configuración

Crea un archivo `.env` con:

```
MONGODB_URI=tu_connection_string
TELEGRAM_BOT_TOKEN=tu_token_de_botfather
```

## Uso

```bash
python src/main.py
```

## Comandos del bot

- `/start` - Iniciar el bot
- `/buscar` o `/juzgados` - Ver juzgados disponibles
- Enviar PDFs y escribir número del juzgado para buscar

## Estructura

```
src/
├── domain/          # Lógica de negocio
├── application/     # Servicios de aplicación
├── infrastructure/  # Adaptadores (MongoDB, PDF, Telegram)
└── main.py         # Entry point
```
