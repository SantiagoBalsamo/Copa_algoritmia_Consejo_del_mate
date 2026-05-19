# ============================================================
#  Copa de Algoritmia y Programación - UADE 2026
#  DESAFÍO 3: "LA CANCHA INTELIGENTE"
# ============================================================

# ── Constantes ──────────────────────────────────────────────
FILAS    = 100
COLUMNAS = 60
EQUIPOS_VALIDOS = ("A", "B")
ROLES_VALIDOS   = ("arquero", "defensor", "mediocampista", "delantero")


# ════════════════════════════════════════════════════════════
#  TAREA 1 – Crear la cancha
# ════════════════════════════════════════════════════════════
def crear_cancha():
    """Retorna una matriz 100×60 inicializada con '.'."""
    cancha = []
    for _ in range(FILAS):
        fila = []
        for _ in range(COLUMNAS):
            fila.append(".")
        cancha.append(fila)
    return cancha


# ════════════════════════════════════════════════════════════
#  TAREA 2 – Posicionar jugadores
# ════════════════════════════════════════════════════════════
def posicionar_jugador(cancha, jugadores, nombre, equipo, fila, columna, rol, tiene_pelota):
    """
    Agrega un jugador a la cancha y a la lista de jugadores.
    Retorna True si el registro fue exitoso, False en caso contrario.
    """
    # Validar equipo
    if equipo not in EQUIPOS_VALIDOS:
        print(f"ERROR: Equipo '{equipo}' no válido. Use 'A' o 'B'.")
        return False

    # Validar rol
    if rol not in ROLES_VALIDOS:
        print(f"ERROR: Rol '{rol}' no válido. Use: {', '.join(ROLES_VALIDOS)}.")
        return False

    # Validar límites
    if not (0 <= fila < FILAS and 0 <= columna < COLUMNAS):
        print(f"ERROR: Posición ({fila}, {columna}) fuera de los límites de la cancha.")
        return False

    # Validar celda libre
    if cancha[fila][columna] != ".":
        print(f"ERROR: La celda ({fila}, {columna}) ya está ocupada.")
        return False

    # Validar posesión única de la pelota
    if tiene_pelota:
        for j in jugadores:
            if j["tiene_pelota"]:
                print(f"ERROR: '{j['nombre']}' ya posee la pelota. Solo un jugador puede tenerla.")
                return False

    # Registrar jugador
    jugador = {
        "nombre":      nombre,
        "equipo":      equipo,
        "fila":        fila,
        "columna":     columna,
        "rol":         rol,
        "tiene_pelota": tiene_pelota
    }
    jugadores.append(jugador)
    cancha[fila][columna] = equipo

    print(f"OK: Jugador '{nombre}' ({equipo} - {rol}) agregado en ({fila}, {columna}).", end="")
    if tiene_pelota:
        print(" [tiene la pelota]", end="")
    print()
    return True


# ════════════════════════════════════════════════════════════
#  TAREA 3 – Mover jugadores
# ════════════════════════════════════════════════════════════
def mover_jugador(cancha, jugador, direccion):
    """
    Mueve al jugador una celda en la dirección indicada.
    Direcciones válidas: 'arriba', 'abajo', 'izquierda', 'derecha'.
    Retorna True si el movimiento fue exitoso, False si fue inválido.
    """
    deltas = {
        "arriba":    (-1,  0),
        "abajo":     ( 1,  0),
        "izquierda": ( 0, -1),
        "derecha":   ( 0,  1),
    }

    if direccion not in deltas:
        print(f"ERROR: Dirección '{direccion}' no reconocida.")
        return False

    df, dc = deltas[direccion]
    nueva_fila    = jugador["fila"]    + df
    nueva_columna = jugador["columna"] + dc

    # Validar límites
    if not (0 <= nueva_fila < FILAS and 0 <= nueva_columna < COLUMNAS):
        print(f"MOVIMIENTO INVÁLIDO: '{jugador['nombre']}' no puede moverse hacia {direccion} "
              f"(fuera de la cancha).")
        return False

    celda_destino = cancha[nueva_fila][nueva_columna]

    # Validar obstáculo
    if celda_destino == "X":
        print(f"MOVIMIENTO INVÁLIDO: '{jugador['nombre']}' no puede moverse hacia {direccion} "
              f"(zona bloqueada).")
        return False

    # Validar celda ocupada por jugador
    if celda_destino in ("A", "B"):
        print(f"MOVIMIENTO INVÁLIDO: '{jugador['nombre']}' no puede moverse hacia {direccion} "
              f"(celda ocupada por otro jugador).")
        return False

    # Actualizar matriz y jugador
    cancha[jugador["fila"]][jugador["columna"]] = "."
    cancha[nueva_fila][nueva_columna] = jugador["equipo"]
    jugador["fila"]    = nueva_fila
    jugador["columna"] = nueva_columna

    print(f"MOVIMIENTO OK: '{jugador['nombre']}' se movió {direccion} → ({nueva_fila}, {nueva_columna}).")
    return True


# ════════════════════════════════════════════════════════════
#  TAREA 4 – Calcular distancia Manhattan a la pelota
# ════════════════════════════════════════════════════════════
def calcular_distancias(jugadores):
    """
    Calcula la distancia Manhattan de cada jugador respecto al que tiene la pelota.
    Muestra las distancias e indica el/los jugador/es más cercanos.
    """
    portador = None
    for j in jugadores:
        if j["tiene_pelota"]:
            portador = j
            break

    if portador is None:
        print("ERROR: Ningún jugador tiene la pelota.")
        return

    print(f"\n── Distancias a la pelota (portador: '{portador['nombre']}') ──")
    distancias = []

    for j in jugadores:
        if j is portador:
            continue
        dist = abs(j["fila"] - portador["fila"]) + abs(j["columna"] - portador["columna"])
        distancias.append((j["nombre"], dist))
        print(f"  {j['nombre']:20s} → distancia Manhattan: {dist}")

    if not distancias:
        print("  (No hay otros jugadores en la cancha.)")
        return

    minima = min(d for _, d in distancias)
    mas_cercanos = [nombre for nombre, d in distancias if d == minima]

    if len(mas_cercanos) == 1:
        print(f"\nJugador más cercano: '{mas_cercanos[0]}' (distancia {minima}).")
    else:
        print(f"\nEmpate en distancia mínima ({minima}): {', '.join(mas_cercanos)}.")


# ════════════════════════════════════════════════════════════
#  TAREA 5 – Detectar posibilidad de pase
# ════════════════════════════════════════════════════════════
def _hay_bloqueo(cancha, fila1, col1, fila2, col2, equipo_rival):
    """
    Verifica si existe un rival o 'X' entre dos posiciones en línea recta.
    Retorna True si el camino está bloqueado.
    """
    if fila1 == fila2:
        c_min = min(col1, col2) + 1
        c_max = max(col1, col2)
        for c in range(c_min, c_max):
            celda = cancha[fila1][c]
            if celda == "X" or celda == equipo_rival:
                return True
    else:
        f_min = min(fila1, fila2) + 1
        f_max = max(fila1, fila2)
        for f in range(f_min, f_max):
            celda = cancha[f][col1]
            if celda == "X" or celda == equipo_rival:
                return True
    return False


def detectar_pases(cancha, jugadores):
    """
    Lista todos los pases posibles para el jugador que posee la pelota.
    """
    portador = None
    for j in jugadores:
        if j["tiene_pelota"]:
            portador = j
            break

    if portador is None:
        print("ERROR: Ningún jugador tiene la pelota.")
        return

    equipo_rival = "B" if portador["equipo"] == "A" else "A"
    pases_posibles = []

    print(f"\n── Pases posibles para '{portador['nombre']}' ──")

    for j in jugadores:
        if j is portador:
            continue
        if j["equipo"] != portador["equipo"]:
            continue

        misma_fila    = j["fila"]    == portador["fila"]
        misma_columna = j["columna"] == portador["columna"]

        if not (misma_fila or misma_columna):
            continue  # Pase diagonal o fuera de línea recta

        bloqueado = _hay_bloqueo(cancha,
                                  portador["fila"], portador["columna"],
                                  j["fila"],        j["columna"],
                                  equipo_rival)
        if bloqueado:
            print(f"  PASE BLOQUEADO: '{portador['nombre']}' → '{j['nombre']}' "
                  f"(rival u obstáculo en el camino).")
        else:
            pases_posibles.append(j["nombre"])
            print(f"  PASE POSIBLE:   '{portador['nombre']}' → '{j['nombre']}'.")

    if not pases_posibles:
        print("  No hay pases posibles disponibles.")

    return pases_posibles


# ════════════════════════════════════════════════════════════
#  TAREA 6 – Detectar camino libre al arco
# ════════════════════════════════════════════════════════════
def detectar_camino_libre(cancha, jugadores):
    """
    Analiza todos los delanteros y determina si tienen camino libre al arco rival.
    """
    print("\n── Detección de camino libre al arco ──")
    hay_delanteros = False

    for j in jugadores:
        if j["rol"] != "delantero":
            continue

        hay_delanteros = True
        equipo   = j["equipo"]
        fila     = j["fila"]
        columna  = j["columna"]
        rival    = "B" if equipo == "A" else "A"

        # Verificar mitad ofensiva
        if equipo == "A":
            en_mitad_ofensiva = (30 <= columna <= 59)
            col_arco_rival    = 59
        else:
            en_mitad_ofensiva = (0 <= columna <= 29)
            col_arco_rival    = 0

        if not en_mitad_ofensiva:
            print(f"  SIN CAMINO LIBRE: '{j['nombre']}' no está en la mitad ofensiva "
                  f"(columna {columna}).")
            continue

        # Verificar camino libre en la misma fila hacia el arco rival
        col_min = min(columna, col_arco_rival) + 1
        col_max = max(columna, col_arco_rival)
        camino_libre = True

        for c in range(col_min, col_max):
            celda = cancha[fila][c]
            if celda == "X" or celda == rival:
                camino_libre = False
                break

        if camino_libre:
            print(f"  CAMINO LIBRE:    '{j['nombre']}' tiene camino libre al arco "
                  f"(fila {fila}, columna {columna}).")
        else:
            print(f"  SIN CAMINO LIBRE: '{j['nombre']}' tiene el camino bloqueado "
                  f"(fila {fila}, columna {columna}).")

    if not hay_delanteros:
        print("  (No hay delanteros registrados en la cancha.)")


# ════════════════════════════════════════════════════════════
#  UTILIDADES
# ════════════════════════════════════════════════════════════
def mostrar_cancha(cancha, filas_mostrar=10, cols_mostrar=20):
    """Muestra una porción de la cancha para verificación visual."""
    print(f"\n── Vista parcial de la cancha (primeras {filas_mostrar} filas × {cols_mostrar} columnas) ──")
    print("   " + "".join(str(c % 10) for c in range(cols_mostrar)))
    for f in range(filas_mostrar):
        print(f"{f:2d} " + "".join(cancha[f][c] for c in range(cols_mostrar)))
    print()

def buscar_jugador(jugadores, nombre):
    """Retorna el diccionario del jugador con ese nombre, o None si no existe."""
    for j in jugadores:
        if j["nombre"] == nombre:
            return j
    return None


# ════════════════════════════════════════════════════════════
#  PROGRAMA PRINCIPAL – casos de prueba
# ════════════════════════════════════════════════════════════
def main():
    print("=" * 60)
    print("  Copa UADE 2026 – Desafío 3: La Cancha Inteligente")
    print("=" * 60)

    # ── Tarea 1: Crear cancha ────────────────────────────────
    cancha   = crear_cancha()
    jugadores = []
    print("\n[TAREA 1] Cancha 100×60 creada correctamente.")

    # Agregar un obstáculo para probar bloqueos
    cancha[10][15] = "X"
    print("  Obstáculo 'X' colocado en (10, 15).")

    # ── Tarea 2: Posicionar jugadores ────────────────────────
    print("\n[TAREA 2] Posicionando jugadores...")

    posicionar_jugador(cancha, jugadores, "Messi",    "A", 10, 10, "delantero",      True)
    posicionar_jugador(cancha, jugadores, "Di Maria",  "A", 10, 12, "mediocampista",  False)
    posicionar_jugador(cancha, jugadores, "Mac Allister", "A", 5, 10, "mediocampista", False)
    posicionar_jugador(cancha, jugadores, "Alvarez",  "A", 35, 45, "delantero",      False)
    posicionar_jugador(cancha, jugadores, "Romero",   "A", 20, 5,  "defensor",       False)

    posicionar_jugador(cancha, jugadores, "Vinicius", "B", 10, 20, "delantero",      False)
    posicionar_jugador(cancha, jugadores, "Rodrygo",  "B", 15, 12, "mediocampista",  False)
    posicionar_jugador(cancha, jugadores, "Endrick",  "B", 50, 10, "delantero",      False)

    # Casos de error
    print("\n  -- Casos de error esperados --")
    posicionar_jugador(cancha, jugadores, "Jugador X", "A", 10, 10, "delantero", False)   # celda ocupada
    posicionar_jugador(cancha, jugadores, "Jugador Y", "C", 5,  5,  "defensor",  False)   # equipo inválido
    posicionar_jugador(cancha, jugadores, "Jugador Z", "A", 200, 5, "defensor",  False)   # fuera de límites
    posicionar_jugador(cancha, jugadores, "Jugador W", "B", 30, 30, "centrocampista", False)  # rol inválido
    posicionar_jugador(cancha, jugadores, "Jugador V", "A", 7,  7,  "arquero",   True)    # doble pelota

    mostrar_cancha(cancha, filas_mostrar=16, cols_mostrar=25)

    # ── Tarea 3: Mover jugadores ────────────────────────────
    print("[TAREA 3] Movimientos de jugadores...")
    messi = buscar_jugador(jugadores, "Messi")

    mover_jugador(cancha, messi, "derecha")        # válido
    mover_jugador(cancha, messi, "derecha")        # válido → columna 12, Di Maria está ahí
    mover_jugador(cancha, messi, "abajo")          # válido
    mover_jugador(cancha, messi, "derecha")        # ahora columna 12... prueba superposición
    mover_jugador(cancha, messi, "derecha")        # hacia obstáculo en col 15 si fila cambia

    # Mover hacia el borde de la cancha
    arquero_test = {"nombre": "Test", "equipo": "A",
                    "fila": 0, "columna": 0, "rol": "arquero", "tiene_pelota": False}
    jugadores.append(arquero_test)
    cancha[0][0] = "A"
    mover_jugador(cancha, arquero_test, "arriba")     # fuera de cancha
    mover_jugador(cancha, arquero_test, "izquierda")  # fuera de cancha

    mostrar_cancha(cancha, filas_mostrar=16, cols_mostrar=25)

    # ── Tarea 4: Distancias Manhattan ───────────────────────
    print("[TAREA 4] Distancias Manhattan a la pelota...")
    calcular_distancias(jugadores)

    # ── Tarea 5: Detectar pases ─────────────────────────────
    print("\n[TAREA 5] Detectar pases posibles...")
    detectar_pases(cancha, jugadores)

    # ── Tarea 6: Camino libre al arco ───────────────────────
    # Posicionar delantero argentino en mitad ofensiva con camino libre
    posicionar_jugador(cancha, jugadores, "Lautaro", "A", 40, 40, "delantero", False)
    # Posicionar delantero brasileño en mitad ofensiva con rival bloqueando
    posicionar_jugador(cancha, jugadores, "Paqueta", "B",  8,  18, "delantero", False)
    # Delantero argentino fuera de mitad ofensiva
    posicionar_jugador(cancha, jugadores, "Dybala",  "A", 60, 20, "delantero", False)

    print("\n[TAREA 6] Detectar camino libre al arco...")
    detectar_camino_libre(cancha, jugadores)

    print("\n" + "=" * 60)
    print("  Fin del programa.")
    print("=" * 60)


if __name__ == "__main__":
    main()