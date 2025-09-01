from core.Player import Player
from core.Dice import Dice


class BackgammonGame:
    def __init__(self, player1= "Blancas", player2= "Negras"):
        self.__players__ = {"B": Player("blanco", player1), "N": Player("negro", player2)}
        self.__turno__ = "B"
        self.__dice__ = Dice()

        def __turno__(self):
            return self.__turno__
        