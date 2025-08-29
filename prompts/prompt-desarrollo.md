# Pregunta 
hola chat, existe alguna libreria que pueda usar para programar una dado? necesito que tire numeros random de l1 al 6
## Respuesta
Sí, para programar un dado en Python no necesitás ninguna librería extra, podés usar la librería estándar random que ya viene incluida.

Un ejemplo súper simple sería este:

import random

def tirar_dado():
    return random.randint(1, 6)

#Probar el dado
for _ in range(5):
    print(tirar_dado())


