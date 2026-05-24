# =============================================================================
# DESAFÍO 3: "LA CANCHA INTELIGENTE"
# Copa de Algoritmia y Programación - UADE 2026
# =============================================================================

import random

FILAS           = 40
COLUMNAS        = 60
EQUIPOS_VALIDOS = ("A", "B")
ROLES_VALIDOS   = ("arquero", "defensor", "mediocampista", "delantero")
RIVAL           = {"A": "B", "B": "A"}
BLOQUEANTES     = {"X", "A_rival", "B_rival"}  # se arma dinámico por función
SIM_ARBITRO     = "R"
SIM_SOMBRA      = "S"


# =============================================================================
# TAREA 1: CREAR LA CANCHA
# =============================================================================

def crear_cancha():
    """Genera la matriz que representa la cancha de fútbol.

    Crea una matriz de 40 filas por 60 columnas inicializada con puntos,
    donde cada punto representa una posición vacía.

    Returns:
        Matriz de 40x60 inicializada con '.'.
    """
    return [["." for _ in range(COLUMNAS)] for _ in range(FILAS)]


# =============================================================================
# TAREA 2: POSICIONAR JUGADORES
# =============================================================================

def posicionar_jugador(cancha, jugadores, jugador):
    """Agrega un jugador a la cancha validando todas las condiciones requeridas.

    Valida nombre duplicado, límites, celda libre, tipo de tiene_pelota,
    equipo, rol y posesión única de la pelota.

    Args:
        cancha: La matriz que representa la cancha.
        jugadores: Lista con todos los jugadores registrados.
        jugador: Diccionario con nombre, equipo, fila, columna, rol y tiene_pelota.

    Returns:
        True si el jugador fue agregado correctamente, False en caso contrario.
    """
    nombre       = jugador["nombre"]
    equipo       = jugador["equipo"]
    fila         = jugador["fila"]
    columna      = jugador["columna"]
    rol          = jugador["rol"]
    tiene_pelota = jugador["tiene_pelota"]

    if any(j["nombre"] == nombre for j in jugadores):
        print(f"[ERROR] No se pudo agregar a {nombre}: ya existe un jugador con ese nombre.")
        return False

    if fila < 0 or fila >= FILAS or columna < 0 or columna >= COLUMNAS:
        print(f"[ERROR] No se pudo agregar a {nombre}: posición ({fila}, {columna}) "
              f"fuera de los límites de la cancha.")
        return False

    celda = cancha[fila][columna]
    if celda == "X":
        print(f"[ERROR] No se pudo agregar a {nombre}: la celda ({fila}, {columna}) "
              f"contiene un obstáculo (X).")
        return False
    if celda in (SIM_ARBITRO, SIM_SOMBRA):
        print(f"[ERROR] No se pudo agregar a {nombre}: la celda ({fila}, {columna}) "
              f"está cubierta por el árbitro o su sombra.")
        return False
    if celda in ("A", "B"):
        print(f"[ERROR] No se pudo agregar a {nombre}: la celda ({fila}, {columna}) "
              f"ya está ocupada por otro jugador.")
        return False

    if not isinstance(tiene_pelota, bool):
        print(f"[ERROR] No se pudo agregar a {nombre}: 'tiene_pelota' debe ser "
              f"True o False (se recibió {type(tiene_pelota).__name__}: {tiene_pelota!r}).")
        return False

    if equipo not in EQUIPOS_VALIDOS:
        print(f"[ERROR] No se pudo agregar a {nombre}: equipo '{equipo}' no válido. "
              f"Use {EQUIPOS_VALIDOS}.")
        return False

    if rol not in ROLES_VALIDOS:
        print(f"[ERROR] No se pudo agregar a {nombre}: rol '{rol}' no válido. "
              f"Use {ROLES_VALIDOS}.")
        return False

    if tiene_pelota:
        for j in jugadores:
            if j["tiene_pelota"]:
                print(f"[ERROR] No se pudo agregar a {nombre} con la pelota: "
                      f"{j['nombre']} ya la posee.")
                return False

    jugadores.append(jugador)
    cancha[fila][columna] = equipo
    print(f"[OK] Jugador {nombre} ({equipo} - {rol}) agregado en ({fila}, {columna})"
          f"{'  [TIENE LA PELOTA]' if tiene_pelota else ''}.")
    return True


# =============================================================================
# TAREA 3: MOVER JUGADORES
# =============================================================================

def mover_jugador(cancha, jugadores, nombre, direccion):
    """Mueve un jugador una celda en la dirección indicada.

    Valida límites, zona bloqueada, celda ocupada y árbitro/sombra.
    Actualiza la posición del jugador y la matriz.

    Args:
        cancha: La matriz que representa la cancha.
        jugadores: Lista con todos los jugadores registrados.
        nombre: Nombre del jugador a mover.
        direccion: 'arriba', 'abajo', 'izquierda' o 'derecha'.

    Returns:
        True si el movimiento fue exitoso, False si fue inválido.
    """
    jugador = buscar_jugador(jugadores, nombre)
    if jugador is None:
        print(f"[ERROR] No se encontró al jugador '{nombre}'.")
        return False

    deltas = {
        "arriba":    (-1,  0),
        "abajo":     ( 1,  0),
        "izquierda": ( 0, -1),
        "derecha":   ( 0,  1),
    }

    if direccion not in deltas:
        print(f"[ERROR] Dirección '{direccion}' no válida. "
              f"Use: arriba, abajo, izquierda, derecha.")
        return False

    df, dc        = deltas[direccion]
    nueva_fila    = jugador["fila"]    + df
    nueva_columna = jugador["columna"] + dc

    if nueva_fila < 0 or nueva_fila >= FILAS or nueva_columna < 0 or nueva_columna >= COLUMNAS:
        print(f"[MOVIMIENTO INVÁLIDO] {nombre} no puede moverse hacia {direccion}: "
              f"fuera de la cancha.")
        return False

    celda_destino  = cancha[nueva_fila][nueva_columna]
    mensajes_error = {
        "X":        "zona bloqueada (X)",
        "A":        "celda ocupada por otro jugador",
        "B":        "celda ocupada por otro jugador",
        SIM_ARBITRO: "celda ocupada por el árbitro",
        SIM_SOMBRA:  "celda cubierta por la sombra del árbitro",
    }

    if celda_destino in mensajes_error:
        print(f"[MOVIMIENTO INVÁLIDO] {nombre} no puede moverse hacia {direccion}: "
              f"{mensajes_error[celda_destino]} en ({nueva_fila}, {nueva_columna}).")
        return False

    fila_anterior    = jugador["fila"]
    columna_anterior = jugador["columna"]

    cancha[fila_anterior][columna_anterior] = "."
    cancha[nueva_fila][nueva_columna]       = jugador["equipo"]
    jugador["fila"]                         = nueva_fila
    jugador["columna"]                      = nueva_columna

    print(f"[MOVIMIENTO OK] {nombre}: ({fila_anterior}, {columna_anterior}) "
          f"→ ({nueva_fila}, {nueva_columna}).")
    return True


# =============================================================================
# TAREA 4: CALCULAR DISTANCIA A LA PELOTA
# =============================================================================

def calcular_distancias(jugadores):
    """Calcula la distancia Manhattan de cada jugador respecto a quien tiene la pelota.

    Muestra la distancia de cada jugador e indica cuál o cuáles son los más
    cercanos. En caso de empate, muestra todos los empatados.

    Args:
        jugadores: Lista con todos los jugadores registrados.

    Returns:
        Lista de jugadores más cercanos a la pelota.
    """
    portador = buscar_portador(jugadores)
    if portador is None:
        print("[ERROR] Ningún jugador tiene la pelota.")
        return []

    print(f"\n--- Distancias Manhattan respecto a {portador['nombre']} "
          f"(pelota en ({portador['fila']}, {portador['columna']})) ---")

    distancias = []
    for j in jugadores:
        if j is portador:
            continue
        dist = (abs(j["fila"] - portador["fila"]) +
                abs(j["columna"] - portador["columna"]))
        distancias.append((j, dist))
        print(f"  {j['nombre']} ({j['equipo']}): distancia = {dist}")

    if not distancias:
        print("  No hay otros jugadores en la cancha.")
        return []

    minima       = min(d for _, d in distancias)
    mas_cercanos = [j for j, d in distancias if d == minima]

    if len(mas_cercanos) == 1:
        print(f"  >> Jugador más cercano: {mas_cercanos[0]['nombre']} "
              f"(distancia {minima})")
    else:
        nombres = ", ".join(j["nombre"] for j in mas_cercanos)
        print(f"  >> Empate en distancia {minima}: {nombres}")

    return mas_cercanos


# =============================================================================
# TAREA 5: DETECTAR POSIBILIDAD DE PASE
# =============================================================================

def hay_bloqueo_entre(cancha, portador, receptor, equipo_rival):
    """Verifica si existe un rival, árbitro, sombra u obstáculo entre portador y receptor.

    Solo analiza en línea recta. Los jugadores del mismo equipo no bloquean.

    Args:
        cancha: La matriz que representa la cancha.
        portador: Jugador que tiene la pelota.
        receptor: Jugador al que se intenta pasar.
        equipo_rival: Símbolo del equipo rival.

    Returns:
        True si hay bloqueo, False si el camino está libre.
    """
    bloqueantes = {"X", equipo_rival, SIM_ARBITRO, SIM_SOMBRA}

    fila_p, col_p = portador["fila"], portador["columna"]
    fila_r, col_r = receptor["fila"], receptor["columna"]

    if fila_p == fila_r:
        for col in range(min(col_p, col_r) + 1, max(col_p, col_r)):
            if cancha[fila_p][col] in bloqueantes:
                return True
    else:
        for fila in range(min(fila_p, fila_r) + 1, max(fila_p, fila_r)):
            if cancha[fila][col_p] in bloqueantes:
                return True

    return False


def detectar_pases(cancha, jugadores):
    """Lista todos los pases posibles para el jugador que posee la pelota.

    Un pase es válido si el receptor es del mismo equipo, está en la misma
    fila o columna, y no hay rivales, árbitro, sombra ni obstáculos entre ellos.

    Args:
        cancha: La matriz que representa la cancha.
        jugadores: Lista con todos los jugadores registrados.

    Returns:
        Lista de jugadores a los que se puede realizar el pase.
    """
    portador = buscar_portador(jugadores)
    if portador is None:
        print("[ERROR] Ningún jugador tiene la pelota.")
        return []

    equipo_rival   = RIVAL[portador["equipo"]]
    pases_posibles = []

    print(f"\n--- Pases posibles para {portador['nombre']} "
          f"en ({portador['fila']}, {portador['columna']}) ---")

    for j in jugadores:
        if j is portador or j["equipo"] != portador["equipo"]:
            continue

        misma_fila = j["fila"]    == portador["fila"]
        misma_col  = j["columna"] == portador["columna"]

        if not (misma_fila or misma_col):
            continue

        if hay_bloqueo_entre(cancha, portador, j, equipo_rival):
            print(f"  [PASE BLOQUEADO] → {j['nombre']}: rival, árbitro u obstáculo "
                  f"en el camino.")
        else:
            pases_posibles.append(j)
            print(f"  [PASE POSIBLE]   → {j['nombre']} "
                  f"en ({j['fila']}, {j['columna']}).")

    if not pases_posibles:
        print("  No hay pases disponibles.")

    return pases_posibles


# =============================================================================
# TAREA 6: DETECTAR CAMINO LIBRE AL ARCO
# =============================================================================

def detectar_camino_libre(cancha, jugadores):
    """Detecta qué delanteros tienen camino libre al arco rival.

    Un delantero tiene camino libre si está en la mitad ofensiva y no hay
    rivales, árbitro, sombra ni obstáculos en su misma fila entre él y el arco.
    Los compañeros de equipo no bloquean el camino.

    Args:
        cancha: La matriz que representa la cancha.
        jugadores: Lista con todos los jugadores registrados.

    Returns:
        Lista de delanteros con camino libre al arco.
    """
    print("\n--- Detección de camino libre al arco ---")

    delanteros_libres = []
    hay_delanteros    = False

    for j in jugadores:
        if j["rol"] != "delantero":
            continue

        hay_delanteros = True
        equipo         = j["equipo"]
        fila           = j["fila"]
        columna        = j["columna"]
        bloqueantes    = {"X", RIVAL[equipo], SIM_ARBITRO, SIM_SOMBRA}

        en_mitad_ofensiva = (
            (equipo == "A" and 30 <= columna <= 59) or
            (equipo == "B" and  0 <= columna <= 29)
        )

        if not en_mitad_ofensiva:
            print(f"  [SIN CAMINO LIBRE] {j['nombre']}: no está en la mitad ofensiva "
                  f"(columna {columna}).")
            continue

        rango_cols = range(columna + 1, COLUMNAS) if equipo == "A" else range(columna - 1, -1, -1)

        camino_libre = True
        for col in rango_cols:
            if cancha[fila][col] in bloqueantes:
                camino_libre = False
                break

        if camino_libre:
            delanteros_libres.append(j)
            print(f"  [CAMINO LIBRE]    {j['nombre']}: camino libre al arco rival "
                  f"desde ({fila}, {columna}).")
        else:
            print(f"  [SIN CAMINO LIBRE] {j['nombre']}: hay rival, árbitro u "
                  f"obstáculo en su fila.")

    if not hay_delanteros:
        print("  No hay delanteros registrados en la cancha.")

    return delanteros_libres


# =============================================================================
# ÁRBITRO
# =============================================================================

def crear_arbitro(fila, columna):
    """Crea el diccionario que representa al árbitro.

    Args:
        fila: Fila inicial del árbitro.
        columna: Columna inicial del árbitro.

    Returns:
        Diccionario con la posición del árbitro.
    """
    return {"fila": fila, "columna": columna}


def celdas_sombra(fila, columna):
    """Calcula las celdas adyacentes que forman la sombra del árbitro.

    Args:
        fila: Fila actual del árbitro.
        columna: Columna actual del árbitro.

    Returns:
        Lista de tuplas (fila, columna) de celdas con sombra dentro de la cancha.
    """
    candidatas = [
        (fila - 1, columna),
        (fila + 1, columna),
        (fila, columna - 1),
        (fila, columna + 1),
    ]
    return [(f, c) for f, c in candidatas if 0 <= f < FILAS and 0 <= c < COLUMNAS]


def colocar_arbitro(cancha, arbitro):
    """Coloca al árbitro y su sombra en la cancha.

    Args:
        cancha: La matriz que representa la cancha.
        arbitro: Diccionario con la posición del árbitro.

    Returns:
        None
    """
    fila, columna = arbitro["fila"], arbitro["columna"]
    cancha[fila][columna] = SIM_ARBITRO
    for f, c in celdas_sombra(fila, columna):
        if cancha[f][c] == ".":
            cancha[f][c] = SIM_SOMBRA


def quitar_arbitro(cancha, arbitro):
    """Elimina al árbitro y su sombra de la cancha.

    Args:
        cancha: La matriz que representa la cancha.
        arbitro: Diccionario con la posición actual del árbitro.

    Returns:
        None
    """
    fila, columna = arbitro["fila"], arbitro["columna"]
    cancha[fila][columna] = "."
    for f, c in celdas_sombra(fila, columna):
        if cancha[f][c] == SIM_SOMBRA:
            cancha[f][c] = "."


def mover_arbitro(cancha, arbitro, jugadores):
    """Mueve al árbitro aleatoriamente cerca del jugador con la pelota.

    Intenta moverse hacia el portador. Si la celda está ocupada, prueba
    otra dirección aleatoria. Si no puede moverse, permanece en su lugar.

    Args:
        cancha: La matriz que representa la cancha.
        arbitro: Diccionario con la posición actual del árbitro.
        jugadores: Lista con todos los jugadores registrados.

    Returns:
        None
    """
    portador   = buscar_portador(jugadores)
    fila_a     = arbitro["fila"]
    col_a      = arbitro["columna"]

    if portador:
        fila_p = portador["fila"]
        col_p  = portador["columna"]
        df     = 0 if fila_p == fila_a else (1 if fila_p > fila_a else -1)
        dc     = 0 if col_p  == col_a  else (1 if col_p  > col_a  else -1)

        if abs(fila_p - fila_a) >= abs(col_p - col_a):
            direcciones = [(df, 0), (0, dc), (-df, 0), (0, -dc)]
        else:
            direcciones = [(0, dc), (df, 0), (0, -dc), (-df, 0)]

        random.shuffle(direcciones[1:])
    else:
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(direcciones)

    quitar_arbitro(cancha, arbitro)

    for df, dc in direcciones:
        nf = fila_a + df
        nc = col_a  + dc
        if 0 <= nf < FILAS and 0 <= nc < COLUMNAS:
            if cancha[nf][nc] not in ("A", "B", "X"):
                arbitro["fila"]    = nf
                arbitro["columna"] = nc
                break

    colocar_arbitro(cancha, arbitro)
    print(f"[ÁRBITRO] Se movió a ({arbitro['fila']}, {arbitro['columna']}).")


# =============================================================================
# UTILIDADES
# =============================================================================

def agregar_obstaculo(cancha, fila, columna):
    """Coloca un obstáculo fijo en una posición de la cancha.

    Args:
        cancha: La matriz que representa la cancha.
        fila: Fila donde se coloca el obstáculo.
        columna: Columna donde se coloca el obstáculo.

    Returns:
        True si se colocó correctamente, False si la posición es inválida o está ocupada.
    """
    if fila < 0 or fila >= FILAS or columna < 0 or columna >= COLUMNAS:
        print(f"[ERROR] Posición ({fila}, {columna}) fuera de los límites.")
        return False
    if cancha[fila][columna] != ".":
        print(f"[ERROR] La celda ({fila}, {columna}) ya está ocupada: "
              f"'{cancha[fila][columna]}'.")
        return False
    cancha[fila][columna] = "X"
    print(f"[OK] Obstáculo colocado en ({fila}, {columna}).")
    return True


def buscar_jugador(jugadores, nombre):
    """Busca un jugador en la lista por su nombre.

    Args:
        jugadores: Lista con todos los jugadores registrados.
        nombre: Nombre del jugador a buscar.

    Returns:
        Diccionario del jugador si se encuentra, None si no existe.
    """
    for j in jugadores:
        if j["nombre"] == nombre:
            return j
    return None


def buscar_portador(jugadores):
    """Busca el jugador que actualmente posee la pelota.

    Args:
        jugadores: Lista con todos los jugadores registrados.

    Returns:
        Diccionario del jugador con la pelota, None si ninguno la tiene.
    """
    for j in jugadores:
        if j["tiene_pelota"]:
            return j
    return None


def mostrar_seccion_cancha(cancha, fila_inicio, fila_fin, col_inicio, col_fin):
    """Muestra una sección de la cancha por consola.

    Args:
        cancha: La matriz que representa la cancha.
        fila_inicio: Fila inicial del recorte (inclusiva).
        fila_fin: Fila final del recorte (inclusiva).
        col_inicio: Columna inicial del recorte (inclusiva).
        col_fin: Columna final del recorte (inclusiva).

    Returns:
        None
    """
    print(f"\n--- Vista de la cancha (filas {fila_inicio}-{fila_fin}, "
          f"cols {col_inicio}-{col_fin}) ---")
    for f in range(fila_inicio, fila_fin + 1):
        fila_str = " ".join(cancha[f][col_inicio:col_fin + 1])
        print(f"  F{f:02d}: {fila_str}")


def mostrar_jugadores(jugadores):
    """Imprime la posición y estado de todos los jugadores.

    Args:
        jugadores: Lista con todos los jugadores registrados.

    Returns:
        None
    """
    print("\n--- Jugadores en cancha ---")
    for j in jugadores:
        pelota = " [PELOTA]" if j["tiene_pelota"] else ""
        print(f"  {j['nombre']:15s} | {j['equipo']} | {j['rol']:15s} | "
              f"fila {j['fila']:2d}, col {j['columna']:2d}{pelota}")


# =============================================================================
# MENÚ INTERACTIVO
# =============================================================================

def mostrar_menu():
    """Imprime el menú principal de opciones del programa.

    Returns:
        None
    """
    print("\033[2J\033[H", end="")
    print("=" * 55)
    print("        MENÚ — LA CANCHA INTELIGENTE")
    print("=" * 55)
    print("  1. Mostrar cancha (zona central)")
    print("  2. Mover jugador")
    print("  3. Ver distancias a la pelota")
    print("  4. Ver pases posibles")
    print("  5. Ver camino libre al arco")
    print("  6. Mover árbitro")
    print("  7. Ver posiciones de todos los jugadores")
    print("  0. Salir")
    print("=" * 55)


def menu_mover_jugador(cancha, jugadores):
    """Solicita el nombre del jugador y la dirección, valida y ejecuta el movimiento.

    Args:
        cancha: La matriz que representa la cancha.
        jugadores: Lista con todos los jugadores registrados.

    Returns:
        None
    """
    nombre = input("  Nombre del jugador: ").strip()
    if not nombre:
        print("  [ERROR] El nombre no puede estar vacío.")
        return

    direcciones_validas = ("arriba", "abajo", "izquierda", "derecha")
    print(f"  Dirección: {' / '.join(direcciones_validas)}")
    direccion = input("  Dirección: ").strip().lower()

    if not direccion:
        print("  [ERROR] La dirección no puede estar vacía.")
        return

    mover_jugador(cancha, jugadores, nombre, direccion)


def ejecutar_menu(cancha, jugadores, arbitro):
    """Ejecuta el bucle principal del menú interactivo.

    Args:
        cancha: La matriz que representa la cancha.
        jugadores: Lista con todos los jugadores registrados.
        arbitro: Diccionario con la posición actual del árbitro.

    Returns:
        None
    """
    opciones = {
        "1": lambda: mostrar_seccion_cancha(cancha, 0, FILAS - 1, 0, COLUMNAS - 1),
        "2": lambda: menu_mover_jugador(cancha, jugadores),
        "3": lambda: calcular_distancias(jugadores),
        "4": lambda: detectar_pases(cancha, jugadores),
        "5": lambda: detectar_camino_libre(cancha, jugadores),
        "6": lambda: mover_arbitro(cancha, arbitro, jugadores),
        "7": lambda: mostrar_jugadores(jugadores),
    }

    while True:
        mostrar_menu()
        opcion = input("  Elegí una opción: ").strip()

        if opcion == "0":
            print("\n  ¡Hasta la próxima!\n")
            break
        elif opcion in opciones:
            opciones[opcion]()
        else:
            print("  [ERROR] Opción no válida. Ingresá un número del 0 al 7.")


# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================

def main():
    """Punto de entrada del programa.

    Carga la cancha, los jugadores y el árbitro, ejecuta los casos de prueba
    mínimos requeridos por la consigna y lanza el menú interactivo.

    Returns:
        None
    """
    print("=" * 55)
    print("   DESAFÍO 3: LA CANCHA INTELIGENTE — UADE 2026")
    print("=" * 55)

    cancha    = crear_cancha()
    jugadores = []

    # ── Carga inicial de jugadores ────────────────────────────
    print("\n" + "=" * 55)
    print("CARGANDO JUGADORES INICIALES")
    print("=" * 55)

    jugadores_iniciales = [
        {"nombre": "Messi",    "equipo": "A", "fila": 20, "columna": 40,
         "rol": "delantero",     "tiene_pelota": True},
        {"nombre": "Di Maria", "equipo": "A", "fila": 20, "columna": 45,
         "rol": "delantero",     "tiene_pelota": False},
        {"nombre": "De Paul",  "equipo": "A", "fila": 25, "columna": 40,
         "rol": "mediocampista", "tiene_pelota": False},
        {"nombre": "Romero",   "equipo": "A", "fila": 30, "columna": 10,
         "rol": "defensor",      "tiene_pelota": False},
        {"nombre": "Alvarez",  "equipo": "A", "fila":  5, "columna": 35,
         "rol": "delantero",     "tiene_pelota": False},
        {"nombre": "Dybala",   "equipo": "A", "fila":  5, "columna": 20,
         "rol": "delantero",     "tiene_pelota": False},
        {"nombre": "Vinicius", "equipo": "B", "fila": 20, "columna": 43,
         "rol": "delantero",     "tiene_pelota": False},
        {"nombre": "Rodrygo",  "equipo": "B", "fila": 28, "columna": 15,
         "rol": "delantero",     "tiene_pelota": False},
        {"nombre": "Casemiro", "equipo": "B", "fila": 25, "columna": 30,
         "rol": "mediocampista", "tiene_pelota": False},
    ]

    for j in jugadores_iniciales:
        posicionar_jugador(cancha, jugadores, j)

    # ── Casos borde – Tarea 2 ────────────────────────────────
    print("\n" + "=" * 55)
    print("CASOS BORDE — POSICIONAR JUGADORES")
    print("=" * 55)

    print("\n-- Nombre duplicado --")
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Messi", "equipo": "A", "fila": 5, "columna": 5,
        "rol": "delantero", "tiene_pelota": False
    })

    print("\n-- Posición fuera de la cancha --")
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Fantasma", "equipo": "A", "fila": 99, "columna": 5,
        "rol": "defensor", "tiene_pelota": False
    })

    print("\n-- Celda con obstáculo (X) --")
    agregar_obstaculo(cancha, 5, 5)
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Lautaro", "equipo": "A", "fila": 5, "columna": 5,
        "rol": "delantero", "tiene_pelota": False
    })

    print("\n-- Celda ocupada por jugador --")
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Suplente", "equipo": "A", "fila": 20, "columna": 40,
        "rol": "delantero", "tiene_pelota": False
    })

    print("\n-- tiene_pelota con tipo inválido --")
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Lautaro", "equipo": "A", "fila": 10, "columna": 10,
        "rol": "delantero", "tiene_pelota": 1
    })
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Lautaro", "equipo": "A", "fila": 10, "columna": 10,
        "rol": "delantero", "tiene_pelota": "True"
    })
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Lautaro", "equipo": "A", "fila": 10, "columna": 10,
        "rol": "delantero", "tiene_pelota": None
    })

    print("\n-- Rol inválido --")
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Nuevo", "equipo": "A", "fila": 10, "columna": 10,
        "rol": "entrenador", "tiene_pelota": False
    })

    print("\n-- Equipo inválido --")
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Nuevo", "equipo": "C", "fila": 10, "columna": 10,
        "rol": "defensor", "tiene_pelota": False
    })

    print("\n-- Control de posesión única de la pelota --")
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Nuevo", "equipo": "A", "fila": 10, "columna": 10,
        "rol": "delantero", "tiene_pelota": True
    })

    # ── Árbitro ───────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("COLOCANDO ÁRBITRO")
    print("=" * 55)

    arbitro = crear_arbitro(fila=22, columna=38)
    colocar_arbitro(cancha, arbitro)
    print(f"[OK] Árbitro colocado en ({arbitro['fila']}, {arbitro['columna']}) "
          f"con sombra en celdas adyacentes.")

    # ── Obstáculos ────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("AGREGANDO OBSTÁCULOS")
    print("=" * 55)

    agregar_obstaculo(cancha, 20, 42)
    agregar_obstaculo(cancha, 28, 20)

    mostrar_seccion_cancha(cancha, 18, 32, 8, 50)

    # ── Demo de movimientos ───────────────────────────────────
    print("\n" + "=" * 55)
    print("DEMO: MOVIMIENTOS")
    print("=" * 55)

    print("\n-- Movimiento válido --")
    mover_jugador(cancha, jugadores, "De Paul", "arriba")
    mover_jugador(cancha, jugadores, "De Paul", "derecha")

    print("\n-- Movimiento inválido: zona bloqueada (X) --")
    mover_jugador(cancha, jugadores, "Messi", "derecha")
    mover_jugador(cancha, jugadores, "Messi", "derecha")

    print("\n-- Movimiento inválido: celda ocupada por rival --")
    mover_jugador(cancha, jugadores, "Vinicius", "derecha")
    mover_jugador(cancha, jugadores, "Vinicius", "derecha")

    print("\n-- Movimiento inválido: fuera de la cancha --")
    for _ in range(10):
        mover_jugador(cancha, jugadores, "Romero", "izquierda")
    mover_jugador(cancha, jugadores, "Romero", "izquierda")

    print("\n-- Movimiento del árbitro --")
    mover_arbitro(cancha, arbitro, jugadores)

    mostrar_seccion_cancha(cancha, 18, 32, 8, 50)

    # ── Demo análisis ─────────────────────────────────────────
    print("\n" + "=" * 55)
    print("DEMO: DISTANCIAS MANHATTAN")
    print("=" * 55)
    calcular_distancias(jugadores)

    print("\n" + "=" * 55)
    print("DEMO: PASES POSIBLES")
    print("=" * 55)
    detectar_pases(cancha, jugadores)

    print("\n" + "=" * 55)
    print("DEMO: CAMINO LIBRE AL ARCO")
    print("=" * 55)
    detectar_camino_libre(cancha, jugadores)

    # ── Menú interactivo ──────────────────────────────────────
    ejecutar_menu(cancha, jugadores, arbitro)


if __name__ == "__main__":
    main()