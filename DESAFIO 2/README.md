### Copa de Algoritmia y Programación UADE 2026
# Desafío 2 — Predicción de Penales

## Descripción

Sistema que analiza el historial de penales de un jugador rival para predecir su dirección más frecuente, con el objetivo de asistir al arquero en la toma de decisiones.

## Estructura del proyecto

```
DESAFIO 2/
├── desafio2.py
└── penales.txt
```

## Formato de entrada

El archivo `penales.txt` debe contener una sola línea con la secuencia de penales, donde cada carácter representa una dirección:

| Carácter | Dirección |
|----------|-----------|
| L | Izquierda |
| R | Derecha |
| C | Centro |

Ejemplo:
'''
LRRCLRRLLR

'''

## Formato de salida

La dirección más frecuente en la primera línea y su cantidad de apariciones en la segunda:

```
R
5
```

## Reglas

- La secuencia debe tener entre 1 y 1000 caracteres.
- Solo se permiten los caracteres `L`, `R` y `C`.
- En caso de empate, se aplica la prioridad táctica: `L > R > C`.

## Ejemplos

| Entrada | Salida |
|--------|--------|
| `LRRCLRRLLR` | `R / 5` |
| `LLLLL` | `L / 5` |
| `CRCRCRR` | `R / 4` |
| `LLRR` | `L / 2` |

## Manejo de errores

| Error | Mensaje |
|-------|---------|
| Archivo no encontrado | `ERROR: EL ARCHIVO 'nombre' NO EXISTE EN EL DIRECTORIO` |
| Archivo vacío | `El archivo está vacío.` |
| Secuencia mayor a 1000 caracteres | `La secuencia supera los 1000 caracteres.` |
| Carácter inválido | `Carácter inválido encontrado: 'X'. Solo se permiten L, R y C.` |

## Funciones

| Función | Descripción |
|---------|-------------|
| `leer_archivo(nombre_archivo)` | Lee el archivo y devuelve su contenido en mayúsculas sin espacios ni saltos de línea. |
| `validar_secuencia(secuencia)` | Valida longitud y caracteres de la secuencia. |
| `contar_direcciones(secuencia)` | Cuenta las apariciones de cada dirección. |
| `mayor_cantidad(cant_L, cant_R, cant_C)` | Retorna la dirección más frecuente respetando el desempate `L > R > C`. |
| `mostrar_resultado(direccion, maximo)` | Muestra la dirección ganadora y su frecuencia. |

## Compatibilidad

El programa elimina `\r` y `\n` al leer el archivo, por lo que es compatible con archivos creados en Windows, Linux y Mac.

## Requisitos

- Python 3.7 o superior.
- No requiere librerías externas.
- Compatible con Windows, Linux y Mac.

## Ejecución

```bash
python desafio2.py
```

## Autores

- Nombre 1
- Nombre 2
- Nombre 3
- Nombre 4
- Nombre 5

Copa de Algoritmia y Programación UADE 2026