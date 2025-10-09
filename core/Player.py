class Player:
    """
    Representa a un jugador de Backgammon.
    
    Cada jugador tiene un color (blanco o negro) y opcionalmente un nombre.
    """
    
    def __init__(self, color, nombre=None):
        """
        Inicializa un jugador con su color y nombre.
        
        Recibe:
            color: cadena "blanco" o "negro"
            nombre: nombre del jugador (opcional)
        Hace: Valida el color y asigna los atributos
        Devuelve: Nada
        Excepción: ValueError si el color no es válido
        """
        color_norm = (color or "").strip().lower()
        if color_norm not in ("blanco", "negro"):
            raise ValueError("color debe ser 'blanco' o 'negro'")
        self.__color__ = color_norm
        self.__nombre__ = nombre

    def obtener_color(self):
        """
        Obtiene el color del jugador.
        
        Recibe: Nada
        Hace: Retorna el color asignado
        Devuelve: Cadena "blanco" o "negro"
        """
        return self.__color__

    def es_blanco(self):
        """
        Verifica si el jugador es de color blanco.
        
        Recibe: Nada
        Hace: Compara el color con "blanco"
        Devuelve: True si es blanco, False si no
        """
        return self.__color__ == "blanco"

    def es_negro(self):
        """
        Verifica si el jugador es de color negro.
        
        Recibe: Nada
        Hace: Compara el color con "negro"
        Devuelve: True si es negro, False si no
        """
        return self.__color__ == "negro"

    def nombre(self):
        """
        Obtiene el nombre del jugador.
        
        Recibe: Nada
        Hace: Retorna el nombre asignado
        Devuelve: Nombre del jugador o None si no tiene
        """
        return self.__nombre__