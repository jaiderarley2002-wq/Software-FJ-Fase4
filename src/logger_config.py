"""Configuración centralizada del registro de eventos y errores."""

# logging es el módulo de Python que usamos para guardar eventos y errores.
import logging

# Path facilita crear y manejar las rutas de carpetas y archivos.
from pathlib import Path

# Definimos la carpeta logs tomando como referencia la ubicación de este archivo.
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"

# Si la carpeta no existe, la creamos automáticamente.
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Aquí se guardará el historial de eventos y errores del programa.
LOG_FILE = LOG_DIR / "software_fj.log"

# Creamos un logger con nombre propio para identificar los registros del proyecto.
logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.INFO)

# Evitamos agregar varios manejadores si el módulo se importa más de una vez.
if not logger.handlers:
    # Abrimos el archivo en modo de registro y usamos UTF-8 para los caracteres en español.
    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")

    # Indicamos que cada registro debe mostrar fecha, nivel y mensaje.
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)


def registrar_evento(mensaje: str) -> None:
    """Registra una operación relevante del sistema."""
    # Los eventos normales se guardan con nivel INFO.
    logger.info(mensaje)


def registrar_error(mensaje: str) -> None:
    """Registra un error junto con la información de la excepción activa."""
    # Se llama desde un bloque except para incluir también el detalle del error.
    logger.exception(mensaje)
