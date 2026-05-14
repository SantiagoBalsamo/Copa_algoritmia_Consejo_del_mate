# --- Copa algoritmia 2026 --- Desafio 2 ---

# --- Funciones ---

def leer_archivo(nombre_archivo):
    """Lee un archivo de texto y devuelve su contenido en mayúsculas sin espacios ni saltos de línea"""
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        tabla = str.maketrans("", "", " \n\r")
        return archivo.read().upper().translate(tabla)

def validar_secuencia(secuencia):
    """Valida que la secuencia no esté vacía, no supere 1000 caracteres y solo contenga los caracteres: 'L', 'R' o 'C'."""
    if len(secuencia) == 0:
        return False, "El archivo está vacío."
    if len(secuencia) > 1000:
        return False, "La secuencia supera los 1000 caracteres."
    for caracter in secuencia:
        if caracter != "L" and caracter != "R" and caracter != "C":
            return False, f"Carácter inválido encontrado: '{caracter}'. Solo se permiten L, R y C."
    return True, "Secuencia válida."

def contar_direcciones(secuencia):
    """Cuenta la cantidad de repeticiones en cada direccion(L, R, C)"""
    return secuencia.count('L'), secuencia.count('R'), secuencia.count('C')

def mayor_cantidad(cant_L, cant_R, cant_C):
    """Retorna la dirección con mayor cantidad de repeticiones y su valor."""
    direcciones = {"L": cant_L, "R": cant_R, "C": cant_C}
    direccion = max(direcciones, key=direcciones.get)
    return direccion, direcciones[direccion]

def mostrar_resultado(direccion, maximo):
    """Muestra la dirección de penal con más remates y su cantidad."""
    print("--------")
    print(direccion)
    print(maximo)
    print("--------")


# --- PROGRAMA PRINCIPAL ---

nombre_archivo = "./DESAFIO 2/penales.txt"

try:
    secuencia = leer_archivo(nombre_archivo)
except FileNotFoundError:
    print(f"ERROR: EL ARCHIVO '{nombre_archivo}' NO EXISTE EN EL DIRECTORIO")
else:
    es_valida, mensaje = validar_secuencia(secuencia)
    if es_valida:
        cant_L, cant_R, cant_C = contar_direcciones(secuencia)
        direccion, maximo = mayor_cantidad(cant_L, cant_R, cant_C)
        mostrar_resultado(direccion, maximo)
    else:
        print(f"Error: {mensaje}")
        