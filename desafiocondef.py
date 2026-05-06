# Sistema de Clasificacion FIFA 

# --- FUNCIONES ---

#Pide los 4 nombres de equipo y crea un diccionario con los nombres de los paises
def ingresar_equipos():

    print("Ingrese los 4 equipos del grupo:")
    equipos = {}
    for i in range(1, 5):
        while True:
            nombre = " ".join(input(f"  Equipo {i}: ").strip().upper().split())
            if not nombre.replace(" ", "").isalpha():
                print("    No valido, por favor ingrese nuevamente.")
                continue
            if nombre in equipos:
                print(f"    No valido, el pais ya fue ingresado.")
            else:
                equipos[nombre] = crear_equipo()
                break    
    return equipos



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
    


#Pide los goles de cada uno y valida que solo sea un caracter numerico lo que se ingresa
def ingresar_resultados(equipos, partidos):

    print("\nIngrese los resultados de cada partido:\n")
    for local, visitante in partidos:
        print(f"  {local} vs {visitante}")

        # Validar goles del equipo local
        encontrado=False
        while not encontrado:
            entrada = input(f"    Goles {local}: ").strip()
            try:
                goles_local = int(entrada)
                if goles_local<0:
                    print("    No valido, por favor ingrese nuevamente.")
                else:
                    encontrado=True
            except ValueError:
                print("    No valido, por favor ingrese nuevamente.\n")

        # Validar goles del equipo visitante
        encontrado=False
        while not encontrado:
            entrada = input(f"    Goles {visitante}: ").strip()
            try:
                goles_visitante = int(entrada)
                if goles_visitante<0:
                    print("    No valido, por favor ingrese nuevamente.")
                else:
                    encontrado=True
            except ValueError:
                print("    No valido, por favor ingrese nuevamente.\n")

        resultado = procesar_partido(equipos, local, visitante, goles_local, goles_visitante)
        print(f"    Resultado: {resultado}\n")



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
    print(separador)
    print(f"{'POS':<4} {'EQUIPO':<{ancho}} {'PJ':<4} {'PTS':<5} {'GF':<4} {'GC':<4} {'DG':<4}")
    print("-" * (ancho + 30))
    for pos, (nombre, stats) in enumerate(tabla, start=1):
        print(f"{pos:<4} {nombre:<{ancho}} {stats['pj']:<4} {stats['puntos']:<5} {stats['gf']:<4} {stats['gc']:<4} {stats['dg']:<4}")
    print(separador + "\n")



#Muestra los clasificados en el formato oficial FIFA
def mostrar_clasificados(tabla):
    
    print("========================")
    print("Posicion de Clasificados")
    print("========================\n")

    print("------------")
    print("Primer puesto")
    
    print(tabla[0][0])
    print("-------------")
    print("Segundo puesto")
    
    print(tabla[1][0])
    print("-------------")
    print("Tercero puesto")

    print(tabla[2][0])
    print("-------------")



# --- PROGRAMA PRINCIPAL ---

print("=== SISTEMA DE CLASIFICACION FIFA ===\n")

equipos  = ingresar_equipos()
partidos = generar_partidos(equipos)

ingresar_resultados(equipos, partidos)
calcular_diferencia_gol(equipos)

tabla = ordenar_tabla(equipos)

mostrar_tabla(tabla)
mostrar_clasificados(tabla)
