from .Checker import Checker

class Board:
    def __init__(self):
        self.__points__ = [[] for _ in range(24)]
        self.__bar__ = {"B": [], "N": []} 
        self.__off__ = {"B": 0, "N": 0}
        self._setup()

    def _put(self, idx, color, n):
        for _ in range(n):
            self.__points__[idx].append(Checker(color))

    def _setup(self):
        """Setup estÃ¡ndar de backgammon.
        Blancas: 24(2), 13(5), 8(3), 6(5)
        Negras: 1(2), 12(5), 17(3), 19(5)
        """
        # Ãndices 0-based (punto 1 = idx 0, punto 24 = idx 23)
        self._put(23, 'B', 2)   # punto 24
        self._put(12, 'B', 5)   # punto 13
        self._put(7, 'B', 3)    # punto 8
        self._put(5, 'B', 5)    # punto 6
        
        self._put(0, 'N', 2)    # punto 1
        self._put(11, 'N', 5)   # punto 12
        self._put(16, 'N', 3)   # punto 17
        self._put(18, 'N', 5)   # punto 19

    def points(self):
        return self.__points__

    def bar(self):
        return self.__bar__

    def off(self):
        return self.__off__

    def point_owner_count(self, idx):
        if not self.__points__[idx]:
            return None, 0
        color = self.__points__[idx][0].color()
        count = len(self.__points__[idx])
        return color, count

    def has_checkers_on_bar(self, color):
        return len(self.__bar__[color]) > 0

    def _get_home_range(self, color):
        """Casa: Blancas 1-6 (idx 0-5), Negras 19-24 (idx 18-23)"""
        return range(0, 6) if color == 'B' else range(18, 24)

    def can_bear_off(self, color):
        """Verifica si todas las fichas estÃ¡n en casa o fuera."""
        if self.has_checkers_on_bar(color):
            return False
            
        home_range = self._get_home_range(color)
        
        for idx in range(24):
            if idx not in home_range:
                if any(c.color() == color for c in self.__points__[idx]):
                    return False
        return True

    def _can_land_on(self, to_point, player_color):
        """Verifica si se puede aterrizar en un punto."""
        if not (0 <= to_point <= 23):
            return False
        
        owner, count = self.point_owner_count(to_point)
        if owner is None or owner == player_color:
            return True
        return count == 1  # Puede capturar si hay solo 1 ficha rival

    def _is_furthest_checker(self, from_point, color):
        """Verifica si la ficha es la mÃ¡s lejana en casa."""
        if color == 'B':
            # Blancas casa 0-5. La mÃ¡s lejana es idx 5
            for idx in range(from_point + 1, 6):
                if any(c.color() == color for c in self.__points__[idx]):
                    return False
            return True
        else:
            # Negras casa 18-23. La mÃ¡s lejana es idx 18
            for idx in range(18, from_point):
                if any(c.color() == color for c in self.__points__[idx]):
                    return False
            return True

    def can_move(self, from_point, die_value, player_color):
        """Verifica si un movimiento es legal."""
        
        # 1. Verificar que el dado sea vÃ¡lido
        if not (1 <= die_value <= 6):
            return False
        
        # 2. Reingreso desde la barra
        if from_point is None:
            if not self.has_checkers_on_bar(player_color):
                return False
            
            # Blancas reingresan a 19-24 (home del oponente), Negras a 1-6
            # CORREGIDO: Blancas mueven 24→1, reingreso en 19-24 (idx 18-23)
            #            Negras mueven 1→24, reingreso en 1-6 (idx 0-5)
            to_point = 24 - die_value if player_color == 'B' else die_value - 1
            return self._can_land_on(to_point, player_color)
        
        # 3. Verificar que hay ficha en el origen
        if not (0 <= from_point <= 23):
            return False
        
        owner, count = self.point_owner_count(from_point)
        if owner != player_color or count == 0:
            return False
        
        # 4. Calcular destino
        # Blancas: RESTAN (24â†’1), Negras: SUMAN (1â†’24)
        to_point = from_point - die_value if player_color == 'B' else from_point + die_value
        
        # 5. Bearing off
        if (player_color == 'B' and to_point < 0) or (player_color == 'N' and to_point > 23):
            if not self.can_bear_off(player_color):
                return False
            
            distance_to_off = from_point + 1 if player_color == 'B' else 24 - from_point
            
            if die_value == distance_to_off:
                return True
            
            if die_value > distance_to_off:
                return self._is_furthest_checker(from_point, player_color)
            
            return False
        
        # 6. Movimiento normal
        if not (0 <= to_point <= 23):
            return False
        
        return self._can_land_on(to_point, player_color)

    def _handle_capture(self, to_point, player_color):
        """Maneja la captura de fichas."""
        opponent_color = 'N' if player_color == 'B' else 'B'
        owner, count = self.point_owner_count(to_point)
        
        if owner == opponent_color and count == 1:
            captured = self.__points__[to_point].pop()
            self.__bar__[opponent_color].append(captured)

    def move(self, from_point, die_value, player_color):
        """Ejecuta un movimiento."""
        if not self.can_move(from_point, die_value, player_color):
            return False
        
        # 1. Desde la barra
        if from_point is None:
            # CORREGIDO: mismo cálculo que en can_move
            to_point = 24 - die_value if player_color == 'B' else die_value - 1
            checker = self.__bar__[player_color].pop()
            self._handle_capture(to_point, player_color)
            self.__points__[to_point].append(checker)
            return True
        
        # 2. Calcular destino
        to_point = from_point - die_value if player_color == 'B' else from_point + die_value
        
        # 3. Bearing off
        if (player_color == 'B' and to_point < 0) or (player_color == 'N' and to_point > 23):
            checker = self.__points__[from_point].pop()
            self.__off__[player_color] += 1
            return True
        
        # 4. Movimiento normal
        checker = self.__points__[from_point].pop()
        self._handle_capture(to_point, player_color)
        self.__points__[to_point].append(checker)
        return True