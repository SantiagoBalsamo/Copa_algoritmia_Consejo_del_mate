# DESAFÍO 3: "LA CANCHA INTELIGENTE"
# Copa de Algoritmia y Programación - UADE 2026

import random

def crear_cancha():
    """
    Crea y retorna la cancha de juego como una matriz de 40 filas x 60 columnas.

    Returns:
        Matriz 40x60 inicializada con '.' en cada celda.
    """
    return [["." for _ in range(60)] for _ in range(40)]


def _dentro_de_limites(fila, columna):
    """
    Verifica si una posicion esta dentro de los limites de la cancha (0-39, 0-59).

    Args:
        Numero de fila a verificar.
        Numero de columna a verificar.

    Returns:
        bool: True si la posicion es valida, False si esta fuera de los limites.
    """
    return 0 <= fila <= 39 and 0 <= columna <= 59


def _celdas_sombra_arbitro(arbitro):
    """
    Calcula el conjunto de celdas bloqueadas por el arbitro: su celda y las 4 adyacentes.

    Args:
        Diccionario con claves 'fila' y 'columna'.

    Returns:
        Conjunto de tuplas (fila, columna) que forman la sombra.
    """
    sombra = set()
    fila_arbitro = arbitro["fila"]
    col_arbitro = arbitro["columna"]
    for delta_fila, delta_col in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
        nueva_fila = fila_arbitro + delta_fila
        nueva_col = col_arbitro + delta_col
        if _dentro_de_limites(nueva_fila, nueva_col):
            sombra.add((nueva_fila, nueva_col))
    return sombra


def _jugador_con_pelota(jugadores):
    """
    Busca y retorna el jugador que actualmente tiene la pelota.

    Args:
        Lista de jugadores en la cancha.

    Returns:
        El jugador con tiene_pelota=True, o None si ninguno la tiene.
    """
    for jugador in jugadores:
        if jugador["tiene_pelota"]:
            return jugador
    return None


def _actualizar_celda_arbitro(cancha, fila_vieja, col_vieja, fila_nueva, col_nueva):
    """
    Actualiza solo las dos celdas afectadas por el movimiento del arbitro.

    Args:
        cancha: La matriz de la cancha.
        fila_vieja: Fila donde estaba el arbitro.
        col_vieja: Columna donde estaba el arbitro.
        fila_nueva: Fila a donde se mueve el arbitro.
        col_nueva: Columna a donde se mueve el arbitro.
    """
    cancha[fila_vieja][col_vieja] = "."
    # Restaurar obstaculo si la celda vieja era uno
    if (fila_vieja, col_vieja) in {(obs[0], obs[1]) for obs in OBSTACULOS}:
        cancha[fila_vieja][col_vieja] = "X"
    cancha[fila_nueva][col_nueva] = "R"


def _mover_arbitro(cancha, jugadores, arbitro):
    """
    Mueve el arbitro una celda tendiendo a acercarse al jugador con la pelota
    (sigue la jugada), con 70% de probabilidad elige la direccion que lo acerca
    al portador; con 30% se mueve de forma aleatoria. Solo ocupa celdas libres.
    Si ninguna celda esta disponible, permanece en su lugar e informa.

    Args:
        cancha: La matriz de la cancha.
        jugadores: Lista de jugadores para evitar colisiones.
        arbitro: Diccionario con la posicion actual del arbitro.
    """
    posiciones_jugadores = {(j["fila"], j["columna"]) for j in jugadores}
    posiciones_obstaculos = {(obs[0], obs[1]) for obs in OBSTACULOS}
    fila_actual = arbitro["fila"]
    col_actual = arbitro["columna"]
    todos_los_deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    portador = _jugador_con_pelota(jugadores)
    if portador and random.random() < 0.70:
        # Priorizar las direcciones que acercan el arbitro al portador
        def acercamiento(delta):
            nf = fila_actual + delta[0]
            nc = col_actual + delta[1]
            return abs(nf - portador["fila"]) + abs(nc - portador["columna"])

        dist_actual = abs(fila_actual - portador["fila"]) + abs(col_actual - portador["columna"])
        deltas_acercan = [d for d in todos_los_deltas if acercamiento(d) < dist_actual]
        deltas_alejan  = [d for d in todos_los_deltas if acercamiento(d) >= dist_actual]
        random.shuffle(deltas_acercan)
        random.shuffle(deltas_alejan)
        # Intenta primero los que acercan; usa los otros como respaldo
        deltas_ordenados = deltas_acercan + deltas_alejan
    else:
        random.shuffle(todos_los_deltas)
        deltas_ordenados = todos_los_deltas

    for delta_fila, delta_col in deltas_ordenados:
        nueva_fila = fila_actual + delta_fila
        nueva_col  = col_actual + delta_col
        celda_libre = (
            _dentro_de_limites(nueva_fila, nueva_col)
            and (nueva_fila, nueva_col) not in posiciones_jugadores
            and (nueva_fila, nueva_col) not in posiciones_obstaculos
        )
        if celda_libre:
            _actualizar_celda_arbitro(cancha, fila_actual, col_actual, nueva_fila, nueva_col)
            arbitro["fila"] = nueva_fila
            arbitro["columna"] = nueva_col
            return

    print("  [Arbitro] No encontro celda libre para moverse, permanece en su lugar.")


ROLES_VALIDOS = {"arquero", "defensor", "mediocampista", "delantero"}
EQUIPOS_VALIDOS = {"A", "B"}


def posicionar_jugador(cancha, jugadores, jugador, arbitro=None):
    """
    Valida todas las condiciones y agrega un jugador a la cancha si son correctas.

    Validaciones realizadas:
        - Posicion dentro de los limites (0-39, 0-59).
        - Celda destino desocupada (sin jugador, obstaculo ni arbitro).
        - Celda fuera de la sombra del arbitro (si hay arbitro).
        - Rol valido: arquero, defensor, mediocampista o delantero.
        - Equipo valido: 'A' o 'B'.
        - Nombre no vacio y no duplicado.
        - Solo un jugador puede tener tiene_pelota=True a la vez.

    Args:
        cancha: La matriz de la cancha.
        jugadores: Lista actual de jugadores.
        jugador: Diccionario con los datos del nuevo jugador.
        arbitro: Posicion del arbitro para validar su sombra.

    Returns:
        True si el jugador fue agregado correctamente, False si hubo algun error.
    """
    nombre = jugador.get("nombre", "").strip()

    # Nombre no puede estar vacio
    if not nombre:
        print("  Error: El nombre del jugador no puede estar vacio.")
        return False

    # Nombre no duplicado
    nombres_existentes = [j["nombre"].lower() for j in jugadores]
    if nombre.lower() in nombres_existentes:
        print(f"  Error: Ya existe un jugador con el nombre '{nombre}'.")
        return False

    # Posicion dentro de limites
    if not _dentro_de_limites(jugador["fila"], jugador["columna"]):
        print(f"  Error: La posicion ({jugador['fila']}, {jugador['columna']}) esta fuera de los limites.")
        return False

    # Celda no ocupada
    celda_destino = cancha[jugador["fila"]][jugador["columna"]]
    if celda_destino != ".":
        print(f"  Error: La celda ({jugador['fila']}, {jugador['columna']}) esta ocupada por '{celda_destino}'.")
        return False

    # Sombra del arbitro
    if arbitro:
        sombra = _celdas_sombra_arbitro(arbitro)
        if (jugador["fila"], jugador["columna"]) in sombra:
            print(f"  Error: La celda ({jugador['fila']}, {jugador['columna']}) esta dentro de la sombra del arbitro.")
            return False

    # Rol valido
    if jugador["rol"] not in ROLES_VALIDOS:
        print(f"  Error: Rol '{jugador['rol']}' invalido. Roles validos: {sorted(ROLES_VALIDOS)}.")
        return False

    # Equipo valido
    if jugador["equipo"] not in EQUIPOS_VALIDOS:
        print(f"  Error: Equipo '{jugador['equipo']}' invalido. Debe ser 'A' o 'B'.")
        return False

    # Solo un jugador con pelota a la vez
    if jugador.get("tiene_pelota", False):
        portador_actual = _jugador_con_pelota(jugadores)
        if portador_actual is not None:
            print(f"  Error: Ya hay un jugador con la pelota ({portador_actual['nombre']}). Solo puede haber uno.")
            return False

    jugadores.append(jugador)
    cancha[jugador["fila"]][jugador["columna"]] = jugador["equipo"]
    print(f"  OK: Jugador '{nombre}' ({jugador['equipo']}, {jugador['rol']}) posicionado en ({jugador['fila']}, {jugador['columna']}).")
    return True


DIRECCIONES = {
    "arriba":    (-1,  0),
    "abajo":     ( 1,  0),
    "izquierda": ( 0, -1),
    "derecha":   ( 0,  1),
}


def mover_jugador(cancha, jugadores, nombre_jugador, direccion, arbitro):
    """
    Mueve un jugador una celda en la direccion indicada, si el movimiento es valido.
    Tras intentar el movimiento (exitoso o no), el arbitro se desplaza aleatoriamente.

    Args:
        cancha: La matriz de la cancha.
        jugadores: Lista de jugadores en la cancha.
        nombre_jugador: Nombre del jugador a mover (no distingue mayusculas).
        direccion: Direccion del movimiento: 'arriba', 'abajo', 'izquierda' o 'derecha'.
        arbitro: Posicion actual del arbitro.

    Returns:
        bool: True si el movimiento fue exitoso, False en caso contrario.
    """
    # Buscar jugador por nombre (sin distinguir mayusculas)
    jugador_a_mover = None
    for jugador in jugadores:
        if jugador["nombre"].lower() == nombre_jugador.lower():
            jugador_a_mover = jugador
            break

    if jugador_a_mover is None:
        print(f"  Error: Jugador '{nombre_jugador}' no encontrado.")
        return False

    if direccion not in DIRECCIONES:
        print(f"  Error: Direccion '{direccion}' invalida. Use: {list(DIRECCIONES.keys())}.")
        return False

    delta_fila, delta_col = DIRECCIONES[direccion]
    nueva_fila = jugador_a_mover["fila"] + delta_fila
    nueva_col = jugador_a_mover["columna"] + delta_col

    # Verificar limites
    if not _dentro_de_limites(nueva_fila, nueva_col):
        print(f"  Movimiento invalido: la celda ({nueva_fila}, {nueva_col}) esta fuera de los limites.")
        _mover_arbitro(cancha, jugadores, arbitro)
        return False

    # Verificar celda destino libre
    celda_destino = cancha[nueva_fila][nueva_col]
    if celda_destino != ".":
        print(f"  Movimiento invalido: la celda ({nueva_fila}, {nueva_col}) esta ocupada por '{celda_destino}'.")
        _mover_arbitro(cancha, jugadores, arbitro)
        return False

    # Verificar sombra del arbitro (las celdas adyacentes al arbitro aparecen como '.' en la matriz
    # pero deben tratarse como bloqueadas segun el enunciado)
    sombra = _celdas_sombra_arbitro(arbitro)
    if (nueva_fila, nueva_col) in sombra:
        print(f"  Movimiento invalido: la celda ({nueva_fila}, {nueva_col}) esta en la zona del arbitro.")
        _mover_arbitro(cancha, jugadores, arbitro)
        return False

    # Ejecutar el movimiento: limpiar celda anterior y marcar la nueva
    cancha[jugador_a_mover["fila"]][jugador_a_mover["columna"]] = "."
    jugador_a_mover["fila"] = nueva_fila
    jugador_a_mover["columna"] = nueva_col
    cancha[nueva_fila][nueva_col] = jugador_a_mover["equipo"]
    print(f"  OK: {jugador_a_mover['nombre']} se movio {direccion} -> ({nueva_fila}, {nueva_col}).")

    _mover_arbitro(cancha, jugadores, arbitro)
    return True


def calcular_distancias(jugadores):
    """
    Calcula la distancia Manhattan desde cada jugador hasta el portador de la pelota.
    Formula: |fila1 - fila2| + |columna1 - columna2|
    Muestra una tabla con todos los jugadores e indica quien/quienes estan mas cerca,
    contemplando empates. El portador queda excluido del calculo.

    Args:
        Lista de jugadores en la cancha.
    """
    portador = _jugador_con_pelota(jugadores)
    if portador is None:
        print("  Error: Ningun jugador tiene la pelota.")
        return

    print(f"\n  Portador: {portador['nombre']} ({portador['equipo']}) en ({portador['fila']}, {portador['columna']})")
    print(f"  {'Jugador':<20} {'Equipo':<8} {'Fila,Col':<14} {'Distancia'}")
    print("  " + "-" * 55)

    distancias = []
    for jugador in jugadores:
        if jugador is portador:
            continue
        dist = abs(jugador["fila"] - portador["fila"]) + abs(jugador["columna"] - portador["columna"])
        distancias.append((jugador, dist))
        print(f"  {jugador['nombre']:<20} {jugador['equipo']:<8} ({jugador['fila']},{jugador['columna']}){'':>6} {dist}")

    if not distancias:
        print("  No hay otros jugadores.")
        return

    distancia_minima = min(dist for _, dist in distancias)
    mas_cercanos = [jugador["nombre"] for jugador, dist in distancias if dist == distancia_minima]
    print(f"\n  Mas cercano(s) (dist={distancia_minima}): {', '.join(mas_cercanos)}")


# ─────────────────────────────────────────────
#  TAREA 5 – detectar_pases
# ─────────────────────────────────────────────
def _linea_libre(cancha, arbitro, fila_origen, col_origen, fila_destino, col_destino, equipo_portador):
    """
    Verifica que el camino recto entre dos posiciones no tenga obstaculos bloqueantes.
    Solo funciona para lineas horizontales o verticales (no diagonales).
    Se revisan unicamente las celdas intermedias (no los extremos).

    Bloquea el pase: rivales, obstaculos 'X', arbitro 'R' y su sombra.
    No bloquea el pase: jugadores del mismo equipo.

    Args:
        cancha: La matriz de la cancha.
        arbitro: Posicion del arbitro para calcular su sombra.
        fila_origen: Fila del jugador con la pelota.
        col_origen: Columna del jugador con la pelota.
        fila_destino: Fila del receptor.
        col_destino: Columna del receptor.
        equipo_portador: Equipo del portador ('A' o 'B').

    Returns:
        True si la linea esta libre para el pase, False si esta bloqueada.
    """
    sombra = _celdas_sombra_arbitro(arbitro)
    equipo_rival = "B" if equipo_portador == "A" else "A"

    if fila_origen == fila_destino:
        # Pase horizontal: recorrer columnas intermedias
        col_menor = min(col_origen, col_destino)
        col_mayor = max(col_origen, col_destino)
        for col_intermedia in range(col_menor + 1, col_mayor):
            if (fila_origen, col_intermedia) in sombra:
                return False
            celda = cancha[fila_origen][col_intermedia]
            if celda == "X" or celda == "R" or celda == equipo_rival:
                return False

    elif col_origen == col_destino:
        # Pase vertical: recorrer filas intermedias
        fila_menor = min(fila_origen, fila_destino)
        fila_mayor = max(fila_origen, fila_destino)
        for fila_intermedia in range(fila_menor + 1, fila_mayor):
            if (fila_intermedia, col_origen) in sombra:
                return False
            celda = cancha[fila_intermedia][col_origen]
            if celda == "X" or celda == "R" or celda == equipo_rival:
                return False

    else:
        # Pase diagonal: no permitido por el enunciado
        return False

    return True


def _motivo_bloqueo_pase(cancha, arbitro, fila_origen, col_origen, fila_destino, col_destino, equipo_portador):
    """
    Determina el motivo por el que un pase esta bloqueado, para mostrarlo al usuario.
    Recorre las celdas intermedias de la linea y devuelve una descripcion del primer
    obstaculo encontrado.

    Args:
        cancha: La matriz de la cancha.
        arbitro: Posicion del arbitro.
        fila_origen: Fila del portador.
        col_origen: Columna del portador.
        fila_destino: Fila del receptor.
        col_destino: Columna del receptor.
        equipo_portador: Equipo del portador ('A' o 'B').

    Returns:
        Descripcion del motivo de bloqueo.
    """
    sombra = _celdas_sombra_arbitro(arbitro)
    equipo_rival = "B" if equipo_portador == "A" else "A"

    if fila_origen == fila_destino:
        col_menor = min(col_origen, col_destino)
        col_mayor = max(col_origen, col_destino)
        celdas = [(fila_origen, c) for c in range(col_menor + 1, col_mayor)]
    else:
        fila_menor = min(fila_origen, fila_destino)
        fila_mayor = max(fila_origen, fila_destino)
        celdas = [(f, col_origen) for f in range(fila_menor + 1, fila_mayor)]

    for fila_c, col_c in celdas:
        if (fila_c, col_c) in sombra:
            return f"zona del arbitro en ({fila_c}, {col_c})"
        celda = cancha[fila_c][col_c]
        if celda == "X":
            return f"obstaculo fijo en ({fila_c}, {col_c})"
        if celda == "R":
            return f"arbitro en ({fila_c}, {col_c})"
        if celda == equipo_rival:
            return f"rival en ({fila_c}, {col_c})"
    return "diagonal (no permitido)"


def detectar_pases(cancha, jugadores, arbitro):
    """
    Detecta y muestra todos los pases posibles para el jugador que tiene la pelota.
    Para cada companero del mismo equipo que este en la misma fila o columna, informa
    si el pase es posible o indica el motivo por el que esta bloqueado.
    Al final sugiere movimientos utiles si no hay pases disponibles.

    Un pase es valido si:
        - El receptor es del mismo equipo.
        - Esta en la misma fila o columna (sin diagonales).
        - No hay rivales, obstaculos 'X', arbitro ni su sombra en la linea intermedia.

    Args:
        cancha: La matriz de la cancha.
        jugadores: Lista de jugadores en la cancha.
        arbitro: Posicion del arbitro.
    """
    portador = _jugador_con_pelota(jugadores)
    if portador is None:
        print("  Error: Ningun jugador tiene la pelota.")
        return

    equipo_portador = portador["equipo"]
    nombre_equipo = "Argentina" if equipo_portador == "A" else "Brasil"
    print(f"\n  === SUGERENCIA DE JUGADAS ===")
    print(f"  Portador: {portador['nombre']} ({nombre_equipo}) en ({portador['fila']}, {portador['columna']})")
    print(f"  Arbitro en: ({arbitro['fila']}, {arbitro['columna']})")
    print()

    pases_validos = []
    pases_bloqueados = []
    companeros_sin_linea = []

    for jugador in jugadores:
        if jugador is portador:
            continue
        if jugador["equipo"] != equipo_portador:
            continue

        misma_fila    = jugador["fila"]    == portador["fila"]
        misma_columna = jugador["columna"] == portador["columna"]

        if not misma_fila and not misma_columna:
            # Companero en diagonal: no tiene linea directa
            companeros_sin_linea.append(jugador)
            continue

        if _linea_libre(cancha, arbitro,
                        portador["fila"], portador["columna"],
                        jugador["fila"],  jugador["columna"],
                        equipo_portador):
            pases_validos.append(jugador)
        else:
            motivo = _motivo_bloqueo_pase(
                cancha, arbitro,
                portador["fila"], portador["columna"],
                jugador["fila"],  jugador["columna"],
                equipo_portador
            )
            pases_bloqueados.append((jugador, motivo))

    # --- Mostrar pases disponibles ---
    if pases_validos:
        print(f"  PASES DISPONIBLES ({len(pases_validos)}):")
        for jugador in pases_validos:
            dist = abs(jugador["fila"] - portador["fila"]) + abs(jugador["columna"] - portador["columna"])
            direccion = "horizontal" if jugador["fila"] == portador["fila"] else "vertical"
            print(f"    [OK] -> {jugador['nombre']} ({jugador['rol']}) "
                  f"en ({jugador['fila']}, {jugador['columna']}) "
                  f"| {direccion} | distancia {dist}")
    else:
        print("  PASES DISPONIBLES: ninguno.")

    # --- Mostrar pases bloqueados con motivo ---
    if pases_bloqueados:
        print()
        print(f"  PASES BLOQUEADOS ({len(pases_bloqueados)}):")
        for jugador, motivo in pases_bloqueados:
            print(f"    [--] {jugador['nombre']} ({jugador['rol']}) "
                  f"en ({jugador['fila']}, {jugador['columna']}) "
                  f"| bloqueado por: {motivo}")

    # --- Companeros sin linea directa ---
    if companeros_sin_linea:
        print()
        print(f"  COMPANEROS SIN LINEA DIRECTA ({len(companeros_sin_linea)}):")
        for jugador in companeros_sin_linea:
            print(f"    [..] {jugador['nombre']} ({jugador['rol']}) "
                  f"en ({jugador['fila']}, {jugador['columna']}) "
                  f"| no esta en la misma fila ni columna")

    # --- Sugerencia de movimiento si no hay pases ---
    if not pases_validos:
        print()
        print("  SUGERENCIA: No hay pases directos disponibles.")
        print("  Podrias mover al portador para alinearlo con un companero:")
        equipo_rival = "B" if equipo_portador == "A" else "A"
        sugerencias = []
        for jugador in companeros_sin_linea:
            # Verificar si alinearse en la fila del companero es posible
            delta_fila = jugador["fila"] - portador["fila"]
            if delta_fila != 0:
                dir_fila = "abajo" if delta_fila > 0 else "arriba"
                sugerencias.append(
                    f"    Mover a {portador['nombre']} {dir_fila} para alinearse "
                    f"con {jugador['nombre']} en fila {jugador['fila']}"
                )
            delta_col = jugador["columna"] - portador["columna"]
            if delta_col != 0:
                dir_col = "derecha" if delta_col > 0 else "izquierda"
                sugerencias.append(
                    f"    Mover a {portador['nombre']} {dir_col} para alinearse "
                    f"con {jugador['nombre']} en columna {jugador['columna']}"
                )
        if sugerencias:
            for s in sugerencias[:3]:   # Mostrar hasta 3 sugerencias para no saturar
                print(s)
        else:
            print("    No se encontraron sugerencias de movimiento disponibles.")


def detectar_camino_arco(cancha, jugadores, arbitro):
    """
    Para cada delantero en la cancha, verifica si tiene camino libre al arco rival.

    Condiciones para camino libre:
        - El delantero debe estar en la mitad ofensiva (Argentina: cols 30-59, Brasil: cols 0-29).
        - No debe haber rivales, obstaculos 'X', arbitro 'R' ni su sombra entre el
          delantero y el arco rival en la misma fila.
        - Jugadores del mismo equipo no bloquean el camino.

    Args:
        cancha: La matriz de la cancha.
        jugadores: Lista de jugadores en la cancha.
        arbitro: Posicion del arbitro para calcular su sombra.
    """
    delanteros = [jugador for jugador in jugadores if jugador["rol"] == "delantero"]
    if not delanteros:
        print("  No hay delanteros en el campo.")
        return

    sombra = _celdas_sombra_arbitro(arbitro)
    print("\n  Analisis de camino al arco:")

    for delantero in delanteros:
        equipo = delantero["equipo"]
        fila_delantero = delantero["fila"]
        col_delantero = delantero["columna"]

        if equipo == "A":
            en_mitad_ofensiva = col_delantero >= 30
            col_arco_rival = 59
            columnas_al_arco = range(col_delantero + 1, col_arco_rival)
        else:
            en_mitad_ofensiva = col_delantero <= 29
            col_arco_rival = 0
            columnas_al_arco = range(col_delantero - 1, col_arco_rival, -1)

        if not en_mitad_ofensiva:
            print(f"  {delantero['nombre']} ({equipo}): NO esta en la mitad ofensiva (col={col_delantero}).")
            continue

        equipo_rival = "B" if equipo == "A" else "A"
        camino_libre = True

        for col_intermedia in columnas_al_arco:
            if (fila_delantero, col_intermedia) in sombra:
                camino_libre = False
                break
            celda = cancha[fila_delantero][col_intermedia]
            if celda == "X" or celda == "R" or celda == equipo_rival:
                camino_libre = False
                break

        if camino_libre:
            print(f"  {delantero['nombre']} ({equipo}, col={col_delantero}): CAMINO LIBRE al arco rival (col={col_arco_rival}).")
        else:
            print(f"  {delantero['nombre']} ({equipo}, col={col_delantero}): camino BLOQUEADO al arco rival.")


def mostrar_cancha_completa(cancha, arbitro, jugadores):
    """
    Muestra la cancha completa (40 filas x 60 columnas) en consola.
    Incluye los arcos de cada equipo en las columnas 0 (Argentina) y 59 (Brasil),
    representados como '|' en las filas centrales del arco (filas 15 a 24).
    Debajo de la cancha se imprime una leyenda con todos los jugadores.

    Args:
        cancha: La matriz de la cancha.
        arbitro: Posicion del arbitro.
        jugadores: Lista de todos los jugadores para la leyenda.
    """
    # Filas que forman el arco (zona central vertical de la cancha)
    FILAS_ARCO_INICIO = 15
    FILAS_ARCO_FIN = 24

    print("\n  === CANCHA COMPLETA ===")
    print()

    # Encabezado: decenas de columna
    print("      " + "".join(str(col // 10) for col in range(60)))
    # Encabezado: unidades de columna
    print("      " + "".join(str(col % 10) for col in range(60)))
    print("      " + "-" * 60)

    for fila in range(40):
        fila_str = f"{fila:>3} |"
        for col in range(60):
            # Dibujar postes del arco de Argentina (columna 0) y Brasil (columna 59)
            if col == 0 and FILAS_ARCO_INICIO <= fila <= FILAS_ARCO_FIN:
                fila_str += "|"
            elif col == 59 and FILAS_ARCO_INICIO <= fila <= FILAS_ARCO_FIN:
                fila_str += "|"
            else:
                fila_str += cancha[fila][col]
        print(fila_str)

    print("      " + "-" * 60)

    # Referencias de los arcos
    print(f"  Arco Argentina (A): columna 0  | filas {FILAS_ARCO_INICIO}-{FILAS_ARCO_FIN}")
    print(f"  Arco Brasil    (B): columna 59 | filas {FILAS_ARCO_INICIO}-{FILAS_ARCO_FIN}")

    # Leyenda completa de jugadores
    print()
    print(f"  {'Equipo':<8} {'Nombre':<16} {'Fila':>4} {'Col':>4}  {'Rol':<16} {'Pelota'}")
    print("  " + "-" * 60)
    for jugador in jugadores:
        indicador_pelota = "[*]" if jugador["tiene_pelota"] else ""
        print(
            f"  {jugador['equipo']:<8} {jugador['nombre']:<16}"
            f" {jugador['fila']:>4} {jugador['columna']:>4}  "
            f"{jugador['rol']:<16} {indicador_pelota}"
        )
    if arbitro:
        print(f"  {'R':<8} {'Arbitro':<16} {arbitro['fila']:>4} {arbitro['columna']:>4}")


# Posiciones fijas de obstaculos en la cancha (fila, columna)
OBSTACULOS = [(5, 25), (25, 25), (15, 35)]


def inicializar():
    """
    Construye el estado inicial de la partida: cancha, jugadores hardcodeados y arbitro.
    Posiciona todos los jugadores de Argentina y Brasil segun el enunciado,
    marca los obstaculos fijos y coloca al arbitro cerca del portador inicial.

    Returns:
        (cancha, jugadores, arbitro) con el estado inicial completo.
    """
    cancha = crear_cancha()
    jugadores = []

    # Marcar obstaculos fijos en la matriz
    for obs_fila, obs_col in OBSTACULOS:
        cancha[obs_fila][obs_col] = "X"

    # Jugadores de Argentina
    jugadores_argentina = [
        {"nombre": "Martinez",    "equipo": "A", "fila": 20, "columna":  5, "rol": "arquero",       "tiene_pelota": False},
        {"nombre": "Romero",      "equipo": "A", "fila": 10, "columna": 15, "rol": "defensor",      "tiene_pelota": False},
        {"nombre": "Mac Allister","equipo": "A", "fila": 20, "columna": 25, "rol": "mediocampista", "tiene_pelota": True},
        {"nombre": "Lautaro",     "equipo": "A", "fila": 20, "columna": 45, "rol": "delantero",     "tiene_pelota": False},
        {"nombre": "Di Maria",    "equipo": "A", "fila": 30, "columna": 40, "rol": "delantero",     "tiene_pelota": False},
    ]

    # Jugadores de Brasil
    jugadores_brasil = [
        {"nombre": "Alisson",  "equipo": "B", "fila": 20, "columna": 54, "rol": "arquero",       "tiene_pelota": False},
        {"nombre": "Silva",    "equipo": "B", "fila": 15, "columna": 42, "rol": "defensor",      "tiene_pelota": False},
        {"nombre": "Rodrygo",  "equipo": "B", "fila": 20, "columna": 35, "rol": "mediocampista", "tiene_pelota": False},
        {"nombre": "Vinicius", "equipo": "B", "fila": 10, "columna": 20, "rol": "delantero",     "tiene_pelota": False},
    ]

    for jugador in jugadores_argentina + jugadores_brasil:
        posicionar_jugador(cancha, jugadores, jugador)

    # Colocar arbitro cerca del portador inicial
    portador_inicial = _jugador_con_pelota(jugadores)
    arbitro = {
        "fila": portador_inicial["fila"] - 2,
        "columna": portador_inicial["columna"] + 2,
    }
    cancha[arbitro["fila"]][arbitro["columna"]] = "R"

    return cancha, jugadores, arbitro


# ─────────────────────────────────────────────
#  MENU PRINCIPAL
# ─────────────────────────────────────────────
def menu():
    """
    Punto de entrada del programa. Muestra el menu interactivo y delega cada opcion
    a la funcion correspondiente. El bucle continua hasta que el usuario elija salir.
    """
    print("\n" + "=" * 40)
    print("   Desafio 3 - Cancha Inteligente - ")
    print("   Copa de Algoritmia UADE 2026 -")
    print("=" * 40)

    cancha, jugadores, arbitro = inicializar()
    print("\n  Cancha inicializada correctamente.\n")

    while True:
        print("\n" + "-" * 40)
        print("  MENU PRINCIPAL")
        print("-" * 40)
        print("  1. Ver cancha completa")
        print("  2. Agregar jugador")
        print("  3. Mover jugador")
        print("  4. Calcular distancias a la pelota")
        print("  5. Detectar pases posibles")
        print("  6. Detectar camino libre al arco")
        print("  7. Salir")
        print("-" * 40)

        opcion = input("  Opcion: ").strip()

        if opcion == "1":
            mostrar_cancha_completa(cancha, arbitro, jugadores)

        elif opcion == "2":
            print("\n  === AGREGAR JUGADOR ===")

            # --- Nombre: solo letras y espacios, no vacio, no duplicado ---
            nombre = ""
            while True:
                nombre = input("  Nombre (solo letras): ").strip()
                if not nombre:
                    print("  Error: El nombre no puede estar vacio.")
                elif not all(caracter.isalpha() or caracter == " " for caracter in nombre):
                    print("  Error: El nombre solo puede contener letras y espacios, sin numeros ni simbolos.")
                else:
                    break

            # --- Equipo: solo A o B ---
            equipo = ""
            while True:
                equipo = input("  Equipo (A o B): ").strip().upper()
                if equipo == "A" or equipo == "B":
                    break
                print("  Error: El equipo debe ser A o B, sin numeros ni otras palabras.")

            # --- Fila: solo numeros enteros en rango 0-39 ---
            fila = -1
            while True:
                entrada_fila = input("  Fila (0-39): ").strip()
                if not entrada_fila.isdigit():
                    print("  Error: La fila debe ser un numero entero positivo, sin letras.")
                elif not (0 <= int(entrada_fila) <= 39):
                    print("  Error: La fila debe estar entre 0 y 39.")
                else:
                    fila = int(entrada_fila)
                    break

            # --- Columna: solo numeros enteros en rango 0-59 ---
            columna = -1
            while True:
                entrada_columna = input("  Columna (0-59): ").strip()
                if not entrada_columna.isdigit():
                    print("  Error: La columna debe ser un numero entero positivo, sin letras.")
                elif not (0 <= int(entrada_columna) <= 59):
                    print("  Error: La columna debe estar entre 0 y 59.")
                else:
                    columna = int(entrada_columna)
                    break

            # --- Rol: seleccion por numero ---
            MENU_ROLES = {
                "1": "arquero",
                "2": "defensor",
                "3": "mediocampista",
                "4": "delantero",
            }
            print(" Rol:")
            print("  1. Arquero")
            print("  2. Defensor")
            print("  3. Mediocampista")
            print("  4. Delantero")
            rol = ""
            while True:
                opcion_rol = input("  Seleccione el numero del rol (1-4): ").strip()
                if opcion_rol in MENU_ROLES:
                    rol = MENU_ROLES[opcion_rol]
                    break
                print("  Error: Ingrese 1, 2, 3 o 4 para seleccionar el rol.")

            # --- Pelota ---
            respuesta_pelota = input("  Tiene pelota? (s/n): ").strip().lower()
            tiene_pelota = respuesta_pelota == "s"

            nuevo_jugador = {
                "nombre": nombre,
                "equipo": equipo,
                "fila": fila,
                "columna": columna,
                "rol": rol,
                "tiene_pelota": tiene_pelota,
            }
            posicionar_jugador(cancha, jugadores, nuevo_jugador, arbitro)

        elif opcion == "3":
            print("\n  === MOVER JUGADOR ===")

            # --- Mostrar lista de jugadores de ambos equipos ---
            jugadores_arg = [j for j in jugadores if j["equipo"] == "A"]
            jugadores_bra = [j for j in jugadores if j["equipo"] == "B"]

            print()
            print(f"  {'#':<4} {'Equipo':<8} {'Nombre':<16} {'Fila':>4} {'Col':>4}  {'Rol'}")
            print("  " + "-" * 52)

            nombres_validos = []
            contador = 1
            for jugador in jugadores_arg:
                indicador = " [*]" if jugador["tiene_pelota"] else ""
                print(
                    f"  {contador:<4} {'Argentina':<8} {jugador['nombre']:<16}"
                    f" {jugador['fila']:>4} {jugador['columna']:>4}  {jugador['rol']}{indicador}"
                )
                nombres_validos.append(jugador["nombre"].lower())
                contador += 1

            print("  " + "-" * 52)
            for jugador in jugadores_bra:
                indicador = " [*]" if jugador["tiene_pelota"] else ""
                print(
                    f"  {contador:<4} {'Brasil':<8} {jugador['nombre']:<16}"
                    f" {jugador['fila']:>4} {jugador['columna']:>4}  {jugador['rol']}{indicador}"
                )
                nombres_validos.append(jugador["nombre"].lower())
                contador += 1

            print()

            # --- Nombre: solo letras/espacios y debe estar en la lista ---
            nombre_jugador = ""
            while True:
                nombre_jugador = input("  Nombre del jugador a mover: ").strip()
                if not nombre_jugador:
                    print("  Error: El nombre no puede estar vacio.")
                elif not all(caracter.isalpha() or caracter == " " for caracter in nombre_jugador):
                    print("  Error: El nombre solo puede contener letras y espacios, sin numeros ni simbolos.")
                elif nombre_jugador.lower() not in nombres_validos:
                    print(f"  Error: '{nombre_jugador}' no esta en la lista de jugadores.")
                else:
                    break

            # --- Direccion ---
            print("Direccion:")
            print("  1. Arriba")
            print("  2. Abajo")
            print("  3. Izquierda")
            print("  4. Derecha")
            MENU_DIRECCIONES = {"1": "arriba", "2": "abajo", "3": "izquierda", "4": "derecha"}
            while True:
                opcion_dir = input("  Seleccione el numero de la direccion (1-4): ").strip()
                if opcion_dir in MENU_DIRECCIONES:
                    direccion = MENU_DIRECCIONES[opcion_dir]
                    break
                print("  Error: Ingrese 1, 2, 3 o 4 para seleccionar la direccion.")

            mover_jugador(cancha, jugadores, nombre_jugador, direccion, arbitro)
        elif opcion == "4":
            calcular_distancias(jugadores)
        elif opcion == "5":
            detectar_pases(cancha, jugadores, arbitro)
        elif opcion == "6":
            detectar_camino_arco(cancha, jugadores, arbitro)
        elif opcion == "7":
            print("\n  Hasta la proxima!\n")
            break
        else:
            print("  Opcion invalida. Ingrese un numero del 1 al 7.")
            

if __name__ == "__main__":
    menu()