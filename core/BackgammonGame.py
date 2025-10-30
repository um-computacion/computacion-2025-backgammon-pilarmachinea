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

    # =========================
    # Helpers de bearing off
    # =========================
    def _is_in_home_range(self, point_idx: int, color: str) -> bool:
        """Devuelve True si el punto está en el tablero interno (home) del color."""
        if color == "B":
            return 18 <= point_idx <= 23  # 19-24 en notación humana
        else:
            return 0 <= point_idx <= 5    # 1-6 en notación humana

    def _pips_to_bear_off(self, point_idx: int, color: str) -> int:
        """Pasos exactos que faltan desde point_idx hasta salir (off)."""
        if color == "B":
            return (23 - point_idx) + 1  # B sube hacia 23 y sale
        else:
            return point_idx + 1         # N baja hacia 0 y sale

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
        # El dado debe estar disponible
        if die_value not in self.available_dice():
            return False

        # Verifica si es un movimiento válido, incluyendo la lógica de Bearing Off exacto
        if not self.can_move(from_point, die_value):
            return False
        
        # El 'move' del Board ya maneja la lógica de captura y Bearing Off
        if self.__board__.move(from_point, die_value, self.__turno__):
            self.__used_dice__.append(die_value)
            
            # ¿Terminó el juego?
            if self.is_game_over():
                print(f"¡El jugador {self.current_player().nombre()} ha ganado!")
            
            # Si no quedan dados, termina el turno
            if not self.available_dice():
                self.end_turn() 
            
            return True
        return False
    
    def can_move(self, from_point, die_value):
        """
        Verifica si un movimiento es válido.
        REGLA NUEVA: para retirar (bear off) se exige dado EXACTO.
        """
        # Dado debe estar disponible
        if die_value not in self.available_dice():
            return False

        color = self.__turno__

        # Si el origen es un punto del tablero, aplicamos la restricción de "off exacto"
        if isinstance(from_point, int) and 0 <= from_point <= 23:
            # Si está en el home del color, podría ser un intento de retirar
            if self._is_in_home_range(from_point, color):
                pips = self._pips_to_bear_off(from_point, color)
                # Si el dado es MAYOR que la distancia para salir, NO permitimos (regla estricta)
                if die_value > pips:
                    return False
                # Si el dado es EXACTO, lo dejamos pasar a evaluación del Board (que además valida que todas estén en casa)
                # Si el dado es menor, es movimiento interno normal dentro del home; lo decide el Board.
        
        # Para cualquier otro caso (incluye barra y movimientos normales), delegamos al Board
        return self.__board__.can_move(from_point, die_value, color)
    
    def get_valid_moves(self):
        """Obtiene todos los movimientos válidos (según Board)."""
        return self.__board__.get_valid_moves(self.__turno__, self.available_dice())
    
    def has_valid_moves(self):
        """
        Verifica si hay movimientos válidos con la REGLA ESTRICTA de 'off' exacto.
        Probamos todos los orígenes razonables con cada dado disponible usando nuestro can_move().
        """
        dice = self.available_dice()
        if not dice:
            return False

        # Probar entrada desde barra si el Board lo soporta con from_point=None
        for d in set(dice):
            try:
                if self.can_move(None, d):  # muchos Boards aceptan None para la barra
                    return True
            except Exception:
                # Si el Board no soporta None, ignoramos y seguimos
                pass

        # Probar todos los puntos del tablero (0..23)
        for i in range(24):
            for d in set(dice):
                try:
                    if self.can_move(i, d):
                        return True
                except Exception:
                    # Si el Board lanza algo por un índice inválido en cierto estado, seguimos
                    continue
        return False
    
    def can_end_turn(self):
        """Verifica si se puede terminar el turno"""
        if not self.__dice_cache__:  # Si no se ha tirado
            return False 
        if not self.available_dice():
            return True
        # Si no hay ningún movimiento válido (con regla estricta), se puede finalizar
        return not self.has_valid_moves()

    def end_turn(self):
        """Termina el turno y cambia al siguiente jugador"""
        self.__turno__ = "N" if self.__turno__ == "B" else "B"
        # Limpia la tirada de dados
        self.__dice_cache__ = []
        self.__used_dice__ = []
        
    def is_game_over(self):  # Condición de victoria
        """Verifica si el juego ha terminado (un jugador retiró 15 fichas)."""
        return self.__board__.off()['B'] == 15 or self.__board__.off()['N'] == 15

    def winner(self):  # Devuelve el ganador
        """Retorna el color ('B'/'N') del ganador o None."""
        if self.__board__.off()['B'] == 15:
            return "B"
        if self.__board__.off()['N'] == 15:
            return "N"
        return None
