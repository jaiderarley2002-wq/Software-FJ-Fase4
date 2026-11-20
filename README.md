# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto académico desarrollado en Python para demostrar programación orientada a objetos y manejo robusto de excepciones.

## Requisitos
- Python 3.10 o superior.
- No requiere instalar paquetes externos.

## Ejecución
Desde la carpeta raíz del proyecto:

```bash
python main.py
```

## Estructura
- `main.py`: punto de entrada y escenarios de prueba.
- `src/entities.py`: clase abstracta `Entidad` y clase `Cliente`.
- `src/services.py`: clase abstracta `Servicio` y servicios especializados.
- `src/reservations.py`: gestión de reservas y estados.
- `src/exceptions.py`: excepciones personalizadas.
- `src/logger_config.py`: registro de eventos y errores.
- `logs/software_fj.log`: archivo generado durante la ejecución.

## Características
- Abstracción, herencia, encapsulación y polimorfismo.
- Variantes de cálculo de costos mediante argumentos variables y opcionales.
- Excepciones personalizadas, `try/except/else/finally` y encadenamiento.
- Catorce escenarios de prueba válidos e inválidos.
- Registro de eventos y errores en archivo de log.

## Nota
La información de clientes, servicios y reservas se mantiene en memoria mediante objetos y listas/diccionarios durante la ejecución. No se utiliza motor de base de datos.

## Comentarios del código
Los módulos de Python incluyen comentarios en español que explican la finalidad de las clases,
las validaciones, los métodos y los bloques principales del programa. Se busca que la lectura
sea clara para un estudiante que está aplicando los conceptos vistos en el curso.
