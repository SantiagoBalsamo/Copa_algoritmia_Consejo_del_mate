# 🏟️ La Cancha Inteligente

**Desafío 3 — Copa de Algoritmia y Programación UADE 2026**  
Dirección Carreras de Informática y Sistemas

---

## Descripción

Simulador de posicionamiento táctico para un partido del Mundial. La cancha se representa como una **matriz de 100 × 60 celdas** y permite registrar jugadores, moverlos, calcular distancias y detectar situaciones ofensivas entre Argentina y Brasil.

---

## Requisitos

- Python 3.8 o superior
- Sin dependencias externas (solo librería estándar)

---

## Cómo ejecutar

```bash
python la_cancha_inteligente.py
```

El programa corre todos los casos de prueba automáticamente y muestra los resultados por consola.

---

## Estructura del proyecto

```
la_cancha_inteligente.py   # Programa principal
README.md                  # Este archivo
```

---

## Representación de la cancha

| Símbolo | Significado          |
|---------|----------------------|
| `.`     | Celda vacía          |
| `A`     | Jugador de Argentina |
| `B`     | Jugador de Brasil    |
| `X`     | Obstáculo / zona bloqueada |

- **Dimensiones:** 100 filas (0–99) × 60 columnas (0–59)
- **Arco de Argentina:** columna 0 — ataca hacia la derecha
- **Arco de Brasil:** columna 59 — ataca hacia la izquierda
- La pelota siempre comparte posición con un jugador (no ocupa celda propia)

---

## Estructura de un jugador

Cada jugador se representa con un diccionario Python:

```python
jugador = {
    "nombre":       "Messi",        # str — debe ser único
    "equipo":       "A",            # "A" (Argentina) | "B" (Brasil)
    "fila":         50,             # int 0–99
    "columna":      40,             # int 0–59
    "rol":          "delantero",    # arquero | defensor | mediocampista | delantero
    "tiene_pelota": True            # bool estricto — solo un jugador a la vez
}
```

---

## Funciones principales

### `crear_cancha()`
Genera y retorna la matriz 100 × 60 inicializada con `"."`.

---

### `posicionar_jugador(cancha, jugadores, jugador)`
Agrega un jugador a la cancha con las siguientes validaciones (en orden):

1. Nombre no duplicado
2. Posición dentro de los límites
3. Celda sin obstáculo `X` *(mensaje diferenciado)*
4. Celda sin jugador previo *(mensaje diferenciado)*
5. `tiene_pelota` es estrictamente `bool` (rechaza `1`, `"True"`, `None`)
6. Equipo válido (`"A"` o `"B"`)
7. Rol válido (`arquero`, `defensor`, `mediocampista`, `delantero`)
8. Pelota no duplicada (solo un portador a la vez)

---

### `mover_jugador(cancha, jugadores, nombre, direccion)`
Mueve un jugador una celda en la dirección indicada (`"arriba"`, `"abajo"`, `"izquierda"`, `"derecha"`).

Valida que el destino no esté fuera de la cancha, no sea un obstáculo `X` ni una celda con otro jugador. Retorna `True` si el movimiento fue exitoso, `False` si no.

---

### `calcular_distancias(jugadores)`
Calcula la **distancia Manhattan** entre cada jugador y el portador de la pelota:

```
distancia = |fila_jugador - fila_pelota| + |columna_jugador - columna_pelota|
```

Muestra todas las distancias e indica el/los jugadores más cercanos. En caso de empate, lista todos.

---

### `detectar_pases(cancha, jugadores)`
Lista todos los pases posibles para el jugador con la pelota. Un pase es válido si:

- Ambos son del mismo equipo
- Están en la misma fila **o** la misma columna (sin diagonales)
- No hay rivales ni obstáculos `X` entre ellos
- Los compañeros de equipo **no** bloquean el pase

---

### `detectar_camino_libre(cancha, jugadores)`
Detecta qué **delanteros** tienen camino libre al arco rival. Condiciones:

- Rol: `delantero`
- Está en la mitad ofensiva de su equipo:
  - Argentina: columnas 30–59
  - Brasil: columnas 0–29
- No hay rivales ni obstáculos `X` en su misma fila entre él y el arco rival
- Los compañeros de equipo **no** bloquean el camino

---

### Funciones auxiliares

| Función | Descripción |
|---|---|
| `agregar_obstaculo(cancha, fila, columna)` | Coloca un `"X"` en la posición indicada |
| `mostrar_seccion_cancha(cancha, fi, ff, ci, cf)` | Imprime un recorte de la cancha para visualización |
| `_buscar_jugador(jugadores, nombre)` | Retorna el dict del jugador por nombre, o `None` |
| `_buscar_portador(jugadores)` | Retorna el dict del jugador con la pelota, o `None` |

---

## Casos de prueba cubiertos

El bloque `if __name__ == "__main__"` ejecuta los siguientes escenarios:

| Caso | Resultado esperado |
|---|---|
| Jugadores válidos de ambos equipos | `[OK]` con datos completos |
| Nombre duplicado | `[ERROR]` nombre ya existe |
| Posición fuera de la cancha | `[ERROR]` fuera de límites |
| Posicionar sobre obstáculo `X` | `[ERROR]` contiene obstáculo |
| Posicionar sobre otro jugador | `[ERROR]` celda con jugador |
| `tiene_pelota = 1` / `"True"` / `None` | `[ERROR]` tipo inválido |
| Rol inválido | `[ERROR]` rol no reconocido |
| Equipo inválido | `[ERROR]` equipo no reconocido |
| Dos jugadores con pelota | `[ERROR]` ya hay portador |
| Movimiento válido | `[MOVIMIENTO OK]` |
| Movimiento hacia `X` | `[MOVIMIENTO INVÁLIDO]` |
| Movimiento hacia jugador | `[MOVIMIENTO INVÁLIDO]` |
| Movimiento fuera de la cancha | `[MOVIMIENTO INVÁLIDO]` |
| Distancia Manhattan | Distancias + jugador más cercano |
| Empate en distancia | Lista todos los empatados |
| Pase válido entre compañeros | `[PASE POSIBLE]` |
| Pase bloqueado por rival/obstáculo | `[BLOQUEADO]` |
| Pase diagonal (no en línea recta) | `[BLOQUEADO]` |
| Delantero con camino libre | `[CAMINO LIBRE]` |
| Delantero bloqueado por rival/X | `[SIN CAMINO LIBRE]` |
| Delantero fuera de mitad ofensiva | `[SIN CAMINO LIBRE]` |

---

## Restricciones del programa

- ✅ Usa matrices, funciones y diccionarios
- ✅ Valida todas las entradas antes de modificar el estado
- ✅ Mantiene la matriz sincronizada tras cada operación
- ✅ Solo librerías estándar de Python
- ❌ No usa clases
- ❌ No usa librerías externas
- ❌ No modifica posiciones sin validación previa