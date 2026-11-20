"""Punto de entrada y demostración de diez o más operaciones del sistema."""

# Importamos la clase para crear y validar clientes.
from src.entities import Cliente

# Importamos los tres tipos de servicio que ofrece Software FJ.
from src.services import ReservaSala, AlquilerEquipo, Asesoria

# Importamos la clase que permite crear y procesar reservas.
from src.reservations import Reserva

# Usamos la excepción base para capturar errores propios del sistema.
from src.exceptions import SoftwareFJError, ValidationError

# Estas funciones permiten guardar los resultados y errores en el archivo de log.
from src.logger_config import registrar_evento, registrar_error


def ejecutar_prueba(numero: int, descripcion: str, operacion) -> None:
    """Ejecuta cada escenario por separado para que un error no detenga los demás."""
    print(f"\n[{numero}] {descripcion}")

    # Intentamos ejecutar la operación que corresponde al escenario.
    try:
        resultado = operacion()

    # Capturamos primero los errores que fueron creados para este proyecto.
    except SoftwareFJError as error:
        registrar_error(f"Escenario {numero}: {error}")
        print(f"Error controlado: {error}")

    # Si aparece otro error no previsto, también lo controlamos y lo registramos.
    except Exception as error:
        registrar_error(f"Escenario {numero}, error inesperado: {error}")
        print(f"Error inesperado controlado: {error}")

    # Este bloque solo se ejecuta cuando la operación termina sin errores.
    else:
        print(f"Resultado: {resultado}")
        registrar_evento(f"Escenario {numero} ejecutado correctamente")

    # Este mensaje se muestra tanto si la operación sale bien como si falla.
    finally:
        print("Fin del escenario.")


def main() -> None:
    """Crea los datos de ejemplo y ejecuta todos los escenarios."""
    print("=" * 62)
    print(" SOFTWARE FJ - GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")
    print("=" * 62)

    # Usamos diccionarios en memoria para administrar los objetos del ejercicio.
    clientes = {}

    # Creamos los servicios disponibles y uno adicional para probar un error.
    servicios = {
        "SALA01": ReservaSala("SALA01", "Sala de reuniones", 45000),
        "EQ01": AlquilerEquipo("EQ01", "Proyector", 18000),
        "ASE01": Asesoria("ASE01", "Asesoría en software", 60000),
        "EQ02": AlquilerEquipo("EQ02", "Equipo no disponible", 12000, disponible=False),
    }

    # Esta función crea un cliente con datos que cumplen las validaciones.
    def crear_cliente():
        cliente = Cliente("C001", "Laura Méndez", "laura@email.com", "3001234567")
        clientes[cliente.identificador] = cliente
        return cliente.describir()

    # En este caso usamos datos incorrectos para comprobar las excepciones.
    def cliente_invalido():
        return Cliente("C002", "A", "correo-invalido", "123")

    # Creamos un segundo cliente para usarlo en otras pruebas.
    def crear_segundo_cliente():
        cliente = Cliente("C003", "Carlos Pérez", "carlos@email.com", "3107654321")
        clientes[cliente.identificador] = cliente
        return cliente.describir()

    # Probamos la validación de una sala con una capacidad permitida.
    def validar_sala():
        servicios["SALA01"].validar_parametros(capacidad=12)
        return "Parámetros de sala válidos"

    # Aquí enviamos una cantidad de equipos igual a cero para generar un error.
    def validar_equipo_invalido():
        servicios["EQ01"].validar_parametros(cantidad=0)
        return "Equipo validado"

    # Creamos una reserva de sala usando un cliente y un servicio existentes.
    def crear_reserva_sala():
        reserva = Reserva("R001", clientes["C001"], servicios["SALA01"], 2)
        reservas[reserva.identificador] = reserva
        return reserva.describir()

    # Cambiamos la reserva de pendiente a confirmada.
    def confirmar_reserva():
        reservas["R001"].confirmar()
        return reservas["R001"].describir()

    # Procesamos la reserva y aplicamos el impuesto y el descuento de la prueba.
    def procesar_reserva():
        return f"Total: ${reservas['R001'].procesar(impuesto=0.19, descuento=0.10):,.2f}"

    # Intentamos confirmar una reserva cuyo servicio está marcado como no disponible.
    def reserva_servicio_no_disponible():
        reserva = Reserva("R002", clientes["C003"], servicios["EQ02"], 1)
        reserva.confirmar()
        return reserva.describir()

    # Intentamos procesar una reserva que todavía no ha sido confirmada.
    def procesar_reserva_pendiente():
        reserva = Reserva("R003", clientes["C003"], servicios["ASE01"], 1)
        return reserva.procesar()

    # Cancelamos la reserva principal para probar el cambio de estado.
    def cancelar_reserva():
        reservas["R001"].cancelar()
        return reservas["R001"].describir()

    # Volvemos a cancelar la misma reserva para comprobar que el sistema controle el error.
    def cancelar_dos_veces():
        reservas["R001"].cancelar()
        return "Cancelación repetida"

    # Enviamos una duración negativa para probar la validación del costo.
    def costo_con_argumentos_invalidos():
        return servicios["SALA01"].calcular_costo(-2)

    # Este escenario convierte un texto inválido y luego encadena una excepción propia.
    def encadenar_error():
        try:
            int("dato-no-numerico")
        except ValueError as error:
            # 'from error' conserva la causa original para poder rastrear el problema.
            raise ValidationError("No fue posible convertir el dato recibido.") from error

    # Aquí se guardarán las reservas que se vayan creando durante las pruebas.
    reservas = {}

    # Organizamos los escenarios en una lista para ejecutarlos uno por uno.
    escenarios = [
        ("Registro válido de cliente", crear_cliente),
        ("Registro inválido de cliente", cliente_invalido),
        ("Segundo registro válido de cliente", crear_segundo_cliente),
        ("Validación correcta de parámetros de sala", validar_sala),
        ("Validación incorrecta de cantidad de equipos", validar_equipo_invalido),
        ("Creación correcta de reserva", crear_reserva_sala),
        ("Confirmación de reserva", confirmar_reserva),
        ("Procesamiento y cálculo de reserva", procesar_reserva),
        ("Intento de reserva con servicio no disponible", reserva_servicio_no_disponible),
        ("Intento de procesar reserva pendiente", procesar_reserva_pendiente),
        ("Cancelación de reserva", cancelar_reserva),
        ("Intento de cancelar dos veces", cancelar_dos_veces),
        ("Cálculo con duración inválida", costo_con_argumentos_invalidos),
        ("Encadenamiento de excepciones", encadenar_error),
    ]

    # enumerate numera las pruebas empezando desde uno.
    for numero, (descripcion, operacion) in enumerate(escenarios, start=1):
        ejecutar_prueba(numero, descripcion, operacion)

    # Al final mostramos cuántas operaciones se intentaron ejecutar.
    print("\n" + "=" * 62)
    print(f"Simulaciones ejecutadas: {len(escenarios)}")
    print("Revise logs/software_fj.log para consultar eventos y errores.")
    print("El sistema finalizó sin interrumpirse por los errores simulados.")
    print("=" * 62)


# Este bloque hace que main() se ejecute solamente al iniciar este archivo directamente.
if __name__ == "__main__":
    try:
        # Iniciamos el programa principal con todas las simulaciones.
        main()
    except Exception as error:
        # Si ocurre un error general, lo registramos para no perder la información.
        registrar_error(f"Error crítico controlado en la aplicación: {error}")
        print(f"No fue posible completar la ejecución: {error}")
    finally:
        # Este mensaje se muestra siempre al cerrar la aplicación.
        print("Aplicación Software FJ finalizada.")
