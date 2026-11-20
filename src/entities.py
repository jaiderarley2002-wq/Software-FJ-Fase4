"""Entidades principales del sistema mediante abstracción y encapsulación."""

# ABC y abstractmethod sirven para crear clases abstractas y métodos obligatorios.
from abc import ABC, abstractmethod

# Importamos el error que vamos a utilizar cuando un dato no sea válido.
from .exceptions import ValidationError

# Usamos esta función para dejar constancia cuando se crea un cliente.
from .logger_config import registrar_evento


# Esta clase reúne las características que pueden compartir las entidades.
class Entidad(ABC):
    """Representa una entidad general identificable del sistema."""

    def __init__(self, identificador: str):
        # Revisamos que el identificador tenga contenido antes de guardarlo.
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValidationError("El identificador es obligatorio.")

        # El guion bajo indica que el atributo se maneja como dato interno.
        self._identificador = identificador.strip()

    @property
    def identificador(self) -> str:
        # Esta propiedad permite consultar el identificador sin modificarlo directamente.
        return self._identificador

    @abstractmethod
    def describir(self) -> str:
        # Las clases que hereden de Entidad deben implementar su propia descripción.
        """Devuelve una descripción de la entidad."""
        raise NotImplementedError


# Cliente hereda de Entidad y agrega los datos que necesita nuestro sistema.
class Cliente(Entidad):
    """Cliente con datos personales encapsulados y validados."""

    def __init__(self, identificador: str, nombre: str, correo: str, telefono: str):
        # Primero inicializamos la parte que viene de la clase padre.
        super().__init__(identificador)

        # Asignamos los datos usando propiedades para que pasen por sus validaciones.
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

        # Guardamos en el log que el cliente se creó correctamente.
        registrar_evento(f"Cliente creado: {self.identificador}")

    @property
    def nombre(self) -> str:
        # Devolvemos el nombre que está guardado como atributo interno.
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        # Evitamos nombres vacíos o con menos de dos caracteres.
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ValidationError("El nombre debe tener al menos dos caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        # Permitimos consultar el correo guardado del cliente.
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        # Hacemos una validación básica para evitar correos sin formato.
        if not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            raise ValidationError("El correo electrónico no tiene un formato válido.")
        # Guardamos el correo sin espacios externos y en minúsculas.
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        # Devolvemos el teléfono del cliente.
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        # El teléfono debe tener solo números y al menos siete dígitos.
        if not isinstance(valor, str) or not valor.isdigit() or len(valor) < 7:
            raise ValidationError("El teléfono debe contener al menos siete dígitos.")
        self._telefono = valor

    def describir(self) -> str:
        # Esta descripción se utiliza cuando mostramos los datos del cliente.
        return f"Cliente {self.nombre} | {self.correo} | {self.telefono}"
