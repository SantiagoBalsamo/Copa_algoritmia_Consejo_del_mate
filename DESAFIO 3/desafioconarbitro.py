# =============================================================================
# DESAFÍO 3: "LA CANCHA INTELIGENTE"
# Copa de Algoritmia y Programación - UADE 2026
# =============================================================================

import random

FILAS = 40
COLUMNAS = 60
EQUIPOS_VALIDOS = ("A", "B")
ROLES_VALIDOS = ("arquero", "defensor", "mediocampista", "delantero")

# Símbolo del árbitro y sus sombras en la matriz
SIM_ARBITRO = "R"
SIM_SOMBRA  = "S"


# =============================================================================
# TAREA 1: CREAR LA CANCHA
# =============================================================================

def crear_cancha():
    """Genera la matriz que representa la cancha de fútbol.

    Crea una matriz de 40 filas por 60 columnas inicializada con puntos,
    donde cada punto representa una posición vacía.

    Returns:
        list[list[str]]: Matriz de 40x60 inicializada con ".".
    """
    cancha = [["." for _ in range(COLUMNAS)] for _ in range(FILAS)]
    return cancha


# =============================================================================
# TAREA 2: POSICIONAR JUGADORES
# =============================================================================

def posicionar_jugador(cancha, jugadores, jugador):
    """Agrega un jugador a la cancha validando todas las condiciones requeridas.

    Valida que el nombre no esté duplicado, que la posición sea válida,
    que la celda no tenga obstáculo ni jugador (con mensajes distintos),
    que tiene_pelota sea estrictamente booleano, que el rol y equipo sean
    correctos, y que la pelota no esté duplicada.
    Si todo es correcto, actualiza la matriz y la lista de jugadores.

    Args:
        cancha (list[list[str]]): La matriz que representa la cancha.
        jugadores (list[dict]): Lista con todos los jugadores registrados.
        jugador (dict): Diccionario con los datos del jugador a agregar.
            Debe contener: nombre, equipo, fila, columna, rol, tiene_pelota.

    Returns:
        bool: True si el jugador fue agregado correctamente, False en caso contrario.
    """
    nombre       = jugador["nombre"]
    equipo       = jugador["equipo"]
    fila         = jugador["fila"]
    columna      = jugador["columna"]
    rol          = jugador["rol"]
    tiene_pelota = jugador["tiene_pelota"]

    # Validar nombre duplicado
    if any(j["nombre"] == nombre for j in jugadores):
        print(f"[ERROR] No se pudo agregar a {nombre}: ya existe un jugador con ese nombre.")
        return False

    # Validar límites de la cancha
    if fila < 0 or fila >= FILAS or columna < 0 or columna >= COLUMNAS:
        print(f"[ERROR] No se pudo agregar a {nombre}: posición ({fila}, {columna}) "
              f"fuera de los límites de la cancha.")
        return False

    # Validar que la celda no tenga un obstáculo o el árbitro/sombra
    celda = cancha[fila][columna]
    if celda == "X":
        print(f"[ERROR] No se pudo agregar a {nombre}: la celda ({fila}, {columna}) "
              f"contiene un obstáculo (X).")
        return False
    if celda in (SIM_ARBITRO, SIM_SOMBRA):
        print(f"[ERROR] No se pudo agregar a {nombre}: la celda ({fila}, {columna}) "
              f"está cubierta por el árbitro o su sombra.")
        return False

    # Validar que la celda no esté ocupada por otro jugador
    if celda in ("A", "B"):
        print(f"[ERROR] No se pudo agregar a {nombre}: la celda ({fila}, {columna}) "
              f"ya está ocupada por otro jugador.")
        return False

    # Validar tipo booleano estricto de tiene_pelota
    if not isinstance(tiene_pelota, bool):
        print(f"[ERROR] No se pudo agregar a {nombre}: 'tiene_pelota' debe ser "
              f"True o False (se recibió {type(tiene_pelota).__name__}: {tiene_pelota!r}).")
        return False

    # Validar equipo
    if equipo not in EQUIPOS_VALIDOS:
        print(f"[ERROR] No se pudo agregar a {nombre}: equipo '{equipo}' no válido. "
              f"Use {EQUIPOS_VALIDOS}.")
        return False

    # Validar rol
    if rol not in ROLES_VALIDOS:
        print(f"[ERROR] No se pudo agregar a {nombre}: rol '{rol}' no válido. "
              f"Use {ROLES_VALIDOS}.")
        return False

    # Validar posesión única de la pelota
    if tiene_pelota:
        for j in jugadores:
            if j["tiene_pelota"]:
                print(f"[ERROR] No se pudo agregar a {nombre} con la pelota: "
                      f"{j['nombre']} ya la posee.")
                return False

    # Agregar jugador a la lista y actualizar la matriz
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

    Valida que el movimiento no salga de la cancha, no pise a otro jugador,
    no ingrese a una zona bloqueada (X), ni a la posición del árbitro o su sombra.
    Actualiza la posición del jugador y la matriz.

    Args:
        cancha (list[list[str]]): La matriz que representa la cancha.
        jugadores (list[dict]): Lista con todos los jugadores registrados.
        nombre (str): Nombre del jugador a mover.
        direccion (str): Dirección del movimiento: "arriba", "abajo",
            "izquierda" o "derecha".

    Returns:
        bool: True si el movimiento fue exitoso, False si fue inválido.
    """
    jugador = _buscar_jugador(jugadores, nombre)
    if jugador is None:
        print(f"[ERROR] No se encontró al jugador '{nombre}'.")
        return False

    fila_actual = jugador["fila"]
    col_actual  = jugador["columna"]

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

    delta_fila, delta_col = deltas[direccion]
    nueva_fila = fila_actual + delta_fila
    nueva_col  = col_actual  + delta_col

    # Validar límites de la cancha
    if nueva_fila < 0 or nueva_fila >= FILAS or nueva_col < 0 or nueva_col >= COLUMNAS:
        print(f"[MOVIMIENTO INVÁLIDO] {nombre} no puede moverse hacia {direccion}: "
              f"fuera de la cancha.")
        return False

    celda_destino = cancha[nueva_fila][nueva_col]

    if celda_destino == "X":
        print(f"[MOVIMIENTO INVÁLIDO] {nombre} no puede moverse hacia {direccion}: "
              f"zona bloqueada (X) en ({nueva_fila}, {nueva_col}).")
        return False

    if celda_destino in (SIM_ARBITRO, SIM_SOMBRA):
        print(f"[MOVIMIENTO INVÁLIDO] {nombre} no puede moverse hacia {direccion}: "
              f"celda ({nueva_fila}, {nueva_col}) ocupada por el árbitro o su sombra.")
        return False

    if celda_destino in ("A", "B"):
        print(f"[MOVIMIENTO INVÁLIDO] {nombre} no puede moverse hacia {direccion}: "
              f"celda ({nueva_fila}, {nueva_col}) ocupada por otro jugador.")
        return False

    # Actualizar matriz y posición del jugador
    cancha[fila_actual][col_actual] = "."
    cancha[nueva_fila][nueva_col]   = jugador["equipo"]
    jugador["fila"]    = nueva_fila
    jugador["columna"] = nueva_col

    print(f"[MOVIMIENTO OK] {nombre} se movió hacia {direccion}: "
          f"({fila_actual}, {col_actual}) → ({nueva_fila}, {nueva_col}).")
    return True


# =============================================================================
# TAREA 4: CALCULAR DISTANCIA A LA PELOTA
# =============================================================================

def calcular_distancias(jugadores):
    """Calcula la distancia Manhattan de cada jugador respecto a quien tiene la pelota.

    Muestra por consola la distancia de cada jugador e indica cuál o cuáles
    son los más cercanos. En caso de empate, muestra todos los empatados.

    Args:
        jugadores (list[dict]): Lista con todos los jugadores registrados.

    Returns:
        list[dict]: Lista de jugadores más cercanos a la pelota.
            Retorna lista vacía si ningún jugador tiene la pelota.
    """
    portador = _buscar_portador(jugadores)
    if portador is None:
        print("[ERROR] Ningún jugador tiene la pelota.")
        return []

    print(f"\n--- Distancias Manhattan respecto a {portador['nombre']} "
          f"(pelota en ({portador['fila']}, {portador['columna']})) ---")

    distancias = []
    for jugador in jugadores:
        if jugador["nombre"] == portador["nombre"]:
            continue
        distancia = (abs(jugador["fila"] - portador["fila"]) +
                     abs(jugador["columna"] - portador["columna"]))
        distancias.append((jugador, distancia))
        print(f"  {jugador['nombre']} ({jugador['equipo']}): distancia = {distancia}")

    if not distancias:
        print("  No hay otros jugadores en la cancha.")
        return []

    distancia_minima = min(d for _, d in distancias)
    mas_cercanos = [j for j, d in distancias if d == distancia_minima]

    if len(mas_cercanos) == 1:
        print(f"  >> Jugador más cercano: {mas_cercanos[0]['nombre']} "
              f"(distancia {distancia_minima})")
    else:
        nombres = ", ".join(j["nombre"] for j in mas_cercanos)
        print(f"  >> Empate en distancia {distancia_minima}: {nombres}")

    return mas_cercanos


# =============================================================================
# TAREA 5: DETECTAR POSIBILIDAD DE PASE
# =============================================================================

def detectar_pases(cancha, jugadores):
    """Lista todos los pases posibles para el jugador que posee la pelota.

    Un pase es válido si ambos jugadores son del mismo equipo, están en la
    misma fila o columna, y no hay rivales, obstáculos (X) ni celdas del
    árbitro/sombra entre ellos. Los jugadores del mismo equipo no bloquean.

    Args:
        cancha (list[list[str]]): La matriz que representa la cancha.
        jugadores (list[dict]): Lista con todos los jugadores registrados.

    Returns:
        list[dict]: Lista de jugadores a los que se puede realizar el pase.
            Retorna lista vacía si no hay pases posibles o nadie tiene la pelota.
    """
    portador = _buscar_portador(jugadores)
    if portador is None:
        print("[ERROR] Ningún jugador tiene la pelota.")
        return []

    print(f"\n--- Pases posibles para {portador['nombre']} "
          f"en ({portador['fila']}, {portador['columna']}) ---")

    pases_posibles = []
    equipo_rival = "B" if portador["equipo"] == "A" else "A"

    for jugador in jugadores:
        if jugador["nombre"] == portador["nombre"]:
            continue
        if jugador["equipo"] != portador["equipo"]:
            continue

        misma_fila = jugador["fila"] == portador["fila"]
        misma_col  = jugador["columna"] == portador["columna"]

        if not misma_fila and not misma_col:
            print(f"  [BLOQUEADO] {jugador['nombre']}: no está en línea recta.")
            continue

        bloqueado = _hay_bloqueo_entre(cancha, portador, jugador, equipo_rival)

        if bloqueado:
            print(f"  [BLOQUEADO] Pase a {jugador['nombre']}: hay rival, árbitro "
                  f"u obstáculo en el camino.")
        else:
            print(f"  [PASE POSIBLE] → {jugador['nombre']} "
                  f"en ({jugador['fila']}, {jugador['columna']}).")
            pases_posibles.append(jugador)

    if not pases_posibles:
        print("  No hay pases disponibles.")

    return pases_posibles


def _hay_bloqueo_entre(cancha, portador, receptor, equipo_rival):
    """Verifica si existe un rival, árbitro, sombra u obstáculo entre portador y receptor.

    Solo analiza en línea recta (misma fila o misma columna). Los jugadores
    del mismo equipo no se consideran bloqueo.

    Args:
        cancha (list[list[str]]): La matriz que representa la cancha.
        portador (dict): Jugador que tiene la pelota.
        receptor (dict): Jugador al que se intenta pasar.
        equipo_rival (str): Símbolo del equipo rival ("A" o "B").

    Returns:
        bool: True si hay bloqueo, False si el camino está libre.
    """
    BLOQUEANTES = {"X", equipo_rival, SIM_ARBITRO, SIM_SOMBRA}

    fila_p, col_p = portador["fila"], portador["columna"]
    fila_r, col_r = receptor["fila"], receptor["columna"]

    if fila_p == fila_r:
        col_min = min(col_p, col_r) + 1
        col_max = max(col_p, col_r)
        for col in range(col_min, col_max):
            if cancha[fila_p][col] in BLOQUEANTES:
                return True
    else:
        fila_min = min(fila_p, fila_r) + 1
        fila_max = max(fila_p, fila_r)
        for fila in range(fila_min, fila_max):
            if cancha[fila][col_p] in BLOQUEANTES:
                return True

    return False


# =============================================================================
# TAREA 6: DETECTAR CAMINO LIBRE AL ARCO
# =============================================================================

def detectar_camino_libre(cancha, jugadores):
    """Detecta qué delanteros tienen camino libre al arco rival.

    Un delantero tiene camino libre si está en la mitad ofensiva de su equipo
    y no hay rivales, obstáculos (X) ni celdas del árbitro/sombra en su misma
    fila entre él y el arco rival. Los compañeros de equipo no bloquean.

    Mitad ofensiva:
        - Argentina (A): columnas 30 a 59.
        - Brasil (B): columnas 0 a 29.

    Args:
        cancha (list[list[str]]): La matriz que representa la cancha.
        jugadores (list[dict]): Lista con todos los jugadores registrados.

    Returns:
        list[dict]: Lista de delanteros con camino libre al arco.
    """
    print("\n--- Detección de camino libre al arco ---")

    delanteros_libres = []
    hay_delanteros = False

    for jugador in jugadores:
        if jugador["rol"] != "delantero":
            continue

        hay_delanteros = True
        nombre  = jugador["nombre"]
        equipo  = jugador["equipo"]
        fila    = jugador["fila"]
        columna = jugador["columna"]

        en_mitad_ofensiva = (
            (equipo == "A" and 30 <= columna <= 59) or
            (equipo == "B" and 0  <= columna <= 29)
        )

        if not en_mitad_ofensiva:
            print(f"  [SIN CAMINO LIBRE] {nombre}: no está en la mitad ofensiva.")
            continue

        equipo_rival  = "B" if equipo == "A" else "A"
        BLOQUEANTES   = {"X", equipo_rival, SIM_ARBITRO, SIM_SOMBRA}

        if equipo == "A":
            rango_cols = range(columna + 1, COLUMNAS)
        else:
            rango_cols = range(columna - 1, -1, -1)

        camino_libre = True
        for col in rango_cols:
            if cancha[fila][col] in BLOQUEANTES:
                camino_libre = False
                break

        if camino_libre:
            print(f"  [CAMINO LIBRE] {nombre} tiene camino libre al arco rival.")
            delanteros_libres.append(jugador)
        else:
            print(f"  [SIN CAMINO LIBRE] {nombre}: hay rival, árbitro u obstáculo "
                  f"en su fila.")

    if not hay_delanteros:
        print("  No hay delanteros registrados en la cancha.")

    return delanteros_libres


# =============================================================================
# ÁRBITRO: POSICIONAMIENTO Y MOVIMIENTO ALEATORIO
# =============================================================================

def crear_arbitro(fila, columna):
    """Crea el diccionario que representa al árbitro.

    El árbitro ocupa una celda central y proyecta sombra en las cuatro celdas
    adyacentes (arriba, abajo, izquierda, derecha), que también actúan como
    obstáculos para pases y movimientos.

    Args:
        fila (int): Fila inicial del árbitro.
        columna (int): Columna inicial del árbitro.

    Returns:
        dict: Diccionario con la posición del árbitro.
    """
    return {"fila": fila, "columna": columna}


def _celdas_sombra(fila, columna):
    """Calcula las celdas adyacentes que forman la sombra del árbitro.

    La sombra cubre las cuatro celdas ortogonales al árbitro, siempre
    que estén dentro de los límites de la cancha.

    Args:
        fila (int): Fila actual del árbitro.
        columna (int): Columna actual del árbitro.

    Returns:
        list[tuple[int, int]]: Lista de (fila, columna) de celdas con sombra.
    """
    candidatas = [
        (fila - 1, columna),
        (fila + 1, columna),
        (fila, columna - 1),
        (fila, columna + 1),
    ]
    return [(f, c) for f, c in candidatas
            if 0 <= f < FILAS and 0 <= c < COLUMNAS]


def colocar_arbitro(cancha, arbitro):
    """Coloca al árbitro y su sombra en la cancha.

    Marca con SIM_ARBITRO la celda del árbitro y con SIM_SOMBRA las
    celdas adyacentes, siempre que estén vacías o ya sean sombra/árbitro.
    No desplaza jugadores ni obstáculos existentes.

    Args:
        cancha (list[list[str]]): La matriz que representa la cancha.
        arbitro (dict): Diccionario con la posición del árbitro.

    Returns:
        None
    """
    fila, columna = arbitro["fila"], arbitro["columna"]
    cancha[fila][columna] = SIM_ARBITRO
    for f, c in _celdas_sombra(fila, columna):
        if cancha[f][c] == ".":
            cancha[f][c] = SIM_SOMBRA


def quitar_arbitro(cancha, arbitro):
    """Elimina al árbitro y su sombra de la cancha.

    Restaura a "." las celdas que pertenecían al árbitro o su sombra,
    sin tocar jugadores ni obstáculos.

    Args:
        cancha (list[list[str]]): La matriz que representa la cancha.
        arbitro (dict): Diccionario con la posición actual del árbitro.

    Returns:
        None
    """
    fila, columna = arbitro["fila"], arbitro["columna"]
    cancha[fila][columna] = "."
    for f, c in _celdas_sombra(fila, columna):
        if cancha[f][c] == SIM_SOMBRA:
            cancha[f][c] = "."


def mover_arbitro(cancha, arbitro, jugadores):
    """Mueve al árbitro aleatoriamente una celda hacia la jugada activa.

    El árbitro intenta moverse hacia el jugador con la pelota. Si la celda
    elegida está ocupada por un jugador u obstáculo, busca otra dirección
    aleatoria. Si no puede moverse, permanece en su lugar.

    Args:
        cancha (list[list[str]]): La matriz que representa la cancha.
        arbitro (dict): Diccionario con la posición actual del árbitro.
        jugadores (list[dict]): Lista con todos los jugadores registrados.

    Returns:
        None
    """
    portador = _buscar_portador(jugadores)
    fila_a, col_a = arbitro["fila"], arbitro["columna"]

    # Calcular dirección preferida hacia el portador
    if portador:
        fila_p, col_p = portador["fila"], portador["columna"]
        df = 0 if fila_p == fila_a else (1 if fila_p > fila_a else -1)
        dc = 0 if col_p  == col_a  else (1 if col_p  > col_a  else -1)
        # Elegir el eje con mayor diferencia para acercarse paso a paso
        if abs(fila_p - fila_a) >= abs(col_p - col_a):
            direcciones = [(df, 0), (0, dc), (-df, 0), (0, -dc)]
        else:
            direcciones = [(0, dc), (df, 0), (0, -dc), (-df, 0)]
        # Añadir algo de aleatoriedad mezclando las opciones no preferidas
        random.shuffle(direcciones[1:])
    else:
        # Sin portador: movimiento completamente aleatorio
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(direcciones)

    quitar_arbitro(cancha, arbitro)

    for df, dc in direcciones:
        nf, nc = fila_a + df, col_a + dc
        if 0 <= nf < FILAS and 0 <= nc < COLUMNAS:
            celda = cancha[nf][nc]
            # El árbitro no puede pisar jugadores ni obstáculos fijos
            if celda not in ("A", "B", "X"):
                arbitro["fila"]    = nf
                arbitro["columna"] = nc
                break

    colocar_arbitro(cancha, arbitro)
    print(f"[ÁRBITRO] Se movió a ({arbitro['fila']}, {arbitro['columna']}).")


# =============================================================================
# MENÚ INTERACTIVO
# =============================================================================

def mostrar_menu():
    """Imprime el menú principal de opciones del programa.

    Returns:
        None
    """
    print("\n" + "=" * 55)
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
    """Solicita al usuario el nombre del jugador y la dirección para moverlo.

    Args:
        cancha (list[list[str]]): La matriz que representa la cancha.
        jugadores (list[dict]): Lista con todos los jugadores registrados.

    Returns:
        None
    """
    nombre = input("  Nombre del jugador: ").strip()
    print("  Dirección: arriba / abajo / izquierda / derecha")
    direccion = input("  Dirección: ").strip().lower()
    mover_jugador(cancha, jugadores, nombre, direccion)


def mostrar_jugadores(jugadores):
    """Imprime por consola la posición y estado de todos los jugadores.

    Args:
        jugadores (list[dict]): Lista con todos los jugadores registrados.

    Returns:
        None
    """
    print("\n--- Jugadores en cancha ---")
    for j in jugadores:
        pelota = " [PELOTA]" if j["tiene_pelota"] else ""
        print(f"  {j['nombre']:15s} | {j['equipo']} | {j['rol']:15s} | "
              f"fila {j['fila']:2d}, col {j['columna']:2d}{pelota}")


def ejecutar_menu(cancha, jugadores, arbitro):
    """Ejecuta el bucle principal del menú interactivo.

    Permite al usuario mover jugadores, consultar pases, distancias y
    camino libre, y mover al árbitro, hasta que elija salir.

    Args:
        cancha (list[list[str]]): La matriz que representa la cancha.
        jugadores (list[dict]): Lista con todos los jugadores registrados.
        arbitro (dict): Diccionario con la posición actual del árbitro.

    Returns:
        None
    """
    while True:
        mostrar_menu()
        opcion = input("  Elegí una opción: ").strip()

        if opcion == "1":
            # Mostrar zona central de la cancha
            mostrar_seccion_cancha(cancha, 0, FILAS - 1, 0, COLUMNAS - 1)
        elif opcion == "2":
            menu_mover_jugador(cancha, jugadores)
        elif opcion == "3":
            calcular_distancias(jugadores)
        elif opcion == "4":
            detectar_pases(cancha, jugadores)
        elif opcion == "5":
            detectar_camino_libre(cancha, jugadores)
        elif opcion == "6":
            mover_arbitro(cancha, arbitro, jugadores)
        elif opcion == "7":
            mostrar_jugadores(jugadores)
        elif opcion == "0":
            print("\n  ¡Hasta la próxima!\n")
            break
        else:
            print("  [ERROR] Opción no válida. Ingresá un número del 0 al 7.")


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def _buscar_jugador(jugadores, nombre):
    """Busca un jugador en la lista por su nombre.

    Args:
        jugadores (list[dict]): Lista con todos los jugadores registrados.
        nombre (str): Nombre del jugador a buscar.

    Returns:
        dict | None: El diccionario del jugador si se encuentra, None si no.
    """
    for jugador in jugadores:
        if jugador["nombre"] == nombre:
            return jugador
    return None


def _buscar_portador(jugadores):
    """Busca el jugador que actualmente posee la pelota.

    Args:
        jugadores (list[dict]): Lista con todos los jugadores registrados.

    Returns:
        dict | None: El diccionario del jugador con la pelota, None si ninguno la tiene.
    """
    for jugador in jugadores:
        if jugador["tiene_pelota"]:
            return jugador
    return None


def agregar_obstaculo(cancha, fila, columna):
    """Coloca un obstáculo fijo en una posición de la cancha.

    Args:
        cancha (list[list[str]]): La matriz que representa la cancha.
        fila (int): Fila donde se coloca el obstáculo.
        columna (int): Columna donde se coloca el obstáculo.

    Returns:
        bool: True si se colocó correctamente, False si la posición es inválida
            o está ocupada.
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


def mostrar_seccion_cancha(cancha, fila_inicio, fila_fin, col_inicio, col_fin):
    """Muestra una sección de la cancha por consola.

    Útil para visualizar zonas específicas sin imprimir la matriz completa.

    Args:
        cancha (list[list[str]]): La matriz que representa la cancha.
        fila_inicio (int): Fila inicial del recorte (inclusiva).
        fila_fin (int): Fila final del recorte (inclusiva).
        col_inicio (int): Columna inicial del recorte (inclusiva).
        col_fin (int): Columna final del recorte (inclusiva).

    Returns:
        None
    """
    print(f"\n--- Vista de la cancha (filas {fila_inicio}-{fila_fin}, "
          f"cols {col_inicio}-{col_fin}) ---")
    for fila in range(fila_inicio, fila_fin + 1):
        fila_str = " ".join(cancha[fila][col_inicio:col_fin + 1])
        print(f"  F{fila:02d}: {fila_str}")


# =============================================================================
# MAIN: CARGA INICIAL + CASOS BORDE + MENÚ INTERACTIVO
# =============================================================================

if __name__ == "__main__":

    print("=" * 55)
    print("   DESAFÍO 3: LA CANCHA INTELIGENTE — UADE 2026")
    print("=" * 55)

    # --- Inicializar cancha y lista de jugadores ---
    cancha    = crear_cancha()
    jugadores = []

    # =========================================================
    # CARGA PREVIA DE JUGADORES (datos hardcodeados)
    # =========================================================
    print("\n" + "=" * 55)
    print("CARGANDO JUGADORES INICIALES")
    print("=" * 55)

    jugadores_iniciales = [
        {"nombre": "Messi",    "equipo": "A", "fila": 20, "columna": 40,
         "rol": "delantero",      "tiene_pelota": True},
        {"nombre": "Di Maria", "equipo": "A", "fila": 20, "columna": 45,
         "rol": "delantero",      "tiene_pelota": False},
        {"nombre": "De Paul",  "equipo": "A", "fila": 25, "columna": 40,
         "rol": "mediocampista",  "tiene_pelota": False},
        {"nombre": "Romero",   "equipo": "A", "fila": 30, "columna": 10,
         "rol": "defensor",       "tiene_pelota": False},
        {"nombre": "Vinicius", "equipo": "B", "fila": 20, "columna": 43,
         "rol": "delantero",      "tiene_pelota": False},
        {"nombre": "Rodrygo",  "equipo": "B", "fila": 28, "columna": 15,
         "rol": "delantero",      "tiene_pelota": False},
        {"nombre": "Casemiro", "equipo": "B", "fila": 25, "columna": 30,
         "rol": "mediocampista",  "tiene_pelota": False},
    ]

    for j in jugadores_iniciales:
        posicionar_jugador(cancha, jugadores, j)

    # =========================================================
    # CASOS BORDE — VALIDACIONES
    # =========================================================
    print("\n" + "=" * 55)
    print("CASOS BORDE")
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
        "nombre": "Alvarez", "equipo": "A", "fila": 20, "columna": 40,
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

    print("\n-- Dos jugadores con pelota --")
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Alvarez", "equipo": "A", "fila": 18, "columna": 38,
        "rol": "delantero", "tiene_pelota": True
    })

    # =========================================================
    # ÁRBITRO
    # =========================================================
    print("\n" + "=" * 55)
    print("COLOCANDO ÁRBITRO")
    print("=" * 55)

    # El árbitro arranca cerca de la jugada (junto a Messi en fila 20, col 40)
    arbitro = crear_arbitro(fila=22, columna=38)
    colocar_arbitro(cancha, arbitro)
    print(f"[OK] Árbitro colocado en ({arbitro['fila']}, {arbitro['columna']}) "
          f"con sombra en celdas adyacentes.")

    # =========================================================
    # OBSTÁCULOS ADICIONALES
    # =========================================================
    print("\n" + "=" * 55)
    print("AGREGANDO OBSTÁCULOS")
    print("=" * 55)

    agregar_obstaculo(cancha, 20, 42)   # Entre Messi y Di Maria
    agregar_obstaculo(cancha, 28, 20)   # En fila de Rodrygo

    mostrar_seccion_cancha(cancha, 18, 32, 8, 50)

    # =========================================================
    # DEMO AUTOMÁTICA: movimientos y análisis
    # =========================================================
    print("\n" + "=" * 55)
    print("DEMO: MOVIMIENTOS")
    print("=" * 55)

    mover_jugador(cancha, jugadores, "De Paul", "arriba")
    mover_jugador(cancha, jugadores, "De Paul", "derecha")

    print("\n-- Hacia obstáculo X --")
    mover_jugador(cancha, jugadores, "Messi", "derecha")   # col 40→41 OK
    mover_jugador(cancha, jugadores, "Messi", "derecha")   # col 41→42 = X BLOQUEADO

    print("\n-- Hacia jugador rival --")
    mover_jugador(cancha, jugadores, "Vinicius", "derecha")  # 43→44 OK
    mover_jugador(cancha, jugadores, "Vinicius", "derecha")  # 44→45 = Di Maria BLOQUEADO

    print("\n-- Fuera de la cancha --")
    for _ in range(10):
        mover_jugador(cancha, jugadores, "Romero", "izquierda")
    mover_jugador(cancha, jugadores, "Romero", "izquierda")  # col 0 → FUERA

    print("\n-- Hacia sombra del árbitro --")
    # De Paul quedó en (24, 41); árbitro en (22,38), sombra en (23,38)
    # Lo movemos para que intente pisar una sombra
    mover_arbitro(cancha, arbitro, jugadores)   # árbitro se mueve 1 vez
    mostrar_seccion_cancha(cancha, 18, 32, 8, 50)

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

    # Agregar delantero con camino libre garantizado
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Alvarez", "equipo": "A", "fila": 3, "columna": 35,
        "rol": "delantero", "tiene_pelota": False
    })
    detectar_camino_libre(cancha, jugadores)

    # =========================================================
    # MENÚ INTERACTIVO
    # =========================================================
    ejecutar_menu(cancha, jugadores, arbitro)