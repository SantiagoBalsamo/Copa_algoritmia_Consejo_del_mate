# --- Copa algoritmia 2026 --- Desafio 3 ---

# Constantes 
FILAS           = 100
COLUMNAS        = 60
EQUIPOS_VALIDOS = ("A", "B")
ROLES_VALIDOS   = ("arquero", "defensor", "mediocampista", "delantero")
RIVAL           = {"A": "B", "B": "A"}
CONFIG_EQUIPOS  = {
    "A": {"mitad": (30, 59), "arco": 59},
    "B": {"mitad": (0,  29), "arco": 0},
}

# FUNCIONES

def crear_cancha():
    """Crea e inicializa la cancha de juego.

    Returns:
        Matriz de 100 filas × 60 columnas inicializada con '.'.
    """
    cancha = []
    for _ in range(FILAS):
        fila = []
        for _ in range(COLUMNAS):
            fila.append(".")
        cancha.append(fila)
    return cancha


def posicionar_jugador(
    cancha,
    jugadores,
    nombre,
    equipo,
    fila,
    columna,
    rol,
    tiene_pelota
):
    """Valida y agrega un jugador a la cancha y a la lista de jugadores.

    Args:
        cancha: Matriz que representa la cancha.
        jugadores: Lista de jugadores registrados.
        nombre: Nombre del jugador.
        equipo: Equipo del jugador ('A' o 'B').
        fila: Fila donde se posiciona (0-99).
        columna: Columna donde se posiciona (0-59).
        rol: Rol del jugador (arquero, defensor, mediocampista, delantero).
        tiene_pelota: True si el jugador inicia con la pelota.

    Returns:
        True si el jugador fue registrado correctamente, False en caso contrario.
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
    """Mueve un jugador una celda en la dirección indicada.

    Valida que el movimiento no salga de los límites, no ingrese
    a una zona bloqueada ni a una celda ocupada por otro jugador.

    Args:
        cancha: Matriz que representa la cancha.
        jugador: Diccionario con los datos del jugador a mover.
        direccion: 'arriba', 'abajo', 'izquierda' o 'derecha'.

    Returns:
        True si el movimiento fue exitoso, False si fue inválido.
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

    celda_destino  = cancha[nueva_fila][nueva_columna]
    mensajes_error = {
        "X": "zona bloqueada",
        "A": "celda ocupada por otro jugador",
        "B": "celda ocupada por otro jugador",
    }

    if celda_destino in mensajes_error:
        print(f"  MOVIMIENTO INVÁLIDO: '{jugador['nombre']}' no puede moverse hacia {direccion} "
              f"({mensajes_error[celda_destino]}).")
        return False

    cancha[jugador["fila"]][jugador["columna"]] = "."
    cancha[nueva_fila][nueva_columna] = jugador["equipo"]
    jugador["fila"]    = nueva_fila
    jugador["columna"] = nueva_columna

    print(f"  MOVIMIENTO OK: '{jugador['nombre']}' se movió {direccion} → ({nueva_fila}, {nueva_columna}).")
    return True


def buscar_portador(jugadores):
    """Busca y retorna el jugador que tiene la pelota.

    Args:
        jugadores: Lista de jugadores registrados.

    Returns:
        Diccionario del jugador con la pelota, o None si ninguno la tiene.
    """
    for j in jugadores:
        if j["tiene_pelota"]:
            return j
    return None


def buscar_jugador(jugadores, nombre):
    """Busca un jugador por nombre en la lista de jugadores.

    Args:
        jugadores: Lista de jugadores registrados.
        nombre: Nombre del jugador a buscar.

    Returns:
        Diccionario del jugador encontrado, o None si no existe.
    """
    for j in jugadores:
        if j["nombre"] == nombre:
            return j
    return None


def pedir_entero(mensaje, minimo, maximo):
    """Solicita al usuario un número entero dentro de un rango válido.

    Repite la solicitud hasta recibir un valor correcto.

    Args:
        mensaje: Texto que se muestra al usuario.
        minimo: Valor mínimo aceptado (inclusivo).
        maximo: Valor máximo aceptado (inclusivo).

    Returns:
        Entero válido ingresado por el usuario.
    """
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"  Por favor ingrese un número entre {minimo} y {maximo}.")
        except ValueError:
            print("  Por favor ingrese un número entero válido.")


def calcular_distancias(jugadores):
    """Calcula y muestra la distancia Manhattan de cada jugador al portador.

    Identifica al jugador más cercano. En caso de empate,
    muestra todos los jugadores empatados.

    Args:
        jugadores: Lista de jugadores registrados.

    Returns:
        None
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


def hay_bloqueo(
    cancha,
    fila1,
    col1,
    fila2,
    col2,
    equipo_rival
):
    """Verifica si hay un rival o obstáculo entre dos posiciones en línea recta.

    Solo analiza recorridos horizontales o verticales, nunca diagonales.
    Los jugadores del mismo equipo no se consideran bloqueo.

    Args:
        cancha: Matriz que representa la cancha.
        fila1: Fila de la posición origen.
        col1: Columna de la posición origen.
        fila2: Fila de la posición destino.
        col2: Columna de la posición destino.
        equipo_rival: Símbolo del equipo rival ('A' o 'B').

    Returns:
        True si el camino está bloqueado, False si está libre.
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
    """Lista todos los pases posibles para el jugador que posee la pelota.

    Un pase es válido si el receptor es del mismo equipo, está en la
    misma fila o columna, y no hay rivales ni obstáculos entre ellos.

    Args:
        cancha: Matriz que representa la cancha.
        jugadores: Lista de jugadores registrados.

    Returns:
        None
    """
    portador = buscar_portador(jugadores)

    if portador is None:
        print("  ERROR: Ningún jugador tiene la pelota.")
        return

    equipo_rival = RIVAL[portador["equipo"]]

    print(f"\n  ── Pases posibles para '{portador['nombre']}' ──")

    hay_pases = False
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
            hay_pases = True
            print(f"  PASE POSIBLE:   '{portador['nombre']}' → '{j['nombre']}'.")

    if not hay_pases:
        print("  No hay pases posibles disponibles.")


def detectar_camino_libre(cancha, jugadores):
    """Detecta qué delanteros tienen camino libre al arco rival.

    Un delantero tiene camino libre si está en la mitad ofensiva
    y no hay rivales ni obstáculos entre él y el arco en su misma fila.
    Los compañeros de equipo no bloquean el camino.

    Args:
        cancha: Matriz que representa la cancha.
        jugadores: Lista de jugadores registrados.

    Returns:
        None
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
        rival   = RIVAL[equipo]

        col_inicio, col_fin = CONFIG_EQUIPOS[equipo]["mitad"]
        col_arco_rival      = CONFIG_EQUIPOS[equipo]["arco"]
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
    """Muestra una vista parcial de la cancha por consola.

    Imprime las primeras 15 filas y 30 columnas con índices
    para facilitar la ubicación visual de los jugadores.

    Args:
        cancha: Matriz que representa la cancha.

    Returns:
        None
    """
    filas_mostrar = 15
    cols_mostrar  = 30
    print(f"\n  ── Vista parcial de la cancha "
          f"(primeras {filas_mostrar} filas × {cols_mostrar} columnas) ──")
    print("     " + "".join(str(c % 10) for c in range(cols_mostrar)))
    for f in range(filas_mostrar):
        print(f"  {f:2d} " + "".join(cancha[f][c] for c in range(cols_mostrar)))
    print()


def mostrar_menu():
    """Imprime el menú principal de opciones por consola.

    Returns:
        None
    """
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


def menu_agregar_jugador(cancha, jugadores):
    """Solicita los datos al usuario y agrega un nuevo jugador a la cancha.

    Args:
        cancha: Matriz que representa la cancha.
        jugadores: Lista de jugadores registrados.

    Returns:
        None
    """
    print("\n  ── Agregar jugador ──")
    nombre = input("  Nombre: ").strip()
    if not nombre:
        print("  ERROR: El nombre no puede estar vacío.")
        return

    equipo  = input("  Equipo (A/B): ").strip().upper()
    fila    = pedir_entero("  Fila (0-99): ", 0, 99)
    columna = pedir_entero("  Columna (0-59): ", 0, 59)

    print("  Roles disponibles: arquero, defensor, mediocampista, delantero")
    rol = input("  Rol: ").strip().lower()

    respuesta    = input("  ¿Tiene la pelota? (s/n): ").strip().lower()
    tiene_pelota = respuesta == "s"

    posicionar_jugador(cancha, jugadores, nombre, equipo, fila, columna, rol, tiene_pelota)


def menu_mover_jugador(cancha, jugadores):
    """Solicita el nombre y dirección al usuario y mueve al jugador indicado.

    Args:
        cancha: Matriz que representa la cancha.
        jugadores: Lista de jugadores registrados.

    Returns:
        None
    """
    print("\n  ── Mover jugador ──")
    if not jugadores:
        print("  ERROR: No hay jugadores en la cancha.")
        return

    nombre  = input("  Nombre del jugador a mover: ").strip()

    if not nombre:
        print("  ERROR: El nombre no puede estar vacío.")
        return

    jugador = buscar_jugador(jugadores, nombre)

    if jugador is None:
        print(f"  ERROR: No se encontró al jugador '{nombre}'.")
        return

    print("  Direcciones válidas: arriba, abajo, izquierda, derecha")
    direccion = input("  Dirección: ").strip().lower()

    if not direccion:
        print("  ERROR: La dirección no puede estar vacía.")
        return

    mover_jugador(cancha, jugador, direccion)


def menu_agregar_obstaculo(cancha):
    """Solicita una posición al usuario y coloca un obstáculo en la cancha.

    Args:
        cancha: Matriz que representa la cancha.

    Returns:
        None
    """
    print("\n  ── Agregar obstáculo ──")
    fila    = pedir_entero("  Fila (0-99): ", 0, 99)
    columna = pedir_entero("  Columna (0-59): ", 0, 59)

    if cancha[fila][columna] != ".":
        print(f"  ERROR: La celda ({fila}, {columna}) ya está ocupada.")
    else:
        cancha[fila][columna] = "X"
        print(f"  OK: Obstáculo colocado en ({fila}, {columna}).")



#  PROGRAMA PRINCIPAL

def ejecutar_casos_prueba(cancha, jugadores):
    """Ejecuta un conjunto de casos mínimos requeridos por la consigna.

    Demuestra todas las situaciones pedidas: movimientos válidos e inválidos,
    pases posibles y bloqueados, distancias Manhattan, camino libre al arco
    y control de posesión única de la pelota.

    Args:
        cancha: Matriz que representa la cancha.
        jugadores: Lista de jugadores registrados.

    Returns:
        None
    """
    separador = "=" * 50

    print(f"\n{separador}")
    print("  CASOS DE PRUEBA MÍNIMOS")
    print(separador)

    # Obstáculo 
    cancha[10][15] = "X"
    print("\n  Obstáculo 'X' colocado en (10, 15).")

    # Posicionar jugadores 
    print(f"\n{separador}")
    print("  [TAREA 2] Posicionando jugadores")
    print(separador)

    # Casos válidos
    posicionar_jugador(cancha, jugadores, "Messi",       "A", 10, 10, "delantero",     True)
    posicionar_jugador(cancha, jugadores, "Di Maria",    "A", 10, 12, "mediocampista", False)
    posicionar_jugador(cancha, jugadores, "Mac Allister","A",  5, 10, "mediocampista", False)
    posicionar_jugador(cancha, jugadores, "Alvarez",     "A", 40, 40, "delantero",     False)
    posicionar_jugador(cancha, jugadores, "Romero",      "A", 20,  5, "defensor",      False)
    posicionar_jugador(cancha, jugadores, "Dybala",      "A", 60, 20, "delantero",     False)
    posicionar_jugador(cancha, jugadores, "Vinicius",    "B", 10, 20, "delantero",     False)
    posicionar_jugador(cancha, jugadores, "Rodrygo",     "B", 15, 12, "mediocampista", False)
    posicionar_jugador(cancha, jugadores, "Endrick",     "B", 50, 10, "delantero",     False)
    posicionar_jugador(cancha, jugadores, "Paqueta",     "B",  8, 18, "delantero",     False)

    # Casos de error
    print("\n  -- Errores esperados --")
    posicionar_jugador(cancha, jugadores, "Error1", "A", 10, 10, "delantero",      False)  
    posicionar_jugador(cancha, jugadores, "Error2", "C",  5,  5, "defensor",       False)  
    posicionar_jugador(cancha, jugadores, "Error3", "A", 200, 5, "defensor",       False)  
    posicionar_jugador(cancha, jugadores, "Error4", "B", 30, 30, "centrocampista", False)  
    posicionar_jugador(cancha, jugadores, "Error5", "A",  7,  7, "arquero",        True)   

    #  Movimientos 
    print(f"\n{separador}")
    print("  [TAREA 3] Movimientos de jugadores")
    print(separador)

    messi = buscar_jugador(jugadores, "Messi")

    # Movimiento válido
    mover_jugador(cancha, messi, "derecha")

    # Movimiento inválido: celda ocupada (Di Maria en col 12)
    mover_jugador(cancha, messi, "derecha")

    # Movimiento inválido: zona bloqueada (obstáculo en col 15)
    mover_jugador(cancha, messi, "abajo")
    mover_jugador(cancha, messi, "derecha")
    mover_jugador(cancha, messi, "derecha")
    mover_jugador(cancha, messi, "derecha")

    # Movimiento inválido: fuera de la cancha
    arquero = {"nombre": "Arquero", "equipo": "A",
               "fila": 0, "columna": 0, "rol": "arquero", "tiene_pelota": False}
    jugadores.append(arquero)
    cancha[0][0] = "A"
    mover_jugador(cancha, arquero, "arriba")
    mover_jugador(cancha, arquero, "izquierda")

    # Distancias Manhattan 
    print(f"\n{separador}")
    print("  [TAREA 4] Distancias Manhattan a la pelota")
    print(separador)
    calcular_distancias(jugadores)

    print(f"\n{separador}")
    print("  [TAREA 5] Detectar pases posibles")
    print(separador)

    detectar_pases(cancha, jugadores)

    print(f"\n{separador}")
    print("  [TAREA 6] Camino libre al arco")
    print(separador)

    detectar_camino_libre(cancha, jugadores)

    print(f"\n{separador}")
    print("  Fin de los casos de prueba.")
    print(separador)


def main():
    """Punto de entrada del programa.

    Inicializa la cancha y ejecuta el menú principal
    hasta que el usuario elija salir.

    Returns:
        None
    """
    print("=" * 50)
    print("  Copa UADE 2026 – Desafío 3")
    print("  La Cancha Inteligente")
    print("=" * 50)

    cancha    = crear_cancha()
    jugadores = []
    print("\n  Cancha 100×60 creada correctamente.")

    # Ejecuta casos de prueba mínimos 
    respuesta = input("\n  ¿Desea ejecutar los casos de prueba mínimos? (s/n): ").strip().lower()
    if respuesta == "s":
        ejecutar_casos_prueba(cancha, jugadores)

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