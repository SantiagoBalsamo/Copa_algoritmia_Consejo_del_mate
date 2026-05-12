# Copa Algoritmia UADE 2026— Desafío 2

### Grupo de Programación - EL CONSEJO DEL MATE

##¿Qué hace el programa?
El código lee un archivo llamado `penales.txt` que tiene una secuencia de letras:
* **L**: Izquierda
* **R**: Derecha
* **C**: Centro

Lo que hace es contar cuántas veces aparece cada una y fijarse cuál es la que más se repite. Al final, imprime la letra ganadora y la cantidad de veces que salió.

##  El tema de los empates (Prioridad Táctica)
Como decía el PDF de la consigna, si hay un empate en la cantidad de tiros, usamos la regla de prioridad:
1.  **Izquierda (L)** le gana a todos.
2.  **Derecha (R)** le gana al Centro.
3.  **Centro (C)** queda último.

O sea: **L > R > C**. Esto ya lo dejamos configurado en los `if/elif` de la función `direccion_maxima`.

##  Archivos en la carpeta
* `desfio2.py`: Es el archivo principal con todo el código modularizado con funciones (nos pareció más prolijo así).
* `penales.txt`: Acá es donde tienen que pegar la secuencia de penales para que el programa la analice. Ya dejamos una cargada para probar.

---
**Nota para el profe:** Intentamos que el código sea lo más eficiente posible recorriendo la lista una sola vez como pedía la consigna. Cualquier cosa nos avisan!