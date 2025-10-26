from .Player import Player
from .Dice import Dice
from .Board import Board

class BackgammonGame:
    def __init__(self, player1="Blancas", player2="Negras"):
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
        # Asumiendo que Player.obtener_color() devuelve 'blanco' o 'negro',
        # pero el juego usa 'B' o 'N', adaptamos.
        color_key = "B" if self.__players__[self.__turno__].obtener_color() == "blanco" else "N"
        return self.__players__[color_key]

    def board(self):
        return self.__board__

    def roll(self):
        self.__dice_cache__ = self.__dice__.roll()
        self.__used_dice__ = []
        return list(self.__dice_cache__)

    def dice(self):
        """Retorna todos los dados de la tirada actual"""
        return list(self.__dice_cache__)
    
    def available_dice(self):
        """Retorna los dados disponibles (no usados)"""
        available = []
        used_copy = list(self.__used_dice__)
        
        for die in self.__dice_cache__:
            if die in used_copy:
                used_copy.remove(die)
            else:
                available.append(die)
        
        return available
    
    def move(self, from_point, die_value):
        """Intenta mover una ficha"""
        
        # El dado debe estar disponible (se quita el check de can_move para evitar redundancia)
        if die_value not in self.available_dice():
            return False

        # Verifica si es un movimiento válido, incluyendo la lógica de Bearing Off
        if not self.can_move(from_point, die_value):
            return False
        
        # El 'move' del Board ya maneja la lógica de captura y Bearing Off
        if self.__board__.move(from_point, die_value, self.__turno__):
            self.__used_dice__.append(die_value)
            
            # NUEVO: Verificar si el juego terminó después del movimiento
            if self.is_game_over():
                print(f"¡El jugador {self.current_player().nombre()} ha ganado!")
            
            # NUEVO: Terminar el turno automáticamente si no quedan dados
            if not self.available_dice():
                self.end_turn() 
            
            return True
        return False
    
    def can_move(self, from_point, die_value):
        """Verifica si un movimiento es válido"""
        if die_value not in self.available_dice():
            return False
        return self.__board__.can_move(from_point, die_value, self.__turno__)
    
    def get_valid_moves(self):
        """Obtiene todos los movimientos válidos"""
        return self.__board__.get_valid_moves(self.__turno__, self.available_dice())
    
    def has_valid_moves(self):
        """Verifica si hay movimientos válidos"""
        return len(self.get_valid_moves()) > 0
    
    def can_end_turn(self):
        """Verifica si se puede terminar el turno"""
        if not self.__dice_cache__: # Si no se ha tirado
            return False 
        if not self.available_dice():
            return True
        return not self.has_valid_moves()

    def end_turn(self):
        """Termina el turno y cambia al siguiente jugador"""
        self.__turno__ = "N" if self.__turno__ == "B" else "B"
        
        # <<< ESTAS DOS LÍNEAS FALTABAN O ESTABAN MAL >>>
        self.__dice_cache__ = []  # Limpia la tirada de dados
        self.__used_dice__ = []   # Limpia los dados usados
        
    def is_game_over(self): # NUEVO: Condición de victoria
        """Verifica si el juego ha terminado (un jugador retiró 15 fichas)."""
        return self.__board__.off()['B'] == 15 or self.__board__.off()['N'] == 15

    def winner(self): # NUEVO: Devuelve el ganador
        """Retorna el color ('B'/'N') del ganador o None."""
        if self.__board__.off()['B'] == 15:
            return "B"
        if self.__board__.off()['N'] == 15:
            return "N"
        return None