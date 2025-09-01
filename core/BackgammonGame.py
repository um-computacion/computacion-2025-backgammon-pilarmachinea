from Player import Player
from Dice import Dice
from Board import Board

class BackgammonGame:
    def __init__(self, player1= "Blancas", player2= "Negras"):
        self.__players__ = {"B": Player("blanco", player1), "N": Player("negro", player2)}
        self.__turno__ = "B"
        self.__dice__ = Dice()
        self.__board__ = Board()
        self.__dice_cache__ = []

    def turno(self):
        return self.__turno__
    
    def players(self):
        return dict(self.__players__)
    
    def current_player(self):
        return self.__players__[self.__turno__]

    def board(self):
        return self.__board__

    def roll(self):
        self.__dice_cache__ = self.__dice__.roll()
        return list(self.__dice_cache__)

    def dice(self):
        return list(self.__dice_cache__)

    def end_turn(self):
        self.__turno__ = "N" if self.__turno__ == "B" else "B"
        self.__dice_cache__ = []

