class Player:
    def __init__(self, color, nombre):
        self.__color__ = color
        self.__nombre__ = nombre

    def color(self):
        return self.__color__
    
    def nombre(self):
        return self.__nombre__