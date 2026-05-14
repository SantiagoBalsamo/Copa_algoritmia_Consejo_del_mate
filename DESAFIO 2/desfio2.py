# --- Copa algoritmia 2026 --- Desafio 2 ---

# --- Funciones ---

def leer_archivo(nombre_archivo):
    """Abre el archivo y le otorga permisos de lectura.
    Se lee directamente el contenido en MAYUSCULA, se reemplazan los caracteres indicados y devuelve una cadena vacia.

    Args:
        Argumento_1(archivo): Nombre del archivo.txt.

    Returns:
        Retorna el contenido del archivo con las validaciones sobre caracteres dadas.

    Raises:
        FileNotFoundError: En caso de que el nombre ingresado no coincida con ningun archivo.    
    """
    with open(nombre_archivo, "r") as archivo:
        contenido = archivo.read().upper()
        contenido = contenido.replace("\n", "").replace("\r", "").replace(" ", "").strip()
    return contenido

def validar_secuencia(secuencia):
    if len(secuencia) == 0:
        return False, "El archivo está vacío."
    if len(secuencia) > 1000:
        return False, "La secuencia supera los 1000 caracteres."
    for caracter in secuencia:
        if caracter != "L" and caracter != "R" and caracter != "C":
            return False, f"Carácter inválido encontrado: '{caracter}'. Solo se permiten L, R y C."
    return True, "Secuencia válida."

# Inicia los contadores y suma cuando encunetra el caracter
def contar_direcciones(secuencia):
    return secuencia.count('L'), secuencia.count('R'), secuencia.count('C')

# En caso de empate l>r>c
def mayor_cantidad(cant_L, cant_R, cant_C):
    if cant_L >= cant_R and cant_L >= cant_C:
        direccion = "L"
        maximo = cant_L
    elif cant_R >= cant_C:
        direccion = "R"
        maximo = cant_R
    else:
        direccion = "C"
        maximo = cant_C
    return direccion, maximo


# Muestra la direccion de penal donde mas se pateo
def mostrar_resultado(direccion, maximo):
    print("--------")
    print(direccion)
    print(maximo)
    print("--------")



# --- PROGRAMA PRINCIPAL ---

nombre_archivo = "DESAFIO 2/penales.txt"

# si encuentra un dato no valido, pide que se revise el .txt y toque enter para que lo lea nuevamente
while True:
    secuencia = leer_archivo(nombre_archivo)
    es_valida = validar_secuencia(secuencia)
    mensaje = validar_secuencia(secuencia)
    if es_valida:
        cant_L, cant_R, cant_C = contar_direcciones(secuencia)
        direccion, maximo = mayor_cantidad(cant_L, cant_R, cant_C)
        mostrar_resultado(direccion, maximo)
        break
    else:
        print("Error:", mensaje)
        print("Corregí el archivo penales.txt y presioná ENTER para reintentar...")
        input()






        
