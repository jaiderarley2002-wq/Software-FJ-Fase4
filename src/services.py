"""Servicios especializados que aplican herencia y polimorfismo."""

# Utilizamos ABC y abstractmethod para definir una clase base que no se instancia directamente.
from abc import ABC, abstractmethod

# Estos errores permiten informar validaciones incorrectas y servicios no disponibles.
from .exceptions import ValidationError, ServiceUnavailableError


# La clase Servicio contiene los datos y comportamientos que comparten los servicios.
class Servicio(ABC):
    """Clase abstracta que define el comportamiento común de un servicio."""

    def __init__(self, codigo: str, nombre: str, tarifa_hora: float, disponible: bool = True):
        # Comprobamos que el servicio tenga código y nombre.
        if not codigo or not nombre.strip():
            raise ValidationError("El código y el nombre del servicio son obligatorios.")

        # La tarifa debe ser un número positivo para poder calcular los costos.
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ValidationError("La tarifa por hora debe ser un número positivo.")

        # Guardamos los datos básicos del servicio.
        self.codigo = codigo
        self.nombre = nombre.strip()
        self.tarifa_hora = float(tarifa_hora)
        self.disponible = bool(disponible)

    def validar_disponibilidad(self) -> None:
        # Si el servicio está deshabilitado, no dejamos continuar la operación.
        if not self.disponible:
            raise ServiceUnavailableError(f"El servicio '{self.nombre}' no está disponible.")

    @abstractmethod
    def describir(self) -> str:
        # Cada servicio especializado presenta su propia descripción.
        raise NotImplementedError

    @abstractmethod
    def validar_parametros(self, **kwargs) -> None:
        # Cada tipo de servicio revisa los parámetros que necesita.
        raise NotImplementedError

    def calcular_costo(self, *args, **kwargs) -> float:
        """Calcula el costo aceptando distintas combinaciones de argumentos."""
        # Con *args y **kwargs simulamos variantes de cálculo en Python.
        # La primera posición corresponde siempre a la cantidad de horas.
        if not args:
            raise ValidationError("Debe indicar la duración en horas.")

        horas = args[0]

        # El impuesto y el descuento se pueden recibir por posición o por nombre.
        impuesto = kwargs.get("impuesto", args[1] if len(args) > 1 else 0.0)
        descuento = kwargs.get("descuento", args[2] if len(args) > 2 else 0.0)

        # Revisamos que la duración sea un número positivo.
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ValidationError("La duración debe ser mayor que cero.")

        # Validamos que el impuesto y el descuento estén entre 0 y 1.
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise ValidationError("Impuesto y descuento deben estar entre 0 y 1.")

        # Primero calculamos el subtotal y luego aplicamos descuento e impuesto.
        subtotal = self.tarifa_hora * horas
        return round(subtotal * (1 - descuento) * (1 + impuesto), 2)


# Este servicio representa el alquiler de una sala y hereda de Servicio.
class ReservaSala(Servicio):
    def describir(self) -> str:
        # Mostramos el nombre de la sala y su tarifa por hora.
        return f"Reserva de sala: {self.nombre} (${self.tarifa_hora:.2f}/hora)"

    def validar_parametros(self, **kwargs) -> None:
        # Para una sala necesitamos que la capacidad sea un entero positivo.
        capacidad = kwargs.get("capacidad")
        if not isinstance(capacidad, int) or capacidad < 1:
            raise ValidationError("La capacidad de la sala debe ser un entero positivo.")


# Este servicio maneja el alquiler de equipos, por ejemplo un proyector.
class AlquilerEquipo(Servicio):
    def describir(self) -> str:
        # La descripción cambia para identificar que se trata de un equipo.
        return f"Alquiler de equipo: {self.nombre} (${self.tarifa_hora:.2f}/hora)"

    def validar_parametros(self, **kwargs) -> None:
        # La cantidad de equipos debe ser como mínimo uno.
        cantidad = kwargs.get("cantidad", 1)
        if not isinstance(cantidad, int) or cantidad < 1:
            raise ValidationError("La cantidad de equipos debe ser un entero positivo.")


# Este servicio representa las asesorías que ofrece la empresa.
class Asesoria(Servicio):
    def describir(self) -> str:
        # Indicamos que el servicio corresponde a una asesoría especializada.
        return f"Asesoría especializada: {self.nombre} (${self.tarifa_hora:.2f}/hora)"

    def validar_parametros(self, **kwargs) -> None:
        # Para crear una asesoría se debe indicar quién será el especialista.
        especialista = kwargs.get("especialista")
        if not isinstance(especialista, str) or len(especialista.strip()) < 3:
            raise ValidationError("Debe indicar el nombre del especialista.")
