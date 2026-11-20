"""Configuración del registro de eventos y errores en un archivo de texto."""

import logging
from pathlib import Path

# La ruta se calcula a partir de la ubicación de este archivo, no de la terminal.
# Así el programa puede ejecutarse desde la carpeta raíz sin perder el archivo de log.
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
# Se crea la carpeta si todavía no existe; exist_ok evita un error si ya estaba creada.
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "software_fj.log"

# Se utiliza un logger con nombre propio para distinguir los mensajes de esta aplicación.
logger = logging.getLogger("SoftwareFJ")
# INFO permite guardar tanto operaciones normales como advertencias y errores.
logger.setLevel(logging.INFO)
logger.propagate = False

# Se agrega el manejador una sola vez para evitar que los mensajes salgan duplicados.
if not logger.handlers:
    # FileHandler envía los registros al archivo y UTF-8 permite conservar tildes.
    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    # El formato incluye fecha, nivel del mensaje y descripción del evento.
    handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    ))
    logger.addHandler(handler)


# Guarda acciones normales del programa para dejar constancia de lo que sí se ejecutó.
def registrar_evento(mensaje: str) -> None:
    """Guarda una operación normal con el nivel INFO."""
    # Estos mensajes sirven para revisar qué operaciones sí se completaron.
    logger.info(mensaje)


# Registra el error y su información técnica para facilitar la revisión de una falla.
def registrar_error(mensaje: str) -> None:
    """Guarda el error junto con su traza cuando se llama desde un bloque except."""
    # logger.exception conserva el detalle técnico que ayuda a localizar el problema.
    logger.exception(mensaje)
