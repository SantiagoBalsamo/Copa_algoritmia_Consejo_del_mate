# ============================================================
# Sistema de Clasificacion FIFA - Copa del Mundo 2026
# Ingreso manual de equipos y resultados
# ============================================================

print("=== SISTEMA DE CLASIFICACION FIFA ===")
print()

# ----------------------------
# PASO 1: Ingresar los 4 equipos
# ----------------------------
print("Ingrese los 4 equipos del grupo:")
equipos = {}
for i in range(1, 5):
    nombre = input(f"  Equipo {i}: ").strip().upper()
    equipos[nombre] = {"pj": 0, "puntos": 0, "gf": 0, "gc": 0}

nombres = list(equipos.keys())

# ----------------------------
# PASO 2: Generar los 6 partidos automaticamente
# (cada equipo juega contra los otros 3)
# ----------------------------
partidos = []
for i in range(len(nombres)):
    for j in range(i + 1, len(nombres)):
        partidos.append((nombres[i], nombres[j]))

# ----------------------------
# PASO 3: Ingresar resultados de cada partido
# ----------------------------
print()
print("Ingrese los resultados de cada partido:")
print()

for local, visitante in partidos:
    print(f"  {local} vs {visitante}")
    goles_local     = int(input(f"    Goles {local}: "))
    goles_visitante = int(input(f"    Goles {visitante}: "))

    # Sumar partidos jugados
    equipos[local]["pj"]     += 1
    equipos[visitante]["pj"] += 1

    # Sumar goles a favor y en contra
    equipos[local]["gf"]     += goles_local
    equipos[local]["gc"]     += goles_visitante
    equipos[visitante]["gf"] += goles_visitante
    equipos[visitante]["gc"] += goles_local

    # Asignar puntos segun resultado
    if goles_local > goles_visitante:
        equipos[local]["puntos"] += 3
        resultado = f"{local} gana"
    elif goles_visitante > goles_local:
        equipos[visitante]["puntos"] += 3
        resultado = f"{visitante} gana"
    else:
        equipos[local]["puntos"]     += 1
        equipos[visitante]["puntos"] += 1
        resultado = "Empate"

    print(f"    Resultado: {resultado}")
    print()

# ----------------------------
# PASO 4: Calcular diferencia de gol
# ----------------------------
for nombre in equipos:
    equipos[nombre]["dg"] = equipos[nombre]["gf"] - equipos[nombre]["gc"]

# ----------------------------
# PASO 5: Ordenar la tabla
# Criterios: puntos -> diferencia de gol -> goles a favor -> alfabetico
# ----------------------------
tabla = sorted(
    equipos.items(),
    key=lambda equipo: (
        -equipo[1]["puntos"],
        -equipo[1]["dg"],
        -equipo[1]["gf"],
         equipo[0]
    )
)

# ----------------------------
# PASO 6: Mostrar tabla completa
# ----------------------------
print("==========================================")
print(f"{'POS':<4} {'EQUIPO':<8} {'PJ':<4} {'PTS':<5} {'GF':<4} {'GC':<4} {'DG':<4}")
print("------------------------------------------")
for pos, (nombre, stats) in enumerate(tabla, start=1):
    print(f"{pos:<4} {nombre:<8} {stats['pj']:<4} {stats['puntos']:<5} {stats['gf']:<4} {stats['gc']:<4} {stats['dg']:<4}")
print("==========================================")
print()

# ----------------------------
# PASO 7: Mostrar clasificados en formato oficial
# ----------------------------
print("Clasificados:")
print(tabla[0][0])
print(tabla[1][0])
print("Tercero:")
print(tabla[2][0])