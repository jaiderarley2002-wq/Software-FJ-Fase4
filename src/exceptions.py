"""Excepciones propias para identificar los errores del sistema Software FJ."""


# Todas las excepciones propias parten de esta clase para poder capturarlas juntas en main.py.
class SoftwareFJError(Exception):
    """Clase padre de los errores que la aplicación sabe controlar."""


# Separar los errores por tipo permite mostrar mensajes más claros y manejarlos
# de forma distinta sin depender solamente de excepciones generales de Python.
# Se utiliza cuando un dato no cumple las condiciones exigidas por el sistema.
class ValidationError(SoftwareFJError):
    """Se usa cuando un dato recibido no cumple las reglas de validación."""


# Permite diferenciar un servicio fuera de disponibilidad de un dato mal escrito.
class ServiceUnavailableError(SoftwareFJError):
    """Se genera cuando se intenta confirmar una reserva de un servicio no disponible."""


# Identifica acciones que no se pueden realizar por el estado actual de la reserva.
class ReservationError(SoftwareFJError):
    """Representa una acción que no corresponde al estado actual de una reserva."""


# Evita registrar dos clientes diferentes con el mismo identificador.
class DuplicateClientError(SoftwareFJError):
    """Se genera cuando se intenta registrar dos veces el mismo identificador de cliente."""
