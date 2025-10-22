from .Checker import Checker

class Board:
    def __init__(self):
        self.__points__ = [[] for _ in range(24)]
        self.__bar__ = {"B": [], "N": []} 
        self.__off__ = {"B": 0, "N": 0} # Nueva métrica para fichas retiradas
        self._setup()

    def _put(self, idx, color, n):
        for _ in range(n):
            self.__points__[idx].append(Checker(color))

    def _setup(self):
        """Setup estándar de backgammon (USANDO LA CONVENCIÓN DE TU CÓDIGO)"""
        # Blancas (B) - Mueven del 23 al 0 (Hacia abajo)
        self._put(23, 'B', 5)  
        self._put(19, 'N', 3)  
        self._put(16, 'N', 5)  
        self._put(12, 'B', 2)  
        
        # Negras (N) - Mueven del 0 al 23 (Hacia arriba)
        self._put(0, 'N', 5)   
        self._put(4, 'B', 3)   
        self._put(7, 'B', 5)   
        self._put(11, 'N', 2)  

    def off(self):
        return dict(self.__off__)

    def bar(self):
        return dict(self.__bar__)

    def point_owner_count(self, idx):
        stack = self.__points__[idx]
        if not stack:
            return None, 0
        return stack[0].color(), len(stack)

    def points(self):
        return self.__points__
    
    def has_checkers_on_bar(self, color):
        return len(self.__bar__[color]) > 0
    
    # --- Lógica de Bearing Off (Retirada) ---
    
    def _get_home_range(self, color):
        """Retorna el rango de índices domésticos (adaptado a tu convención)."""
        # B mueve 23->0: Casa 0-5. N mueve 0->23: Casa 18-23.
        return range(0, 6) if color == 'B' else range(18, 24) 
        
    def can_bear_off(self, color):
        """Verifica si todas las fichas del jugador están en casa o retiradas."""
        if self.has_checkers_on_bar(color):
            return False
            
        home_range = self._get_home_range(color)
        
        for idx in range(24):
            if idx not in home_range:
                # Si encuentra una ficha del color en cualquier punto fuera de casa, no puede retirar.
                if any(c.color() == color for c in self.__points__[idx]):
                    return False
        
        return True
    
    def _is_furthest_checker(self, from_point, color):
        """Verifica si la ficha es la más lejana en el cuadrante doméstico (para dado excedente)."""
        
        if color == 'B':
            # B mueve 23->0. La más lejana es la de mayor índice (5) en el rango 0-5
            for idx in range(from_point + 1, 6):
                if any(c.color() == color for c in self.__points__[idx]):
                    return False
            return True
        
        else: # color == 'N'
            # N mueve 0->23. La más lejana es la de menor índice (18) en el rango 18-23
            for idx in range(18, from_point):
                if any(c.color() == color for c in self.__points__[idx]):
                    return False
            return True


    # --- Lógica de Movimiento (Adaptada) ---

    def can_move(self, from_point, die_value, player_color):
        
        # 1. Bloqueo por Bar
        if self.has_checkers_on_bar(player_color) and from_point is not None:
            return False
        
        # 2. Reingreso desde el Bar
        if from_point is None:
            if not self.has_checkers_on_bar(player_color):
                return False
            
            # B (23->0) reingresa a 18-23. N (0->23) reingresa a 0-5.
            to_point = 24 - die_value if player_color == 'B' else die_value - 1
            
            return self._can_land_on(to_point, player_color) # Usa el método de aterrizaje
        
        # 3. Origen no válido (vacío o color incorrecto)
        owner, count = self.point_owner_count(from_point)
        if owner != player_color or count == 0:
            return False
        
        # 4. Calcular destino
        to_point = from_point - die_value if player_color == 'B' else from_point + die_value
        
        # 5. Bearing Off (Retirada)
        if (player_color == 'B' and to_point < 0) or (player_color == 'N' and to_point > 23):
            if not self.can_bear_off(player_color):
                return False # No puede retirar si tiene fichas fuera de casa

            distance_to_off = from_point + 1 if player_color == 'B' else 24 - from_point # Distancia al final
            
            if die_value == distance_to_off:
                return True # Dado exacto
            
            if die_value > distance_to_off:
                # Dado excedente: solo si es la ficha más lejana
                return self._is_furthest_checker(from_point, player_color)
                
            return False # Dado insuficiente
        
        # 6. Movimiento normal (destino en tablero 0-23)
        if not (0 <= to_point <= 23):
            return False
        
        return self._can_land_on(to_point, player_color)
    
    def _can_land_on(self, point, player_color):
        """Verifica si se puede aterrizar en un punto, incluyendo la captura (blot)."""
        owner, count = self.point_owner_count(point)
        
        if owner is None or owner == player_color:
            return True
        
        if count == 1:
            return True # Captura (blot)
        
        return False # Bloqueado (dos o más fichas enemigas)
    
    def move(self, from_point, die_value, player_color):
        """Ejecuta un movimiento, incluyendo reingreso, captura y retirada."""
        
        if not self.can_move(from_point, die_value, player_color):
            return False
        
        # 1. Movimiento desde el bar
        if from_point is None:
            to_point = 24 - die_value if player_color == 'B' else die_value - 1
            checker = self.__bar__[player_color].pop()
            self._handle_capture(to_point, player_color)
            self.__points__[to_point].append(checker)
            return True
        
        # 2. Calcular destino
        to_point = from_point - die_value if player_color == 'B' else from_point + die_value

        # 3. Bearing Off (Retirada)
        if (player_color == 'B' and to_point < 0) or (player_color == 'N' and to_point > 23):
            checker = self.__points__[from_point].pop()
            self.__off__[player_color] += 1
            return True

        # 4. Movimiento normal
        checker = self.__points__[from_point].pop()
        self._handle_capture(to_point, player_color)
        self.__points__[to_point].append(checker)
        
        return True
    
    def _handle_capture(self, point, attacking_color):
        """Maneja la captura de una ficha enemiga"""
        owner, count = self.point_owner_count(point)
        
        if owner is not None and owner != attacking_color and count == 1:
            captured = self.__points__[point].pop()
            self.__bar__[owner].append(captured)
    
    def get_valid_moves(self, player_color, available_dice):
        """Obtiene lista de movimientos válidos"""
        valid_moves = []
        
        # 1. Movimiento obligatorio desde el bar
        if self.has_checkers_on_bar(player_color):
            for die in available_dice:
                if self.can_move(None, die, player_color):
                    valid_moves.append((None, die))
            return valid_moves # Solo se puede mover desde el bar
        
        # 2. Movimientos normales (tablero) o retirada
        for point in range(24):
            owner, count = self.point_owner_count(point)
            
            if owner == player_color and count > 0:
                for die in available_dice:
                    # can_move debe manejar la validez para movimientos normales y retirada.
                    if self.can_move(point, die, player_color):
                        valid_moves.append((point, die))
        
        # Eliminar duplicados si hay dobles
        return list(set(valid_moves))