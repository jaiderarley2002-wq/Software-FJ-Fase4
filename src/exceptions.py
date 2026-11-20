"""Excepciones personalizadas que se utilizan en el sistema Software FJ."""


# Creamos una excepción general para agrupar los errores propios del proyecto.
class SoftwareFJError(Exception):
    """Excepción base para los errores controlados de la aplicación."""


# Esta excepción se utiliza cuando los datos ingresados no cumplen las reglas.
class ValidationError(SoftwareFJError):
    """Se produce cuando un dato no cumple las reglas de validación."""


# Se utiliza cuando se intenta trabajar con un servicio que no está disponible.
class ServiceUnavailableError(SoftwareFJError):
    """Se produce cuando un servicio no está disponible."""


# Esta excepción controla acciones que no se pueden realizar sobre una reserva.
class ReservationError(SoftwareFJError):
    """Se produce cuando una operación de reserva no está permitida."""


# La dejamos preparada para controlar registros repetidos de clientes.
class DuplicateClientError(SoftwareFJError):
    """Se produce cuando se intenta registrar un cliente duplicado."""
