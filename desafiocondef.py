# Sistema de Clasificacion FIFA 

# --- FUNCIONES ---

#Devuelve un diccionario con las estadisticas de un equipo en cero
def crear_equipo():
    return {"pj": 0, "puntos": 0, "gf": 0, "gc": 0, "dg": 0}

#Genera los 6 partidos posibles (cada equipo vs los demas), devuelve una lista de tuplas (local, visitante)
def generar_partidos(equipos):
   
    nombres = list(equipos.keys())
    partidos = []
    for i in range(len(nombres)):
        for j in range(i + 1, len(nombres)):
            partidos.append((nombres[i], nombres[j]))
    return partidos


#Actualiza las estadisticas de ambos equipos segun el resultado, suma partidos jugados, goles y puntos
def procesar_partido(equipos, local, visitante, goles_local, goles_visitante):
    
    equipos[local]["pj"]     += 1
    equipos[visitante]["pj"] += 1

    equipos[local]["gf"]     += goles_local
    equipos[local]["gc"]     += goles_visitante
    equipos[visitante]["gf"] += goles_visitante
    equipos[visitante]["gc"] += goles_local

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


#Lee los equipos y resultados desde un archivo.txt(validacion de entradas)
def leer_desde_archivo():

    nombre_archivo = input("Ingrese el nombre del archivo: ").strip()

    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            equipos = {}
            partidos_procesados = set()
            resultados = []

            for linea in archivo:
                linea = linea.strip()

                if not linea:
                    continue

                partes = linea.split(",")
                if len(partes) != 4:
                    print("    No valido, por favor ingrese nuevamente.")
                    return {}

                local, visitante, goles_local, goles_visitante = partes

                local     = " ".join(local.strip().upper().split())
                visitante = " ".join(visitante.strip().upper().split())

                if not local.replace(" ", "").isalpha() or not visitante.replace(" ", "").isalpha():
                    print("    No valido, por favor ingrese nuevamente.")
                    return {}

                if local == visitante:
                    print("")
                    return {}

                par = tuple(sorted([local, visitante]))
                if par in partidos_procesados:
                    print("")
                    return {}
                partidos_procesados.add(par)
          
                try:
                    goles_local     = int(goles_local.strip())
                    goles_visitante = int(goles_visitante.strip())
                except ValueError:
                    print("")
                    return {}

                if goles_local < 0 or goles_local > 20 or goles_visitante < 0 or goles_visitante > 20:
                    print("")
                    return {}

                if local not in equipos:
                    equipos[local] = crear_equipo()
                if visitante not in equipos:
                    equipos[visitante] = crear_equipo()

                if equipos[local]["pj"] >= 3 or equipos[visitante]["pj"] >= 3:
                    print("")
                    return {}

                resultado = procesar_partido(equipos, local, visitante, goles_local, goles_visitante)
                resultados.append(f"  {local} vs {visitante}\n    Resultado: {resultado}\n")

            print("\nResultados de cada partido:\n")
            for r in resultados:
                print(r)
            if len(equipos) != 4:
                print(f"    Porfavor ingrese 4 equipos, actualmente se encontraron {len(equipos)}.")
                return {}
            if len(partidos_procesados) != 6:
                print(f"    Porfavor ingrese 6 partidos,  {len(partidos_procesados)}.")
                return {}
        return equipos

    except FileNotFoundError:
        print(f"\n  Error: no se encontro el archivo '{nombre_archivo}'")
        return {}


#Calcula la diferencia de gol (GF - GC) para cada equipo
def calcular_diferencia_gol(equipos):

    for nombre in equipos:
        equipos[nombre]["dg"] = equipos[nombre]["gf"] - equipos[nombre]["gc"]


'''
    Ordena y devuelve la tabla segun los criterios de la FIFA:
    1. Mas puntos
    2. Mayor diferencia de gol
    3. Mas goles a favor
    4. Orden alfabetico (empate total)
'''
def ordenar_tabla(equipos):
 
    return sorted(
        equipos.items(),
        key=lambda equipo: (
            -equipo[1]["puntos"],
            -equipo[1]["dg"],
            -equipo[1]["gf"],
             equipo[0]
        )
    )


#Muestra la tabla completa con todas las estadisticas
def mostrar_tabla(tabla):

    ancho = max(len(nombre) for nombre, _ in tabla)
    ancho = max(ancho, 6) + 2

    separador = "=" * (ancho + 30)
    divisor   = "-" * (ancho + 30)
    print(separador)
    print(f"{'POS':<4} {'EQUIPO':<{ancho}} {'PJ':<4} {'PTS':<5} {'GF':<4} {'GC':<4} {'DG':<4}")
    print(divisor)
    for pos, (nombre, stats) in enumerate(tabla, start=1):
        print(f"{pos:<4} {nombre:<{ancho}} {stats['pj']:<4} {stats['puntos']:<5} {stats['gf']:<4} {stats['gc']:<4} {stats['dg']:<4}")
    print(separador + "\n")


#Muestra los clasificados en el formato oficial FIFA
def mostrar_clasificados(tabla):
    
    print("========================")
    print("Posicion de Clasificados")
    print("========================\n")

    print("------------")
    print("    Primer puesto")
    print(tabla[0][0])
    print("-------------")
    print("    Segundo puesto")
    print(tabla[1][0])
    print("-------------")
    print("    Tercero puesto")
    print(tabla[2][0])
    print("-------------")


# --- PROGRAMA PRINCIPAL ---

print("=== SISTEMA DE CLASIFICACION FIFA ===\n")

equipos = leer_desde_archivo()

if not equipos or any(stats["pj"] != 3 for _, stats in equipos.items()):
    print("  Error: porfavor ingrese datos validos")

else:
    calcular_diferencia_gol(equipos)
    tabla = ordenar_tabla(equipos)
    mostrar_tabla(tabla)
    mostrar_clasificados(tabla)

    