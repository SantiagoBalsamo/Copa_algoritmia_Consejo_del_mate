#Copa algoritmia 2026 - Desafio 2

# --- Funciones ---

with open('DESAFIO 2/penales.txt', "r") as archivo:
    lista= archivo.read().strip().upper()
    
penales_izquierda=0
penales_centro=0
penales_derecha=0

for letra in lista:
    if letra== "L":
        penales_izquierda=penales_izquierda+1
    elif letra== "C":
        penales_centro=penales_centro+1
    elif letra== "R":
        penales_derecha=penales_derecha+1

if penales_izquierda>= penales_centro and penales_izquierda>=penales_derecha:
    direccion="L"
    maximo=penales_izquierda
elif penales_derecha>= penales_centro:
    direccion="R"
    maximo=penales_derecha
else:
    direccion="C"
    maximo=penales_centro

print(direccion)
print(maximo)

#Recibe datos de un archivo .txt y lo valida

#Valida que los caracteres sean correctos (L,R,C) y que no supere la cantidad (<=0 y >=1000)

#Cuenta los caracteres y los ordena de mayor a menor






# --- Programa inicial --- 