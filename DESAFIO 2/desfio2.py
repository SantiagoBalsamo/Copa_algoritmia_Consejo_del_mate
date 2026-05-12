#Copa algoritmia 2026 - Desafio 2

# --- Funciones ---

def leer_archivo():
        try:
            with open('DESAFIO 2/penales.txt', "r") as archivo:
                datos = archivo.read().strip().upper()
            return datos   
        except FileNotFoundError:
            print('ERROR: NO SE ENCONTRO EL ARCHIVO SELECCIONADO')

def contar_penales(datos):
    penales_izquierda = 0
    penales_centro = 0
    penales_derecha = 0

    for letra in datos:
       try: 
        if letra == "L":
            penales_izquierda = penales_izquierda + 1
        elif letra == "C":
            penales_centro = penales_centro + 1
        elif letra == "R":
            penales_derecha = penales_derecha + 1
       except ValueError:
           print("ERROR: INGRESE DATOS VALIDOS")
    return penales_izquierda, penales_centro, penales_derecha

def direccion_maxima(penales_izquierda, penales_centro, penales_derecha):
    # Cuenta los caracteres y los ordena de mayor a menor
    if penales_izquierda >= penales_centro and penales_izquierda >= penales_derecha:
        direccion = "L"
        maximo = penales_izquierda
    elif penales_derecha >= penales_centro:
        direccion = "R"
        maximo = penales_derecha
    else:
        direccion = "C"
        maximo = penales_centro

    return direccion, maximo

# --- Programa principal ---

lista = leer_archivo()
penales_izquierda, penales_centro, penales_derecha = contar_penales(lista)
direccion, maximo = direccion_maxima(penales_izquierda, penales_centro, penales_derecha)

print(direccion)
print(maximo)