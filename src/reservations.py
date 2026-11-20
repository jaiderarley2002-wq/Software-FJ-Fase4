"""Manejo de reservas y control de los estados permitidos para cada operación."""

from enum import Enum
from math import isfinite
from numbers import Real

from .entities import Entidad, Cliente
from .services import Servicio
from .exceptions import ReservationError, ValidationError
from .logger_config import registrar_evento


class EstadoReserva(Enum):
    """Valores posibles de una reserva durante su proceso."""
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    PROCESADA = "Procesada"


class Reserva(Entidad):
    """Une un cliente con un servicio y controla su duración y estado."""

    # Crea la relación entre cliente y servicio, valida la duración e inicia la reserva en estado pendiente.
    def __init__(self, identificador: str, cliente: Cliente, servicio: Servicio, duracion: float):
        super().__init__(identificador)

        # Se comprueba que los objetos recibidos sean de las clases esperadas.
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ValidationError("La reserva requiere un cliente y un servicio válidos.")

        # bool también se considera un número en Python; por eso se excluye expresamente.
        # isfinite evita aceptar valores como infinito o NaN en la duración.
        if (isinstance(duracion, bool) or not isinstance(duracion, Real)
                or not isfinite(float(duracion)) or duracion <= 0):
            raise ValidationError("La duración de la reserva debe ser positiva y finita.")

        # La reserva conserva las referencias a los objetos, no copias de sus datos.
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = float(duracion)
        # Toda reserva comienza pendiente y debe confirmarse antes de procesarse.
        # La reserva inicia pendiente y solo cambia de estado mediante sus métodos.
        self.estado = EstadoReserva.PENDIENTE
        registrar_evento(f"Reserva creada: {self.identificador}")

    # Realiza el cambio de pendiente a confirmada después de revisar la disponibilidad del servicio.
    def confirmar(self) -> None:
        # Solo una reserva pendiente puede pasar a confirmada.
        if self.estado != EstadoReserva.PENDIENTE:
            raise ReservationError("Solo se pueden confirmar reservas pendientes.")

        # Antes de confirmar también se revisa que el servicio siga disponible.
        # La comprobación se hace justo antes de confirmar para evitar aceptar un servicio fuera de uso.
        self.servicio.validar_disponibilidad()
        # El estado se modifica después de superar la validación de disponibilidad.
        self.estado = EstadoReserva.CONFIRMADA
        registrar_evento(f"Reserva {self.identificador} confirmada")

    # Cambia el estado a cancelado solamente cuando la operación todavía lo permite.
    def cancelar(self) -> None:
        # Una reserva cancelada o ya procesada no se puede cancelar otra vez.
        if self.estado == EstadoReserva.CANCELADA:
            raise ReservationError("La reserva ya está cancelada.")
        if self.estado == EstadoReserva.PROCESADA:
            raise ReservationError("No se puede cancelar una reserva que ya fue procesada.")

        # El cambio queda registrado para que después no pueda repetirse la cancelación.
        self.estado = EstadoReserva.CANCELADA
        registrar_evento(f"Reserva {self.identificador} cancelada")

    # Calcula el costo de una reserva confirmada y luego la marca como procesada.
    def procesar(self, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        # Se exige la confirmación para evitar cobrar una reserva que no fue aprobada.
        if self.estado != EstadoReserva.CONFIRMADA:
            raise ReservationError("La reserva debe estar confirmada antes de procesarse.")

        # El cálculo se delega al servicio; cada servicio comparte la misma operación base.
        # El servicio aplica su tarifa y las reglas generales de cálculo al tiempo reservado.
        total = self.servicio.calcular_costo(
            self.duracion, impuesto=impuesto, descuento=descuento
        )
        # Solo se marca como procesada después de obtener un cálculo válido.
        self.estado = EstadoReserva.PROCESADA
        registrar_evento(f"Reserva {self.identificador} procesada. Total: {total}")
        return total

    # Devuelve un resumen de la reserva con el cliente, el servicio, la duración y su estado actual.
    def describir(self) -> str:
        # Se muestra la información relacionada sin exponer los atributos internos.
        return (f"Reserva {self.identificador} | {self.cliente.nombre} | "
                f"{self.servicio.nombre} | {self.duracion} horas | {self.estado.value}")
