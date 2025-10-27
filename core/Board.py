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
        """Setup estÃƒÂ¡ndar de backgammon.
        Blancas: 24(2), 13(5), 8(3), 6(5)
        Negras: 1(2), 12(5), 17(3), 19(5)
        """
        # ÃƒÂndices 0-based (punto 1 = idx 0, punto 24 = idx 23)
        self._put(0, 'B', 2)    # punto 1
        self._put(11, 'B', 5)   # punto 12
        self._put(16, 'B', 3)   # punto 17
        self._put(18, 'B', 5)   # punto 19
        
        self._put(23, 'N', 2)   # punto 24
        self._put(12, 'N', 5)   # punto 13
        self._put(7, 'N', 3)    # punto 8
        self._put(5, 'N', 5)    # punto 6

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
        """Casa: BLANCAS 19-24 (idx 18-23), NEGRAS 1-6 (idx 0-5)"""
        return range(18, 24) if color == 'B' else range(0, 6)

    def can_bear_off(self, color):
        """Verifica si todas las fichas estÃƒÂ¡n en casa o fuera."""
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
            # Blancas casa 18-23. La mÃ¡s lejana es idx 18
            for idx in range(18, from_point):
                if any(c.color() == color for c in self.__points__[idx]):
                    return False
            return True
        else:
            # Negras casa 0-5. La mÃ¡s lejana es idx 5
            for idx in range(from_point + 1, 6):
                if any(c.color() == color for c in self.__points__[idx]):
                    return False
            return True

    def can_move(self, from_point, die_value, player_color):
        """Verifica si un movimiento es legal."""
        
        # 1. Verificar que el dado sea vÃƒÂ¡lido
        if not (1 <= die_value <= 6):
            return False
        
        # 2. REGLA CRÍTICA: Si hay fichas en el bar, SOLO se puede mover desde el bar
        if self.has_checkers_on_bar(player_color) and from_point is not None:
            return False
        
        # 3. Reingreso desde la barra
        if from_point is None:
            if not self.has_checkers_on_bar(player_color):
                return False
            
            # BLANCAS reingresan en 1-6 (casa oponente)
            # NEGRAS reingresan en 19-24 (casa oponente)
            to_point = die_value - 1 if player_color == 'B' else 24 - die_value
            return self._can_land_on(to_point, player_color)
        
        # 4. Verificar que hay ficha en el origen
        if not (0 <= from_point <= 23):
            return False
        
        owner, count = self.point_owner_count(from_point)
        if owner != player_color or count == 0:
            return False
        
        # 5. Calcular destino
        # Blancas: SUMAN (1â†’24), Negras: RESTAN (24â†’1)
        to_point = from_point + die_value if player_color == 'B' else from_point - die_value
        
        # 6. Bearing off
        if (player_color == 'B' and to_point > 23) or (player_color == 'N' and to_point < 0):
            if not self.can_bear_off(player_color):
                return False
            
            distance_to_off = 24 - from_point if player_color == 'B' else from_point + 1
            
            if die_value == distance_to_off:
                return True
            
            if die_value > distance_to_off:
                return self._is_furthest_checker(from_point, player_color)
            
            return False
        
        # 7. Movimiento normal
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
            to_point = die_value - 1 if player_color == 'B' else 24 - die_value
            checker = self.__bar__[player_color].pop()
            self._handle_capture(to_point, player_color)
            self.__points__[to_point].append(checker)
            return True
        
        # 2. Calcular destino
        to_point = from_point + die_value if player_color == 'B' else from_point - die_value
        
        # 3. Bearing off
        if (player_color == 'B' and to_point > 23) or (player_color == 'N' and to_point < 0):
            checker = self.__points__[from_point].pop()
            self.__off__[player_color] += 1
            return True
        
        # 4. Movimiento normal
        checker = self.__points__[from_point].pop()
        self._handle_capture(to_point, player_color)
        self.__points__[to_point].append(checker)
        return True