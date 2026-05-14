# Copa Algoritmia UADE 2026— Desafío 2
# --- EL CONSEJO DEL MATE ---

# Lenguaje utilizado: Python
# IDE utilizado: Visual Studio Code
# Librerias utilizadas: Ninguna
 

# ¿Qué hace el programa?
El código lee un archivo llamado `penales.txt` que tiene una secuencia de letras:
* **L**: Izquierda
* **R**: Derecha
* **C**: Centro

Lo que hace es contar cuántas veces aparece cada una y fijarse cuál es la que más se repite. Al final, imprime la letra ganadora y la cantidad de veces que salió.

##  En caso de empate absoluto (Prioridad Táctica)
Como decía el PDF de la consigna, si hay un empate en la cantidad de tiros, usamos la regla de prioridad:
1.  **Izquierda (L)** le gana a todos.
2.  **Derecha (R)** le gana al Centro.
3.  **Centro (C)** queda último.

O sea: **L > R > C**. Esto ya lo dejamos configurado en los `if/elif` de la función `direccion_maxima`.

---
