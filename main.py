"""Programa principal: crea datos de ejemplo y ejecuta las pruebas del sistema."""

from src.entities import Cliente
from src.services import Servicio, ReservaSala, AlquilerEquipo, Asesoria
from src.reservations import Reserva
from src.exceptions import (
    SoftwareFJError, ValidationError, DuplicateClientError
)
from src.logger_config import registrar_evento, registrar_error


# Esta función ejecuta una prueba por separado y controla sus errores para que no afecten los escenarios siguientes.
def ejecutar_prueba(numero: int, descripcion: str, operacion) -> None:
    """Ejecuta un escenario aislado para que un error no detenga los demás."""
    print(f"\n[{numero}] {descripcion}")

    # Cada escenario tiene su propio try para poder continuar con el siguiente,
    # incluso cuando la operación que se está probando genera una excepción.
    try:
        resultado = operacion()
    except SoftwareFJError as error:
        # Los errores definidos para el proyecto se registran como errores controlados.
        registrar_error(f"Escenario {numero}: {error}")
        print(f"Error controlado: {error}")
    except Exception as error:
        # Este segundo except sirve como respaldo para errores no previstos.
        registrar_error(f"Escenario {numero}, error inesperado: {error}")
        print(f"Error inesperado controlado: {error}")
    else:
        # El bloque else solo se ejecuta cuando la operación termina sin excepción.
        print(f"Resultado: {resultado}")
        registrar_evento(f"Escenario {numero} ejecutado correctamente")
    finally:
        # El mensaje se muestra tanto si la prueba fue correcta como si falló.
        print("Fin del escenario.")


# Aquí se preparan los datos de ejemplo, las listas de trabajo y la secuencia completa de simulaciones.
def main() -> None:
    """Crea los objetos en memoria y recorre las simulaciones válidas e inválidas."""
    print("=" * 64)
    print(" SOFTWARE FJ - GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")
    print("=" * 64)

    # El ejercicio no usa base de datos: los objetos se guardan en listas durante la ejecución.
    # Las tres listas mantienen los objetos mientras el programa está en ejecución; no se usa una base de datos.
    clientes: list[Cliente] = []
    servicios: list[Servicio] = []
    reservas: list[Reserva] = []

    # Estas funciones buscan los objetos por su código o identificador para reutilizarlos.
    # next() obtiene el primer elemento que coincide; en estas pruebas los datos existen.
    # Busca un cliente que ya fue registrado para poder relacionarlo después con una reserva.
    # La búsqueda recorre la lista y devuelve el primer identificador que coincide.
    def buscar_cliente(identificador: str) -> Cliente:
        return next(cliente for cliente in clientes if cliente.identificador == identificador)

    # Localiza un servicio por su código; así las reservas usan el mismo objeto creado en las pruebas.
    # El código del servicio funciona como referencia para encontrar el objeto correcto.
    def buscar_servicio(codigo: str) -> Servicio:
        return next(servicio for servicio in servicios if servicio.codigo == codigo)

    # Recupera una reserva existente para cambiar su estado o intentar procesarla.
    # Se usa el identificador de reserva para consultar y actualizar el mismo objeto.
    def buscar_reserva(identificador: str) -> Reserva:
        return next(reserva for reserva in reservas if reserva.identificador == identificador)

    # Centraliza el registro de clientes y evita que dos personas tengan el mismo identificador.
    def registrar_cliente(cliente: Cliente) -> str:
        # Antes de agregarlo a la lista se revisa que el identificador no esté repetido.
        if any(actual.identificador == cliente.identificador for actual in clientes):
            raise DuplicateClientError(
                f"Ya existe un cliente con el identificador {cliente.identificador}."
            )
        # La lista se actualiza solo después de pasar la comprobación de duplicados.
        clientes.append(cliente)
        return cliente.describir()

    # ----------------------- Pruebas de clientes -----------------------
    # Prueba el registro de un cliente cuyos datos cumplen las validaciones.
    def crear_cliente_valido():
        return registrar_cliente(
            Cliente("C001", "Laura Méndez", "laura@email.com", "3001234567")
        )

    # Envía datos intencionalmente incorrectos para comprobar que Cliente rechace el registro.
    def crear_cliente_invalido():
        # Este registro se rechaza porque el nombre, correo y teléfono no cumplen las reglas.
        return registrar_cliente(Cliente("C002", "A", "correo-invalido", "123"))

    # Intenta repetir un identificador para comprobar el control de clientes duplicados.
    def registrar_cliente_duplicado():
        # Se intenta usar otra vez C001 para comprobar la excepción de duplicados.
        if any(cliente.identificador == "C001" for cliente in clientes):
            raise DuplicateClientError("Ya existe un cliente con el identificador C001.")
        return registrar_cliente(
            Cliente("C001", "Laura Méndez", "laura@email.com", "3001234567")
        )

    # Agrega otro cliente válido para tener más de una persona disponible en las reservas.
    def crear_segundo_cliente():
        return registrar_cliente(
            Cliente("C003", "Carlos Pérez", "carlos@email.com", "3107654321")
        )

    # ----------------------- Pruebas de servicios ----------------------
    # Crea una sala de reuniones y la agrega a la lista de servicios disponibles.
    def crear_sala():
        # Se construye el objeto con su tarifa por hora y sus datos propios.
        servicio = ReservaSala("SALA01", "Sala de reuniones", 45000)
        servicios.append(servicio)
        return servicio.describir()

    # Crea el servicio de alquiler de un proyector y lo guarda en memoria.
    def crear_equipo():
        # La disponibilidad falsa permite probar el rechazo al confirmar una reserva.
        servicio = AlquilerEquipo("EQ01", "Proyector", 18000)
        servicios.append(servicio)
        return servicio.describir()

    # Registra una asesoría especializada como tercer tipo de servicio.
    def crear_asesoria():
        servicio = Asesoria("ASE01", "Asesoría en software", 60000)
        servicios.append(servicio)
        return servicio.describir()

    # Prueba una tarifa igual a cero, que debe ser rechazada por la clase Servicio.
    def crear_servicio_invalido():
        # La tarifa cero no está permitida y debe producir ValidationError.
        return ReservaSala("SALA02", "Sala inválida", 0)

    # Crea un equipo que existe en el sistema, pero que no puede reservarse por ahora.
    def crear_servicio_no_disponible():
        # El objeto se crea, pero su disponibilidad queda marcada como falsa.
        servicio = AlquilerEquipo(
            "EQ02", "Equipo no disponible", 12000, disponible=False
        )
        servicios.append(servicio)
        return servicio.describir()

    # Comprueba que una capacidad positiva sea aceptada por el servicio de salas.
    def validar_sala():
        buscar_servicio("SALA01").validar_parametros(capacidad=12)
        return "Capacidad de sala válida"

    # Envía una cantidad igual a cero para verificar la validación del alquiler de equipos.
    def validar_equipo_invalido():
        # La cantidad cero se usa para comprobar el rechazo de un parámetro incorrecto.
        buscar_servicio("EQ01").validar_parametros(cantidad=0)
        return "Cantidad de equipos válida"

    # ----------------------- Pruebas de reservas -----------------------
    # Relaciona al primer cliente con la sala y deja la reserva lista para confirmarse.
    def crear_reserva_principal():
        # Primero se relacionan los objetos existentes y después se guarda la reserva.
        reserva = Reserva("R001", buscar_cliente("C001"), buscar_servicio("SALA01"), 2)
        reservas.append(reserva)
        return reserva.describir()

    # Cambia R001 de pendiente a confirmada antes de calcular su valor.
    def confirmar_reserva_principal():
        reserva = buscar_reserva("R001")
        reserva.confirmar()
        return reserva.describir()

    # Procesa la reserva principal y aplica los porcentajes de impuesto y descuento de la prueba.
    def procesar_reserva_principal():
        # Se calcula el valor aplicando 19 % de impuesto y 10 % de descuento.
        # El método procesar delega el cálculo en el servicio vinculado a la reserva.
        total = buscar_reserva("R001").procesar(impuesto=0.19, descuento=0.10)
        return f"Total: ${total:,.2f}"

    # Vuelve a procesar R001 para comprobar que el sistema impida cobrarla por segunda vez.
    def procesar_reserva_repetida():
        # La reserva ya fue procesada; esta segunda llamada debe ser rechazada.
        return buscar_reserva("R001").procesar()

    # Intenta confirmar una reserva asociada a un equipo marcado como no disponible.
    def confirmar_reserva_no_disponible():
        reserva = Reserva("R002", buscar_cliente("C003"), buscar_servicio("EQ02"), 1)
        reservas.append(reserva)
        reserva.confirmar()
        return reserva.describir()

    # Intenta cobrar una reserva que no se confirmó, una operación que debe generar error.
    def procesar_reserva_pendiente():
        # Se deja la reserva en estado pendiente para comprobar que no se cobre sin confirmar.
        reserva = Reserva("R003", buscar_cliente("C003"), buscar_servicio("ASE01"), 1)
        reservas.append(reserva)
        return reserva.procesar()

    # Prepara una reserva independiente que se utilizará en las pruebas de cancelación.
    def crear_reserva_para_cancelar():
        reserva = Reserva("R004", buscar_cliente("C001"), buscar_servicio("SALA01"), 1)
        reservas.append(reserva)
        return reserva.describir()

    # Confirma R004 para que el siguiente escenario pueda cancelarla correctamente.
    def confirmar_reserva_para_cancelar():
        reserva = buscar_reserva("R004")
        reserva.confirmar()
        return reserva.describir()

    # Realiza la cancelación permitida de R004 y permite verificar el nuevo estado.
    def cancelar_reserva():
        reserva = buscar_reserva("R004")
        reserva.cancelar()
        return reserva.describir()

    # Repite la cancelación de R004 para probar que no se pueda cancelar dos veces.
    def cancelar_dos_veces():
        # El segundo intento permite probar que no se cancele una reserva dos veces.
        return buscar_reserva("R004").cancelar()

    # Intenta cancelar una reserva que ya fue procesada y cuyo estado debe conservarse.
    def cancelar_reserva_procesada():
        # R001 ya fue procesada, así que su cancelación no debe permitirse.
        return buscar_reserva("R001").cancelar()

    # Construye una reserva con duración negativa para probar la validación del constructor.
    def duracion_invalida():
        return Reserva("R005", buscar_cliente("C003"), buscar_servicio("SALA01"), -2)

    # ----------------------- Variantes de cálculo ----------------------
    # Compara el cálculo base con las llamadas que también reciben impuesto y descuento.
    def probar_variantes_calculo():
        # Se reutiliza la misma sala para comparar las distintas formas de llamar al cálculo.
        servicio = buscar_servicio("SALA01")
        # Se prueban tres formas: solo duración, duración e impuesto posicional,
        # y duración con impuesto y descuento indicados por nombre.
        return {
            "base": servicio.calcular_costo(1),
            "con_impuesto": servicio.calcular_costo(1, 0.19),
            "con_impuesto_y_descuento": servicio.calcular_costo(
                1, impuesto=0.19, descuento=0.10
            ),
        }

    # Prueba un porcentaje de impuesto fuera del intervalo permitido.
    def calcular_costo_con_parametros_invalidos():
        # Un impuesto superior al 100 % está fuera del rango que maneja el sistema.
        return buscar_servicio("SALA01").calcular_costo(2, impuesto=1.5)

    # Convierte un error nativo de Python en una excepción del proyecto conservando su causa original.
    def encadenar_error():
        try:
            int("dato-no-numerico")
        except ValueError as error:
            # 'from error' permite conservar la causa original al lanzar el error propio.
            raise ValidationError(
                "No fue posible convertir el dato recibido."
            ) from error

    # La lista reúne 26 casos, tanto exitosos como fallidos, para probar el comportamiento.
    # Cada elemento relaciona una descripción legible con la función que debe ejecutarse.
    escenarios = [
        ("Registro válido de cliente", crear_cliente_valido),
        ("Registro inválido de cliente", crear_cliente_invalido),
        ("Intento de registrar un cliente duplicado", registrar_cliente_duplicado),
        ("Registro de un segundo cliente válido", crear_segundo_cliente),
        ("Creación correcta de servicio de sala", crear_sala),
        ("Creación correcta de servicio de alquiler de equipo", crear_equipo),
        ("Creación correcta de servicio de asesoría", crear_asesoria),
        ("Intento de crear un servicio con tarifa inválida", crear_servicio_invalido),
        ("Creación de servicio marcado como no disponible", crear_servicio_no_disponible),
        ("Validación correcta de parámetros de sala", validar_sala),
        ("Validación incorrecta de cantidad de equipos", validar_equipo_invalido),
        ("Creación correcta de reserva", crear_reserva_principal),
        ("Confirmación de reserva", confirmar_reserva_principal),
        ("Procesamiento y cálculo de reserva", procesar_reserva_principal),
        ("Intento de procesar nuevamente una reserva procesada", procesar_reserva_repetida),
        ("Intento de confirmar una reserva con servicio no disponible", confirmar_reserva_no_disponible),
        ("Intento de procesar una reserva pendiente", procesar_reserva_pendiente),
        ("Creación de una reserva para cancelar", crear_reserva_para_cancelar),
        ("Confirmación de la reserva que se va a cancelar", confirmar_reserva_para_cancelar),
        ("Cancelación correcta de reserva", cancelar_reserva),
        ("Intento de cancelar dos veces la misma reserva", cancelar_dos_veces),
        ("Intento de cancelar una reserva ya procesada", cancelar_reserva_procesada),
        ("Intento de crear una reserva con duración inválida", duracion_invalida),
        ("Prueba de variantes para calcular costos", probar_variantes_calculo),
        ("Cálculo con impuesto fuera del rango permitido", calcular_costo_con_parametros_invalidos),
        ("Encadenamiento de excepciones", encadenar_error),
    ]

    # Se enumeran las pruebas desde 1 para que el resultado sea fácil de consultar.
    # enumerate asigna un número consecutivo a cada prueba para identificarla en pantalla y en el log.
    for numero, (descripcion, operacion) in enumerate(escenarios, start=1):
        ejecutar_prueba(numero, descripcion, operacion)

    print("\n" + "=" * 64)
    # El total se obtiene de la misma lista para que coincida con los casos realmente programados.
    print(f"Simulaciones ejecutadas: {len(escenarios)}")
    print("Revise logs/software_fj.log para consultar eventos y errores.")
    print("El sistema finalizó sin interrumpirse por los errores simulados.")
    print("=" * 64)


if __name__ == "__main__":
    try:
        # Desde aquí se inicia el programa cuando se ejecuta python main.py.
        main()
    except Exception as error:
        # Este bloque protege el cierre de la aplicación ante un error general no previsto.
        registrar_error(f"Error crítico controlado en la aplicación: {error}")
        print(f"No fue posible completar la ejecución: {error}")
    finally:
        # Se muestra el cierre incluso si ocurre un error durante la ejecución general.
        print("Aplicación Software FJ finalizada.")
