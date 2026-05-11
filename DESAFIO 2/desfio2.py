def leer_archivo(nombre_archivo):
    with open(nombre_archivo, "r") as archivo:
        contenido= archivo.read().strip().upper()
    return contenido

def validar_lista(lista):
    if len(lista)==0:
        return False, "EL archivo esta vacio."
    
    if len(lista)>1000:
        return False, "La lista supera los 1000 caracteres"
    
    for letra in lista:
        if caracter != "L" and caracter != "R" and caracter != "C":
            return false, f"Se encontro caracter no valido:'{caracter}'. Solo se permite L, R, C."
    return True, "Lista valida."

def contar_lista(lista):
    
    
        

        