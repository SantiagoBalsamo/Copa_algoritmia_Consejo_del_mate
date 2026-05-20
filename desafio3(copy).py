# --- Copa algoritmia 2026 --- Desafio 3 ---

# Constantes 
FILAS           = 100
COLUMNAS        = 60
EQUIPOS_VALIDOS = ("A", "B")
ROLES_VALIDOS   = ("arquero", "defensor", "mediocampista", "delantero")

def crear_cancha():
    """Retorna una matriz 100×60 inicializada con '.'."""
    cancha = []
    for _ in range(FILAS):
        fila = []
        for _ in range(COLUMNAS):
            fila.append(".")
        cancha.append(fila)
    return cancha


def posicionar_jugador(cancha, jugadores, nombre, equipo, fila, columna, rol, tiene_pelota):
    """
    Agrega un jugador a la cancha y a la lista de jugadores.
    Retorna True si el registro fue exitoso, False en caso contrario.
    """
    if equipo not in EQUIPOS_VALIDOS:
        print(f"  ERROR: Equipo '{equipo}' no válido. Use 'A' o 'B'.")
        return False

    if rol not in ROLES_VALIDOS:
        print(f"  ERROR: Rol '{rol}' no válido. Use: {', '.join(ROLES_VALIDOS)}.")
        return False

    if not (0 <= fila < FILAS and 0 <= columna < COLUMNAS):
        print(f"  ERROR: Posición ({fila}, {columna}) fuera de los límites de la cancha.")
        return False

    if cancha[fila][columna] != ".":
        print(f"  ERROR: La celda ({fila}, {columna}) ya está ocupada.")
        return False

    if tiene_pelota:
        for j in jugadores:
            if j["tiene_pelota"]:
                print(f"  ERROR: '{j['nombre']}' ya posee la pelota. Solo un jugador puede tenerla.")
                return False

    jugador = {
        "nombre":       nombre,
        "equipo":       equipo,
        "fila":         fila,
        "columna":      columna,
        "rol":          rol,
        "tiene_pelota": tiene_pelota
    }
    jugadores.append(jugador)
    cancha[fila][columna] = equipo

    print(f"  OK: Jugador '{nombre}' ({equipo} - {rol}) agregado en ({fila}, {columna}).", end="")
    if tiene_pelota:
        print(" [tiene la pelota]", end="")
    print()
    return True


def mover_jugador(cancha, jugador, direccion):
    """
    Mueve al jugador una celda en la dirección indicada.
    Retorna True si el movimiento fue exitoso, False si fue inválido.
    """
    deltas = {
        "arriba":    (-1,  0),
        "abajo":     ( 1,  0),
        "izquierda": ( 0, -1),
        "derecha":   ( 0,  1),
    }

    if direccion not in deltas:
        print(f"  ERROR: Dirección '{direccion}' no reconocida.")
        return False

    df, dc        = deltas[direccion]
    nueva_fila    = jugador["fila"]    + df
    nueva_columna = jugador["columna"] + dc

    if not (0 <= nueva_fila < FILAS and 0 <= nueva_columna < COLUMNAS):
        print(f"  MOVIMIENTO INVÁLIDO: '{jugador['nombre']}' no puede moverse hacia {direccion} "
              f"(fuera de la cancha).")
        return False

    celda_destino = cancha[nueva_fila][nueva_columna]

    if celda_destino == "X":
        print(f"  MOVIMIENTO INVÁLIDO: '{jugador['nombre']}' no puede moverse hacia {direccion} "
              f"(zona bloqueada).")
        return False

    if celda_destino in ("A", "B"):
        print(f"  MOVIMIENTO INVÁLIDO: '{jugador['nombre']}' no puede moverse hacia {direccion} "
              f"(celda ocupada por otro jugador).")
        return False

    cancha[jugador["fila"]][jugador["columna"]] = "."
    cancha[nueva_fila][nueva_columna] = jugador["equipo"]
    jugador["fila"]    = nueva_fila
    jugador["columna"] = nueva_columna

    print(f"  MOVIMIENTO OK: '{jugador['nombre']}' se movió {direccion} → ({nueva_fila}, {nueva_columna}).")
    return True


def buscar_portador(jugadores):
    """Retorna el jugador que tiene la pelota, o None si ninguno la tiene."""
    for j in jugadores:
        if j["tiene_pelota"]:
            return j
    return None


def rival_de(equipo):
    """Retorna el equipo rival dado un equipo."""
    return "B" if equipo == "A" else "A"


def calcular_distancias(jugadores):
    """
    Calcula la distancia Manhattan de cada jugador respecto al que tiene la pelota.
    Muestra las distancias e indica el/los jugador/es más cercanos.
    """
    portador = buscar_portador(jugadores)

    if portador is None:
        print("  ERROR: Ningún jugador tiene la pelota.")
        return

    print(f"\n  ── Distancias a la pelota (portador: '{portador['nombre']}') ──")
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

    minima       = min(d for _, d in distancias)
    mas_cercanos = [nombre for nombre, d in distancias if d == minima]

    if len(mas_cercanos) == 1:
        print(f"\n  Jugador más cercano: '{mas_cercanos[0]}' (distancia {minima}).")
    else:
        print(f"\n  Empate en distancia mínima ({minima}): {', '.join(mas_cercanos)}.")


def hay_bloqueo(cancha, fila1, col1, fila2, col2, equipo_rival):
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
    portador = buscar_portador(jugadores)

    if portador is None:
        print("  ERROR: Ningún jugador tiene la pelota.")
        return

    equipo_rival   = rival_de(portador["equipo"])
    pases_posibles = []

    print(f"\n  ── Pases posibles para '{portador['nombre']}' ──")

    for j in jugadores:
        if j is portador:
            continue
        if j["equipo"] != portador["equipo"]:
            continue

        misma_fila    = j["fila"]    == portador["fila"]
        misma_columna = j["columna"] == portador["columna"]

        if not (misma_fila or misma_columna):
            continue

        bloqueado = hay_bloqueo(cancha,
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


def detectar_camino_libre(cancha, jugadores):
    """
    Analiza todos los delanteros y determina si tienen camino libre al arco rival.
    """
    print("\n  ── Detección de camino libre al arco ──")
    hay_delanteros = False

    for j in jugadores:
        if j["rol"] != "delantero":
            continue

        hay_delanteros = True
        equipo  = j["equipo"]
        fila    = j["fila"]
        columna = j["columna"]
        rival   = rival_de(equipo)

        config_equipo = {
            "A": {"mitad": (30, 59), "arco": 59},
            "B": {"mitad": (0,  29), "arco": 0},
        }
        col_inicio, col_fin = config_equipo[equipo]["mitad"]
        col_arco_rival      = config_equipo[equipo]["arco"]
        en_mitad_ofensiva   = (col_inicio <= columna <= col_fin)

        if not en_mitad_ofensiva:
            print(f"  SIN CAMINO LIBRE: '{j['nombre']}' no está en la mitad ofensiva "
                  f"(columna {columna}).")
            continue

        col_min      = min(columna, col_arco_rival) + 1
        col_max      = max(columna, col_arco_rival)
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


def mostrar_cancha(cancha):
    """Muestra una porción de la cancha (primeras 15 filas × 30 columnas)."""
    filas_mostrar = 15
    cols_mostrar  = 30
    print(f"\n  ── Vista parcial de la cancha "
          f"(primeras {filas_mostrar} filas × {cols_mostrar} columnas) ──")
    print("     " + "".join(str(c % 10) for c in range(cols_mostrar)))
    for f in range(filas_mostrar):
        print(f"  {f:2d} " + "".join(cancha[f][c] for c in range(cols_mostrar)))
    print()


def buscar_jugador(jugadores, nombre):
    """Retorna el diccionario del jugador con ese nombre, o None si no existe."""
    for j in jugadores:
        if j["nombre"] == nombre:
            return j
    return None


def pedir_entero(mensaje, minimo, maximo):
    """Solicita un entero al usuario dentro de un rango válido."""
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"  Por favor ingrese un número entre {minimo} y {maximo}.")
        except ValueError:
            print("  Por favor ingrese un número entero válido.")


def menu_agregar_jugador(cancha, jugadores):
    print("\n  ── Agregar jugador ──")
    nombre  = input("  Nombre: ").strip()
    if not nombre:
        print("  ERROR: El nombre no puede estar vacío.")
        return

    equipo  = input("  Equipo (A/B): ").strip().upper()
    fila    = pedir_entero("  Fila (0-99): ", 0, 99)
    columna = pedir_entero("  Columna (0-59): ", 0, 59)

    print("  Roles disponibles: arquero, defensor, mediocampista, delantero")
    rol     = input("  Rol: ").strip().lower()

    respuesta      = input("  ¿Tiene la pelota? (s/n): ").strip().lower()
    tiene_pelota   = respuesta == "s"

    posicionar_jugador(cancha, jugadores, nombre, equipo, fila, columna, rol, tiene_pelota)


def menu_mover_jugador(cancha, jugadores):
    print("\n  ── Mover jugador ──")
    if not jugadores:
        print("  ERROR: No hay jugadores en la cancha.")
        return

    nombre = input("  Nombre del jugador a mover: ").strip()
    jugador = buscar_jugador(jugadores, nombre)

    if jugador is None:
        print(f"  ERROR: No se encontró al jugador '{nombre}'.")
        return

    print("  Direcciones válidas: arriba, abajo, izquierda, derecha")
    direccion = input("  Dirección: ").strip().lower()
    mover_jugador(cancha, jugador, direccion)


def menu_agregar_obstaculo(cancha):
    print("\n  ── Agregar obstáculo ──")
    fila    = pedir_entero("  Fila (0-99): ", 0, 99)
    columna = pedir_entero("  Columna (0-59): ", 0, 59)

    if cancha[fila][columna] != ".":
        print(f"  ERROR: La celda ({fila}, {columna}) ya está ocupada.")
    else:
        cancha[fila][columna] = "X"
        print(f"  OK: Obstáculo colocado en ({fila}, {columna}).")


def mostrar_menu():
    print("\n" + "=" * 50)
    print("  MENÚ PRINCIPAL")
    print("=" * 50)
    print("  1. Agregar jugador")
    print("  2. Mover jugador")
    print("  3. Ver distancias a la pelota")
    print("  4. Detectar pases posibles")
    print("  5. Detectar camino libre al arco")
    print("  6. Ver cancha")
    print("  7. Agregar obstáculo")
    print("  0. Salir")
    print("=" * 50)


def main():
    print("=" * 50)
    print("  Copa UADE 2026 – Desafío 3")
    print("  La Cancha Inteligente")
    print("=" * 50)

    cancha    = crear_cancha()
    jugadores = []
    print("\n  Cancha 100×60 creada correctamente.")

    opciones = {
        "1": lambda: menu_agregar_jugador(cancha, jugadores),
        "2": lambda: menu_mover_jugador(cancha, jugadores),
        "3": lambda: calcular_distancias(jugadores),
        "4": lambda: detectar_pases(cancha, jugadores),
        "5": lambda: detectar_camino_libre(cancha, jugadores),
        "6": lambda: mostrar_cancha(cancha),
        "7": lambda: menu_agregar_obstaculo(cancha),
    }

    while True:
        mostrar_menu()
        opcion = input("  Ingrese una opción: ").strip()

        if opcion == "0":
            print("\n  Fin del programa.")
            break
        elif opcion in opciones:
            opciones[opcion]()
        else:
            print("  Opción no válida. Ingrese un número del 0 al 7.")


if __name__ == "__main__":
    main()