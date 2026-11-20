"""Clases de los servicios que ofrece Software FJ."""

from abc import ABC, abstractmethod
from math import isfinite
from numbers import Real

from .exceptions import ValidationError, ServiceUnavailableError


class Servicio(ABC):
    """Clase abstracta con los datos y comportamientos que comparten los servicios."""

    # Valida y guarda los datos que comparten todos los servicios antes de que se use una clase especializada.
    def __init__(self, codigo: str, nombre: str, tarifa_hora: float, disponible: bool = True):
        # Los datos comunes se validan aquí para que las clases hijas no repitan el código.
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValidationError("El código del servicio es obligatorio.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValidationError("El nombre del servicio es obligatorio.")

        # Se aceptan números reales, pero no valores booleanos, infinitos ni negativos.
        if (isinstance(tarifa_hora, bool) or not isinstance(tarifa_hora, Real)
                or not isfinite(float(tarifa_hora)) or tarifa_hora <= 0):
            raise ValidationError("La tarifa por hora debe ser un número positivo y finito.")
        if not isinstance(disponible, bool):
            raise ValidationError("La disponibilidad debe indicarse con True o False.")

        # Se guardan los datos limpios después de validar que no estén vacíos.
        self.codigo = codigo.strip()
        self.nombre = nombre.strip()
        self.tarifa_hora = float(tarifa_hora)
        self.disponible = disponible

    # Detiene la confirmación de una reserva cuando el servicio no se encuentra disponible.
    def validar_disponibilidad(self) -> None:
        # Esta validación se reutiliza cuando se confirma una reserva.
        if not self.disponible:
            raise ServiceUnavailableError(f"El servicio '{self.nombre}' no está disponible.")

    @abstractmethod
    # Obliga a cada tipo de servicio a construir una descripción propia.
    def describir(self) -> str:
        # Cada clase hija devuelve una descripción de acuerdo con su tipo de servicio.
        raise NotImplementedError

    @abstractmethod
    # Define la validación que cada servicio especializado debe resolver según sus datos.
    def validar_parametros(self, **kwargs) -> None:
        # Los parámetros cambian según se trate de una sala, un equipo o una asesoría.
        raise NotImplementedError

    # Interpreta los argumentos recibidos y calcula el costo con las opciones de impuesto y descuento.
    def calcular_costo(self, *args, **kwargs) -> float:
        """Calcula el valor y permite distintas formas de enviar los parámetros."""
        # Python no tiene sobrecarga tradicional por firma como otros lenguajes.
        # Por eso se reciben argumentos variables y se interpretan las variantes aquí.
        if len(args) > 3:
            raise ValidationError("Se permiten como máximo tres argumentos posicionales.")

        # Se copia el diccionario para revisar los argumentos sin modificar el original.
        parametros = dict(kwargs)
        # Solo se aceptan estos tres nombres para evitar parámetros escritos por error.
        permitidos = {"horas", "impuesto", "descuento"}
        # La diferencia entre conjuntos identifica los nombres que el método no reconoce.
        desconocidos = set(parametros) - permitidos
        if desconocidos:
            raise ValidationError(f"Parámetros no reconocidos: {', '.join(sorted(desconocidos))}.")

        # No se permite enviar el mismo dato dos veces, por posición y por nombre.
        if args and "horas" in parametros:
            raise ValidationError("La duración se indicó más de una vez.")
        if len(args) > 1 and "impuesto" in parametros:
            raise ValidationError("El impuesto se indicó más de una vez.")
        if len(args) > 2 and "descuento" in parametros:
            raise ValidationError("El descuento se indicó más de una vez.")

        # Se asignan valores por defecto cuando no se envía impuesto o descuento.
        # La duración puede llegar como primer argumento posicional o con el nombre horas.
        horas = args[0] if args else parametros.get("horas")
        impuesto = args[1] if len(args) > 1 else parametros.get("impuesto", 0.0)
        descuento = args[2] if len(args) > 2 else parametros.get("descuento", 0.0)

        # Todos los valores deben ser números finitos; bool se excluye aunque herede de int.
        # Se revisan los tres valores en un mismo ciclo para aplicar la misma regla numérica.
        for nombre, valor in (("duración", horas), ("impuesto", impuesto), ("descuento", descuento)):
            if (isinstance(valor, bool) or not isinstance(valor, Real)
                    or not isfinite(float(valor))):
                raise ValidationError(f"El valor de {nombre} debe ser numérico y finito.")

        # La duración debe ser positiva y los porcentajes deben estar entre 0 y 1.
        if horas <= 0:
            raise ValidationError("La duración debe ser mayor que cero.")
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise ValidationError("Impuesto y descuento deben estar entre 0 y 1.")

        # Primero se calcula el subtotal, luego se aplica descuento e impuesto.
        # El subtotal corresponde a la tarifa por hora multiplicada por el tiempo contratado.
        subtotal = self.tarifa_hora * float(horas)
        # Primero se resta el descuento y luego se suma el impuesto al valor resultante.
        total = subtotal * (1 - float(descuento)) * (1 + float(impuesto))
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio para reservar salas de reuniones o espacios de trabajo."""

    # Obliga a cada tipo de servicio a construir una descripción propia.
    def describir(self) -> str:
        # La descripción cambia según el servicio, aunque el método tenga el mismo nombre.
        return f"Reserva de sala: {self.nombre} (${self.tarifa_hora:.2f}/hora)"

    # Define la validación que cada servicio especializado debe resolver según sus datos.
    def validar_parametros(self, **kwargs) -> None:
        # La capacidad se recibe como argumento nombrado para que la llamada sea más clara.
        capacidad = kwargs.get("capacidad")
        # La capacidad se representa como un número entero positivo de personas.
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad < 1:
            raise ValidationError("La capacidad de la sala debe ser un entero positivo.")


class AlquilerEquipo(Servicio):
    """Servicio para alquilar equipos por una cantidad de horas."""

    # Obliga a cada tipo de servicio a construir una descripción propia.
    def describir(self) -> str:
        return f"Alquiler de equipo: {self.nombre} (${self.tarifa_hora:.2f}/hora)"

    # Define la validación que cada servicio especializado debe resolver según sus datos.
    def validar_parametros(self, **kwargs) -> None:
        # Si el usuario no indica cantidad, se toma un equipo como valor inicial.
        cantidad = kwargs.get("cantidad", 1)
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad < 1:
            raise ValidationError("La cantidad de equipos debe ser un entero positivo.")


class Asesoria(Servicio):
    """Servicio de acompañamiento o asesoría especializada."""

    # Obliga a cada tipo de servicio a construir una descripción propia.
    def describir(self) -> str:
        return f"Asesoría especializada: {self.nombre} (${self.tarifa_hora:.2f}/hora)"

    # Define la validación que cada servicio especializado debe resolver según sus datos.
    def validar_parametros(self, **kwargs) -> None:
        # La asesoría debe tener identificado al profesional que la va a prestar.
        especialista = kwargs.get("especialista")
        # Se necesita conocer quién presta la asesoría para aceptar los parámetros.
        if not isinstance(especialista, str) or len(especialista.strip()) < 3:
            raise ValidationError("Debe indicar el nombre del especialista.")
