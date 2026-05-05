# ============================================================
# Sistema de Clasificacion FIFA - Copa del Mundo 2026
# Version con funciones (def)
print("hola")


def crear_equipo():
    """Devuelve un diccionario con las estadisticas de un equipo en cero."""
    return {"pj": 0, "puntos": 0, "gf": 0, "gc": 0, "dg": 0}


def ingresar_equipos():
    """Pide los 4 nombres de equipo y devuelve el diccionario de equipos."""
    print("Ingrese los 4 equipos del grupo:")
    equipos = {}
    for i in range(1, 5):
        nombre = input(f"  Equipo {i}: ").strip().upper()
        equipos[nombre] = crear_equipo()
    return equipos


def generar_partidos(equipos):
    """
    Genera los 6 partidos posibles (cada equipo vs los demas).
    Devuelve una lista de tuplas (local, visitante).
    """
    nombres = list(equipos.keys())
    partidos = []
    for i in range(len(nombres)):
        for j in range(i + 1, len(nombres)):
            partidos.append((nombres[i], nombres[j]))
    return partidos


def procesar_partido(equipos, local, visitante, goles_local, goles_visitante):
    """
    Actualiza las estadisticas de ambos equipos segun el resultado.
    Suma partidos jugados, goles y puntos.
    """
    # Partidos jugados
    equipos[local]["pj"]     += 1
    equipos[visitante]["pj"] += 1

    # Goles a favor y en contra
    equipos[local]["gf"]     += goles_local
    equipos[local]["gc"]     += goles_visitante
    equipos[visitante]["gf"] += goles_visitante
    equipos[visitante]["gc"] += goles_local

    # Puntos segun resultado
    if goles_local > goles_visitante:
        equipos[local]["puntos"] += 3
        return f"{local} gana"
    elif goles_visitante > goles_local:
        equipos[visitante]["puntos"] += 3
        return f"{visitante} gana"
    else:
        equipos[local]["puntos"]     += 1
        equipos[visitante]["puntos"] += 1
        return "Empate"


def ingresar_resultados(equipos, partidos):
    """
    Recorre los partidos, pide los goles de cada uno
    y llama a procesar_partido() para actualizar estadisticas.
    """
    print("\nIngrese los resultados de cada partido:\n")
    for local, visitante in partidos:
        print(f"  {local} vs {visitante}")
        goles_local     = int(input(f"    Goles {local}: "))
        goles_visitante = int(input(f"    Goles {visitante}: "))
        resultado = procesar_partido(equipos, local, visitante, goles_local, goles_visitante)
        print(f"    Resultado: {resultado}\n")


def calcular_diferencia_gol(equipos):
    """Calcula la diferencia de gol (GF - GC) para cada equipo."""
    for nombre in equipos:
        equipos[nombre]["dg"] = equipos[nombre]["gf"] - equipos[nombre]["gc"]


def ordenar_tabla(equipos):
    """
    Ordena y devuelve la tabla segun los criterios FIFA:
    1. Mas puntos
    2. Mayor diferencia de gol
    3. Mas goles a favor
    4. Orden alfabetico (empate total)
    """
    return sorted(
        equipos.items(),
        key=lambda equipo: (
            -equipo[1]["puntos"],
            -equipo[1]["dg"],
            -equipo[1]["gf"],
             equipo[0]
        )
    )


def mostrar_tabla(tabla):
    """Muestra la tabla completa con todas las estadisticas."""
    print("==========================================")
    print(f"{'POS':<4} {'EQUIPO':<8} {'PJ':<4} {'PTS':<5} {'GF':<4} {'GC':<4} {'DG':<4}")
    print("------------------------------------------")
    for pos, (nombre, stats) in enumerate(tabla, start=1):
        print(f"{pos:<4} {nombre:<8} {stats['pj']:<4} {stats['puntos']:<5} {stats['gf']:<4} {stats['gc']:<4} {stats['dg']:<4}")
    print("==========================================\n")


def mostrar_clasificados(tabla):
    """Muestra los clasificados en el formato oficial FIFA."""
    print("Clasificados:")
    print(tabla[0][0])
    print(tabla[1][0])
    print("Tercero:")
    print(tabla[2][0])


# ============================================================
# PROGRAMA PRINCIPAL
# Llama a cada funcion en orden
# ============================================================

print("=== SISTEMA DE CLASIFICACION FIFA ===\n")

equipos  = ingresar_equipos()
partidos = generar_partidos(equipos)

ingresar_resultados(equipos, partidos)

calcular_diferencia_gol(equipos)

tabla = ordenar_tabla(equipos)

mostrar_tabla(tabla)
mostrar_clasificados(tabla)
