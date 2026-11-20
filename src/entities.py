"""Clases para representar las entidades generales y los clientes del sistema."""

from abc import ABC, abstractmethod

from .exceptions import ValidationError
from .logger_config import registrar_evento


class Entidad(ABC):
    """Clase base: todas las entidades deben tener identificador y descripción."""

    # Inicializa la entidad con un identificador obligatorio que se reutiliza en las clases derivadas.
    def __init__(self, identificador: str):
        # El identificador se valida desde la clase padre para reutilizar la regla.
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValidationError("El identificador es obligatorio.")
        # Se quitan espacios al inicio y al final para guardar un valor uniforme.
        self._identificador = identificador.strip()

    @property
    # Permite consultar el identificador sin ofrecer un método para modificarlo directamente.
    def identificador(self) -> str:
        # Se entrega el dato mediante una propiedad y no se expone para editarlo directamente.
        return self._identificador

    @abstractmethod
    # Define el método que cada entidad concreta debe implementar para mostrar sus datos.
    def describir(self) -> str:
        # Las clases que hereden de Entidad deben escribir su propia descripción.
        raise NotImplementedError


class Cliente(Entidad):
    """Guarda los datos de un cliente y comprueba que tengan un formato válido."""

    # Inicializa la entidad con un identificador obligatorio que se reutiliza en las clases derivadas.
    def __init__(self, identificador: str, nombre: str, correo: str, telefono: str):
        # Primero se valida el identificador heredado y después los datos del cliente.
        super().__init__(identificador)
        # Al asignar mediante las propiedades se ejecutan los validadores de cada dato.
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        registrar_evento(f"Cliente creado: {self.identificador}")

    @property
    # Devuelve el nombre guardado de forma privada en el objeto Cliente.
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    # Devuelve el nombre guardado de forma privada en el objeto Cliente.
    def nombre(self, valor: str) -> None:
        # Se evita guardar nombres vacíos o de un solo carácter.
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ValidationError("El nombre debe tener al menos dos caracteres.")
        self._nombre = valor.strip()

    @property
    # Devuelve el correo electrónico ya validado y normalizado.
    def correo(self) -> str:
        return self._correo

    @correo.setter
    # Devuelve el correo electrónico ya validado y normalizado.
    def correo(self, valor: str) -> None:
        # El correo se normaliza a minúsculas para mantener un formato uniforme.
        if not isinstance(valor, str):
            raise ValidationError("El correo electrónico debe ser texto.")
        correo = valor.strip().lower()
        # partition separa el usuario y el dominio usando la arroba como referencia.
        usuario, separador, dominio = correo.partition("@")

        # Se revisan las partes básicas del correo antes de asignarlo al objeto.
        if (not separador or not usuario or not dominio or "@" in dominio
                or "." not in dominio or dominio.startswith(".") or dominio.endswith(".")
                or any(caracter.isspace() for caracter in correo)):
            raise ValidationError("El correo electrónico no tiene un formato válido.")
        # El dato solo se guarda cuando pasó todas las comprobaciones anteriores.
        self._correo = correo

    @property
    # Devuelve el teléfono que pasó las reglas de formato.
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    # Devuelve el teléfono que pasó las reglas de formato.
    def telefono(self, valor: str) -> None:
        # Para este ejercicio se aceptan teléfonos formados únicamente por dígitos.
        if not isinstance(valor, str) or not valor.isdigit() or not 7 <= len(valor) <= 15:
            raise ValidationError("El teléfono debe contener entre 7 y 15 dígitos.")
        # Se conserva el teléfono como texto para no perder posibles ceros iniciales.
        self._telefono = valor

    # Define el método que cada entidad concreta debe implementar para mostrar sus datos.
    def describir(self) -> str:
        # Este método cumple el contrato definido por la clase abstracta Entidad.
        return f"Cliente {self.nombre} | {self.correo} | {self.telefono}"
