# Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto académico del curso Programación (213023), Fase 4 - Prácticas simuladas. El sistema permite registrar clientes, administrar servicios y gestionar reservas aplicando programación orientada a objetos y manejo de excepciones.

## Requisitos

- Python 3.10 o superior.
- No requiere instalar paquetes externos.
- No utiliza bases de datos; los objetos se administran en listas durante la ejecución.

## Ejecución

Desde la carpeta raíz del proyecto, ejecute:

```bash
python main.py
```

El programa recorre 26 escenarios válidos e inválidos. El resultado de la última ejecución se guarda en `resultado_pruebas.txt`. Los eventos y errores se registran en `logs/software_fj.log`.

## Organización del proyecto

- `main.py`: punto de entrada y escenarios de simulación. Incluye comentarios para explicar el orden de las pruebas y el manejo de errores.
- `src/entities.py`: clase abstracta `Entidad` y clase `Cliente`, con propiedades para validar sus datos.
- `src/services.py`: clase abstracta `Servicio` y sus tres clases especializadas.
- `src/reservations.py`: clase `Reserva` y control de los estados de una reserva.
- `src/exceptions.py`: excepciones personalizadas del sistema.
- `src/logger_config.py`: configuración del registro de eventos y errores.
- `logs/`: carpeta donde se crea el archivo de registro al ejecutar el programa.

## Conceptos aplicados

- Abstracción, herencia, encapsulación y polimorfismo.
- Validación de clientes, servicios, tarifas, duraciones y operaciones de reservas.
- Variantes del cálculo de costos usando argumentos posicionales y opcionales.
- Excepciones personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento de excepciones.
- Registro de operaciones y errores con el módulo `logging`.
- Listas en memoria para administrar clientes, servicios y reservas.

## Sobre los comentarios del código

El código incluye comentarios en español distribuidos en los módulos principales. Se explica el propósito de las funciones y métodos, las validaciones de datos, la relación entre clientes, servicios y reservas, los cambios de estado, las variantes del cálculo de costos, el registro de eventos y el manejo de excepciones. Los comentarios buscan aclarar la lógica de cada bloque sin repetir literalmente las instrucciones.
