class Player:
    def __init__(self, color, nombre):
        self.__color__ = color
        self.__nombre__ = nombre

    def obtener_color(self):
        return self.__color__
    
    def obtener_nombre(self):
        return self.__nombre__