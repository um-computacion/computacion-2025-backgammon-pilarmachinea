import random

class Dice:
    """
    Representa los dados del juego de Backgammon.
    
    Maneja el lanzamiento de dos dados de 6 caras y la regla de dobles
    (cuando salen iguales se pueden hacer 4 movimientos).
    """
    
    def __init__(self):
        """
        Inicializa los dados sin valores.
        
        Recibe: Nada
        Hace: Crea lista vacía para almacenar últimos valores
        Devuelve: Nada
        """
        self.__last__ = []

    def roll(self):
        """
        Lanza los dos dados y genera valores aleatorios.
        
        Recibe: Nada
        Hace: Genera dos números aleatorios del 1 al 6
              Si son iguales (dobles), genera 4 valores iguales
              Si son diferentes, genera 2 valores
        Devuelve: Lista con los valores de los dados
        """
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        if d1 == d2:
            self.__last__ = [d1, d1, d1, d1]
        else:
            self.__last__ = [d1, d2]
        return list(self.__last__)

    def last(self):
        """
        Obtiene los valores de la última tirada.
        
        Recibe: Nada
        Hace: Retorna copia de los últimos valores tirados
        Devuelve: Lista con valores de la última tirada
        """
        return list(self.__last__)