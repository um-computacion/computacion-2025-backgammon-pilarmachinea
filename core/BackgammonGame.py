from .Player import Player
from .Dice import Dice
from .Board import Board

class BackgammonGame:
    def __init__(self, player1= "Blancas", player2= "Negras"):
        self.__players__ = {"B": Player("blanco", player1), "N": Player("negro", player2)}
        self.__turno__ = "B"
        self.__dice__ = Dice()
        self.__board__ = Board()
        self.__dice_cache__ = []
        self.__used_dice__ = []

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
        self.__used_dice__ = []
        return list(self.__dice_cache__)

    def dice(self):
        available = [d for d in self.__dice_cache__ if d not in self.__used_dice__]
        for used in self.__used_dice__:
            if used in available:
                available.remove(used)
        return list(self.__dice_cache__)
    
    def move(self, from_point, die_value):
        if die_value not in self.available_dice():
            return False
        
        if self.__board__.move(from_point, die_value, self.__turno__):
            self.__used_dice__.append(die_value)
            return True
        return False
    
    def can_move(self, from_point, die_value):
        if die_value not in self.available_dice():
            return False
        return self.__board__.can_move(from_point, die_value, self.__turno__)
    
    def get_valid_moves(self):
        return self.__board__.get_valid_moves(self.__turno__, self.available_dice())
    
    def has_valid_moves(self):
        return self.__board__.has_valid_moves(self.__turno__, self.available_dice())
    
    def can_end_turn(self):
        if not self.available_dice():
            return True
        return not self.has_valid_moves()

    def end_turn(self):
        if not self.can_end_turn():
            return False
        self.__turno__ = "N" if self.__turno__ == "B" else "B"
        self.__dice_cache__ = []
        self.__used_dice__ = []
        return True

