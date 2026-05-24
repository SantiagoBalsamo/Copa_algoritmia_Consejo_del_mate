# DESAFÍO 3: "LA CANCHA INTELIGENTE"
# Copa de Algoritmia y Programación - UADE 2026

FILAS = 100
COLUMNAS = 60
EQUIPOS_VALIDOS = ("A", "B")
ROLES_VALIDOS = ("arquero", "defensor", "mediocampista", "delantero")

# TAREA 1: CREAR LA CANCHA
def crear_cancha():
    """Genera la matriz que representa la cancha de fútbol.

    Crea una matriz de 100 filas por 60 columnas inicializada con puntos,
    donde cada punto representa una posición vacía.

    Returns:
        Matriz de 100x60 inicializada con ".".
    """
    cancha = [["." for _ in range(COLUMNAS)] for _ in range(FILAS)]
    return cancha


# TAREA 2: POSICIONAR JUGADORES
def posicionar_jugador(cancha, jugadores, jugador):
    """Agrega un jugador a la cancha validando todas las condiciones requeridas.

    Valida en orden:
        - Que el nombre no esté duplicado.
        - Que la posición esté dentro de los límites de la cancha.
        - Que la celda destino no tenga obstáculo ni otro jugador.
        - Que tiene_pelota sea estrictamente booleano.
        - Que el equipo y el rol sean válidos.
        - Que ningún otro jugador ya posea la pelota.

    Si todo es correcto, actualiza la matriz y agrega el jugador a la lista.

    Args:
        cancha (list[list[str]]): Matriz 100x60 que representa la cancha.
        jugadores (list[dict]): Lista de jugadores ya registrados.
        jugador (dict): Diccionario con los datos del jugador a agregar.
            Debe contener: nombre (str), equipo (str), fila (int),
            columna (int), rol (str), tiene_pelota (bool).

    Returns:
        bool: True si el jugador fue agregado correctamente, False en caso contrario.
    """
    
    nombre = jugador["nombre"]
    equipo = jugador["equipo"]
    fila = jugador["fila"]
    columna = jugador["columna"]
    rol = jugador["rol"]
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

    # Validar que la celda no tenga un obstáculo
    if cancha[fila][columna] == "X":
        print(f"[ERROR] No se pudo agregar a {nombre}: la celda ({fila}, {columna}) "
              f"contiene un obstáculo (X).")
        return False

    # Validar que la celda no esté ocupada por otro jugador
    if cancha[fila][columna] in ("A", "B"):
        print(f"[ERROR] No se pudo agregar a {nombre}: la celda ({fila}, {columna}) "
              f"ya está ocupada por otro jugador.")
        return False

    # Validar tipo booleano de tiene_pelota
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
          f"{'[TIENE LA PELOTA]' if tiene_pelota else ''}.")
    return True

# TAREA 3: MOVER JUGADORES
def mover_jugador(cancha, jugadores, nombre, direccion):
    """Mueve un jugador una celda en la dirección indicada.

    Valida que el movimiento no salga de la cancha, no pise a otro jugador
    ni una zona bloqueada. Actualiza la posición del jugador y la matriz.

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
    col_actual = jugador["columna"]

    # Calcular nueva posición según la dirección
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
    nueva_col = col_actual + delta_col

    # Validar límites de la cancha
    if nueva_fila < 0 or nueva_fila >= FILAS or nueva_col < 0 or nueva_col >= COLUMNAS:
        print(f"[MOVIMIENTO INVÁLIDO] {nombre} no puede moverse hacia {direccion}: "
              f"fuera de la cancha.")
        return False

    # Validar que la celda destino no esté ocupada
    celda_destino = cancha[nueva_fila][nueva_col]
    if celda_destino == "X":
        print(f"[MOVIMIENTO INVÁLIDO] {nombre} no puede moverse hacia {direccion}: "
              f"zona bloqueada (X) en ({nueva_fila}, {nueva_col}).")
        return False

    if celda_destino in ("A", "B"):
        print(f"[MOVIMIENTO INVÁLIDO] {nombre} no puede moverse hacia {direccion}: "
              f"celda ({nueva_fila}, {nueva_col}) ocupada por otro jugador.")
        return False

    # Actualizar matriz y posición del jugador
    cancha[fila_actual][col_actual] = "."
    cancha[nueva_fila][nueva_col] = jugador["equipo"]
    jugador["fila"] = nueva_fila
    jugador["columna"] = nueva_col

    print(f"[MOVIMIENTO OK] {nombre} se movió hacia {direccion}: "
          f"({fila_actual}, {col_actual}) → ({nueva_fila}, {nueva_col}).")
    return True

# TAREA 4: CALCULAR DISTANCIA A LA PELOTA
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

    print(f"\nDistancias Manhattan respecto a {portador['nombre']} "
          f"(pelota en ({portador['fila']}, {portador['columna']}))")

    distancias = []
    for jugador in jugadores:
        if jugador["nombre"] == portador["nombre"]:
            continue
        distancia = (abs(jugador["fila"] - portador["fila"]) +
                     abs(jugador["columna"] - portador["columna"]))
        distancias.append((jugador, distancia))
        print(f"  {jugador['nombre']} ({jugador['equipo']}): distancia = {distancia}")

    if not distancias:
        print("No hay otros jugadores en la cancha.")
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


# TAREA 5: DETECTAR POSIBILIDAD DE PASE
def detectar_pases(cancha, jugadores):
    """Lista todos los pases posibles para el jugador que posee la pelota.

    Un pase es válido si ambos jugadores son del mismo equipo, están en la
    misma fila o columna, y no hay rivales ni obstáculos entre ellos.
    Los jugadores del mismo equipo no bloquean el pase.

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

    print(f"\nPases posibles para {portador['nombre']} "
          f"en ({portador['fila']}, {portador['columna']})")

    pases_posibles = []
    equipo_rival = "B" if portador["equipo"] == "A" else "A"

    for jugador in jugadores:
        # No se pasa a sí mismo ni a rivales
        if jugador["nombre"] == portador["nombre"]:
            continue
        if jugador["equipo"] != portador["equipo"]:
            continue

        misma_fila = jugador["fila"] == portador["fila"]
        misma_col = jugador["columna"] == portador["columna"]

        if not misma_fila and not misma_col:
            print(f"[BLOQUEADO] {jugador['nombre']}: no está en línea recta.")
            continue

        # Verificar si hay obstáculos o rivales entre los dos jugadores
        bloqueado = _hay_bloqueo_entre(cancha, portador, jugador, equipo_rival)

        if bloqueado:
            print(f"[BLOQUEADO] Pase a {jugador['nombre']}: hay rival u obstáculo "
                  f"en el camino.")
        else:
            print(f"[PASE POSIBLE] → {jugador['nombre']} "
                  f"en ({jugador['fila']}, {jugador['columna']}).")
            pases_posibles.append(jugador)

    if not pases_posibles:
        print("No hay pases disponibles.")

    return pases_posibles


def _hay_bloqueo_entre(cancha, portador, receptor, equipo_rival):
    """Verifica si existe un rival u obstáculo entre portador y receptor.

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
    fila_p, col_p = portador["fila"], portador["columna"]
    fila_r, col_r = receptor["fila"], receptor["columna"]

    if fila_p == fila_r:
        col_min = min(col_p, col_r) + 1
        col_max = max(col_p, col_r)
        for col in range(col_min, col_max):
            celda = cancha[fila_p][col]
            if celda == "X" or celda == equipo_rival:
                return True
    else:
        fila_min = min(fila_p, fila_r) + 1
        fila_max = max(fila_p, fila_r)
        for fila in range(fila_min, fila_max):
            celda = cancha[fila][col_p]
            if celda == "X" or celda == equipo_rival:
                return True

    return False


# TAREA 6: DETECTAR CAMINO LIBRE AL ARCO
def detectar_camino_libre(cancha, jugadores):
    """Detecta qué delanteros tienen camino libre al arco rival.

    Un delantero tiene camino libre si está en la mitad ofensiva de su equipo
    y no hay rivales ni obstáculos en su misma fila entre él y el arco rival.
    Los compañeros de equipo no bloquean el camino.

    Mitad ofensiva:
        - Argentina (A): columnas 30 a 59.
        - Brasil (B): columnas 0 a 29.

    Args:
        cancha (list[list[str]]): La matriz que representa la cancha.
        jugadores (list[dict]): Lista con todos los jugadores registrados.

    Returns:
        list[dict]: Lista de delanteros con camino libre al arco.
    """
    print("\nDetección de camino libre al arco")

    delanteros_libres = []
    hay_delanteros = False

    for jugador in jugadores:
        if jugador["rol"] != "delantero":
            continue

        hay_delanteros = True
        nombre = jugador["nombre"]
        equipo = jugador["equipo"]
        fila = jugador["fila"]
        columna = jugador["columna"]

        en_mitad_ofensiva = (
            (equipo == "A" and 30 <= columna <= 59) or
            (equipo == "B" and 0 <= columna <= 29)
        )

        if not en_mitad_ofensiva:
            print(f"[SIN CAMINO LIBRE] {nombre}: no está en la mitad ofensiva.")
            continue

        equipo_rival = "B" if equipo == "A" else "A"
        if equipo == "A":
            rango_cols = range(columna + 1, COLUMNAS)
        else:
            rango_cols = range(columna - 1, -1, -1)

        camino_libre = True
        for col in rango_cols:
            celda = cancha[fila][col]
            if celda == "X" or celda == equipo_rival:
                camino_libre = False
                break

        if camino_libre:
            print(f"[CAMINO LIBRE] {nombre} tiene camino libre al arco rival.")
            delanteros_libres.append(jugador)
        else:
            print(f"[SIN CAMINO LIBRE] {nombre}: hay rival u obstáculo en su fila.")

    if not hay_delanteros:
        print("No hay delanteros registrados en la cancha.")

    return delanteros_libres


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
    """Coloca un obstáculo en una posición de la cancha.

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
    """Muestra una sección reducida de la cancha por consola.

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
    print(f"\nVista de la cancha (filas {fila_inicio}-{fila_fin}, "
          f"cols {col_inicio}-{col_fin})")
    for fila in range(fila_inicio, fila_fin + 1):
        fila_str = " ".join(cancha[fila][col_inicio:col_fin + 1])
        print(f"  F{fila:02d}: {fila_str}")


# MAIN: CASOS DE PRUEBA
if __name__ == "__main__":
    print("==============================================")
    print(" DESAFÍO 3: LA CANCHA INTELIGENTE — UADE 2026")
    print("==============================================")
    
    cancha = crear_cancha()
    jugadores = []

    # BLOQUE 1: CREAR CANCHA (tarea 1)
    print("--------------------------------------")
    print("TAREA 1: CREAR LA CANCHA")
    print("--------------------------------------")
    print("\nCancha creada: 100 filas x 60 columnas.")

    # BLOQUE 2: POSICIONAR JUGADORES (Tarea 2)
    print("-----------------------------")
    print("TAREA 2: POSICIONAR JUGADORES")
    print("-----------------------------")
 

    posicionar_jugador(cancha, jugadores, {
        "nombre": "Messi", "equipo": "A", "fila": 50, "columna": 40,
        "rol": "delantero", "tiene_pelota": True
    })
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Di Maria", "equipo": "A", "fila": 50, "columna": 45,
        "rol": "delantero", "tiene_pelota": False
    })
    posicionar_jugador(cancha, jugadores, {
        "nombre": "De Paul", "equipo": "A", "fila": 55, "columna": 40,
        "rol": "mediocampista", "tiene_pelota": False
    })
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Romero", "equipo": "A", "fila": 70, "columna": 20,
        "rol": "defensor", "tiene_pelota": False
    })
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Vinicius", "equipo": "B", "fila": 50, "columna": 43,
        "rol": "delantero", "tiene_pelota": False
    })
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Rodrygo", "equipo": "B", "fila": 60, "columna": 20,
        "rol": "delantero", "tiene_pelota": False
    })
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Casemiro", "equipo": "B", "fila": 55, "columna": 30,
        "rol": "mediocampista", "tiene_pelota": False
    })

    print("\n-- Caso borde: posición fuera de la cancha --")
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Jugador Fantasma", "equipo": "A", "fila": 110, "columna": 5,
        "rol": "defensor", "tiene_pelota": False
    })

    print("\n-- Caso borde: nombre duplicado --")
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Messi", "equipo": "A", "fila": 10, "columna": 10,
        "rol": "delantero", "tiene_pelota": False
    })

    print("\n-- Caso borde: celda con obstáculo (X) --")
    agregar_obstaculo(cancha, 15, 15)
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Lautaro", "equipo": "A", "fila": 15, "columna": 15,
        "rol": "delantero", "tiene_pelota": False
    })

    print("\n-- Caso borde: celda ocupada por jugador --")
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Alvarez", "equipo": "A", "fila": 50, "columna": 40,
        "rol": "delantero", "tiene_pelota": False
    })

    print("\n-- Caso borde: tiene_pelota con tipo inválido --")
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Lautaro", "equipo": "A", "fila": 30, "columna": 30,
        "rol": "delantero", "tiene_pelota": 1
    })
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Lautaro", "equipo": "A", "fila": 30, "columna": 30,
        "rol": "delantero", "tiene_pelota": "True"
    })
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Lautaro", "equipo": "A", "fila": 30, "columna": 30,
        "rol": "delantero", "tiene_pelota": None
    })

    
    print("\nCaso borde: rol inválido")
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Jugador X", "equipo": "A", "fila": 10, "columna": 10,
        "rol": "entrenador", "tiene_pelota": False
    })

    print("\nCaso borde: equipo inválido")
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Jugador Y", "equipo": "C", "fila": 10, "columna": 10,
        "rol": "defensor", "tiene_pelota": False
    })

    print("\nCaso borde: dos jugadores con pelota")
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Alvarez", "equipo": "A", "fila": 48, "columna": 38,
        "rol": "delantero", "tiene_pelota": True  # ya la tiene Messi
    })

    
    # BLOQUE 2: OBSTÁCULOS
    print("AGREGANDO OBSTÁCULOS . . .")
  
    agregar_obstaculo(cancha, 50, 42)
    agregar_obstaculo(cancha, 60, 25)
    mostrar_seccion_cancha(cancha, 49, 61, 18, 50)

    
    # BLOQUE 3: MOVER JUGADORES (Tarea 3)
    print("------------------------")
    print("TAREA 3: MOVER JUGADORES")
    print("------------------------")

    mover_jugador(cancha, jugadores, "De Paul", "arriba")
    mover_jugador(cancha, jugadores, "De Paul", "derecha")

    print("\nCaso borde: movimiento hacia obstáculo")
    mover_jugador(cancha, jugadores, "Messi", "derecha")
    mover_jugador(cancha, jugadores, "Messi", "derecha")

    print("\nCaso borde: movimiento hacia jugador rival")
    mover_jugador(cancha, jugadores, "Vinicius", "derecha")
    mover_jugador(cancha, jugadores, "Vinicius", "derecha")

    print("\nCaso borde: movimiento fuera de la cancha")
    mover_jugador(cancha, jugadores, "Romero", "izquierda")
    mover_jugador(cancha, jugadores, "Romero", "izquierda")
    mover_jugador(cancha, jugadores, "Romero", "izquierda")
    for _ in range(17):
        mover_jugador(cancha, jugadores, "Romero", "izquierda")
    mover_jugador(cancha, jugadores, "Romero", "izquierda")

    mostrar_seccion_cancha(cancha, 49, 57, 38, 50)

    print("--------------------------------------")
    print("TAREA 4: CALCULAR DISTANCIAS MANHATTAN")
    print("--------------------------------------")
    calcular_distancias(jugadores)

    print("--------------------------------")
    print("TAREA 5: DETECTAR PASES POSIBLES")
    print("--------------------------------")
    detectar_pases(cancha, jugadores)

    print("--------------------------------------")
    print("TAREA 6: DETECTAR CAMINO LIBRE AL ARCO")
    print("--------------------------------------")
    detectar_camino_libre(cancha, jugadores)

    print("\nEscenario extra: delantero con camino libre")
    print("---------------------------------------------")
    posicionar_jugador(cancha, jugadores, {
        "nombre": "Alvarez", "equipo": "A", "fila": 10, "columna": 35,
        "rol": "delantero", "tiene_pelota": False
    })
    detectar_camino_libre(cancha, jugadores)

    print("--------------------")
    print("FIN DE LA SIMULACIÓN")
    print("--------------------")