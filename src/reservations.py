"""Gestión de reservas y validación de sus estados."""

# Enum permite definir los estados posibles para una reserva.
from enum import Enum

# Importamos las clases que se relacionan dentro de una reserva.
from .entities import Entidad, Cliente
from .services import Servicio

# Usamos excepciones propias para controlar datos y operaciones incorrectas.
from .exceptions import ReservationError, ValidationError

# Esta función registra los cambios importantes en el archivo de log.
from .logger_config import registrar_evento


# La reserva puede estar pendiente, confirmada o cancelada.
class EstadoReserva(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"


# Reserva hereda de Entidad y conecta al cliente con el servicio solicitado.
class Reserva(Entidad):
    def __init__(self, identificador: str, cliente: Cliente, servicio: Servicio, duracion: float):
        # Validamos el identificador con el constructor de la clase padre.
        super().__init__(identificador)

        # Comprobamos que se estén pasando objetos de las clases esperadas.
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ValidationError("La reserva requiere un cliente y un servicio válidos.")

        # No permitimos crear una reserva con duración cero o negativa.
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ValidationError("La duración de la reserva debe ser positiva.")

        # Guardamos los objetos relacionados y convertimos la duración a decimal.
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = float(duracion)

        # Toda reserva empieza en estado pendiente.
        self.estado = EstadoReserva.PENDIENTE

    def confirmar(self) -> None:
        # Antes de confirmar revisamos que el servicio esté disponible.
        self.servicio.validar_disponibilidad()

        # Solo una reserva pendiente puede pasar al estado confirmado.
        if self.estado != EstadoReserva.PENDIENTE:
            raise ReservationError("Solo se pueden confirmar reservas pendientes.")

        self.estado = EstadoReserva.CONFIRMADA
        # Registramos el cambio de estado para tener trazabilidad.
        registrar_evento(f"Reserva {self.identificador} confirmada")

    def cancelar(self) -> None:
        # Evitamos cancelar una reserva que ya aparece como cancelada.
        if self.estado == EstadoReserva.CANCELADA:
            raise ReservationError("La reserva ya está cancelada.")

        self.estado = EstadoReserva.CANCELADA
        # Guardamos en el log que se realizó la cancelación.
        registrar_evento(f"Reserva {self.identificador} cancelada")

    def procesar(self, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        # No se puede cobrar una reserva mientras siga pendiente o esté cancelada.
        if self.estado != EstadoReserva.CONFIRMADA:
            raise ReservationError("La reserva debe estar confirmada antes de procesarse.")

        # El servicio calcula el costo según sus tarifas, impuesto y descuento.
        costo = self.servicio.calcular_costo(self.duracion, impuesto=impuesto, descuento=descuento)

        # Registramos el total que se obtuvo al procesar la reserva.
        registrar_evento(f"Reserva {self.identificador} procesada. Total: {costo}")
        return costo

    def describir(self) -> str:
        # Esta información sirve para mostrar un resumen de la reserva.
        return (f"Reserva {self.identificador} | {self.cliente.nombre} | "
                f"{self.servicio.nombre} | {self.duracion} horas | {self.estado.value}")
