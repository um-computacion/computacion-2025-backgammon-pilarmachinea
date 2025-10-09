from core import Checker

class Board:
    """
    Representa el tablero de Backgammon con 24 puntos.
    
    Maneja la disposición de las fichas, validación de movimientos,
    captura de fichas y el bar (fichas capturadas).
    """
    
    def __init__(self):
        """
        Inicializa el tablero con 24 puntos vacíos y configura la posición inicial.
        
        Recibe: Nada
        Hace: Crea el tablero con la configuración estándar de backgammon
        Devuelve: Nada
        """
        self.__points__ = [[] for _ in range(24)]
        self.__bar__ = {"B": [], "N": []}
        self._setup()

    def _put(self, idx, color, n):
        """
        Coloca n fichas de un color en un punto específico.
        
        Recibe:
            idx: índice del punto (0-23)
            color: 'B' para blancas o 'N' para negras
            n: cantidad de fichas a colocar
        Hace: Agrega n fichas al punto especificado
        Devuelve: Nada
        """
        for _ in range(n):
            self.__points__[idx].append(Checker(color))

    def _setup(self):
        """
        Configura la disposición inicial estándar del backgammon.
        
        Recibe: Nada
        Hace: Coloca las 15 fichas de cada jugador en sus posiciones iniciales
        Devuelve: Nada
        """
        self._put(23, 'B', 2)  
        self._put(12, 'B', 5)   
        self._put(7,  'B', 3)   
        self._put(5,  'B', 5)   
        
        self._put(0,  'N', 2)   
        self._put(11, 'N', 5)   
        self._put(16, 'N', 3)   
        self._put(18, 'N', 5)   

    def point_owner_count(self, idx):
        """
        Obtiene el dueño y cantidad de fichas en un punto.
        
        Recibe:
            idx: índice del punto (0-23)
        Hace: Consulta el estado del punto especificado
        Devuelve: Tupla (color, cantidad) o (None, 0) si está vacío
        """
        stack = self.__points__[idx]
        if not stack:
            return None, 0
        return stack[0].color(), len(stack)

    def points(self):
        """
        Obtiene la lista de todos los puntos del tablero.
        
        Recibe: Nada
        Hace: Retorna referencia a los puntos del tablero
        Devuelve: Lista con los 24 puntos
        """
        return self.__points__
    
    def bar(self):
        """
        Obtiene el estado actual del bar (fichas capturadas).
        
        Recibe: Nada
        Hace: Crea una copia del diccionario del bar
        Devuelve: Diccionario con claves 'B' y 'N' y listas de fichas capturadas
        """
        return dict(self.__bar__)
    
    def has_checkers_on_bar(self, color):
        """
        Verifica si un jugador tiene fichas en el bar.
        
        Recibe:
            color: 'B' para blancas o 'N' para negras
        Hace: Consulta el bar del jugador especificado
        Devuelve: True si tiene fichas capturadas, False si no
        """
        return len(self.__bar__[color]) > 0
    
    def can_move(self, from_point, die_value, player_color):
        """
        Valida si un movimiento es legal según las reglas del backgammon.
        
        Recibe:
            from_point: punto de origen (0-23) o None si viene del bar
            die_value: valor del dado a usar (1-6)
            player_color: 'B' para blancas o 'N' para negras
        Hace: Verifica todas las condiciones de movimiento válido
        Devuelve: True si el movimiento es válido, False si no
        """
        if self.has_checkers_on_bar(player_color) and from_point is not None:
            return False
        
        if from_point is None:
            if not self.has_checkers_on_bar(player_color):
                return False
            if player_color == 'B':
                to_point = die_value - 1
            else:
                to_point = 24 - die_value
            
            return self._can_land_on(to_point, player_color)
        
        if from_point < 0 or from_point > 23:
            return False
        
        owner, count = self.point_owner_count(from_point)
        if owner != player_color or count == 0:
            return False
        
        if player_color == 'B':
            to_point = from_point - die_value
        else:
            to_point = from_point + die_value
        
        if to_point < 0 or to_point > 23:
            return False
        
        return self._can_land_on(to_point, player_color)
    
    def _can_land_on(self, point, player_color):
        """
        Verifica si se puede aterrizar en un punto específico.
        
        Recibe:
            point: índice del punto destino (0-23)
            player_color: 'B' para blancas o 'N' para negras
        Hace: Verifica si el punto está disponible según las reglas
        Devuelve: True si puede aterrizar, False si no
        """
        if point < 0 or point > 23:
            return False
        
        owner, count = self.point_owner_count(point)
        
        if owner is None:
            return True
        
        if owner == player_color:
            return True
        
        if count == 1:
            return True
        
        return False
    
    def move(self, from_point, die_value, player_color):
        """
        Ejecuta un movimiento en el tablero.
        
        Recibe:
            from_point: punto de origen (0-23) o None si viene del bar
            die_value: valor del dado a usar (1-6)
            player_color: 'B' para blancas o 'N' para negras
        Hace: Mueve la ficha y maneja capturas si aplica
        Devuelve: True si el movimiento fue exitoso, False si no
        """
        if not self.can_move(from_point, die_value, player_color):
            return False
        
        if from_point is None:
            if player_color == 'B':
                to_point = die_value - 1
            else:
                to_point = 24 - die_value
            
            checker = self.__bar__[player_color].pop()
            self._handle_capture(to_point, player_color)
            self.__points__[to_point].append(checker)
            return True
        
        if player_color == 'B':
            to_point = from_point - die_value
        else:
            to_point = from_point + die_value
        
        checker = self.__points__[from_point].pop()
        self._handle_capture(to_point, player_color)
        self.__points__[to_point].append(checker)
        
        return True
    
    def _handle_capture(self, point, attacking_color):
        """
        Maneja la captura de una ficha enemiga solitaria (blot).
        
        Recibe:
            point: índice del punto donde ocurre la captura
            attacking_color: color del jugador que ataca
        Hace: Si hay un blot enemigo, lo captura y lo envía al bar
        Devuelve: Nada
        """
        owner, count = self.point_owner_count(point)
        
        if owner is not None and owner != attacking_color and count == 1:
            captured = self.__points__[point].pop()
            self.__bar__[owner].append(captured)
    
    def get_valid_moves(self, player_color, available_dice):
        """
        Obtiene lista de todos los movimientos válidos disponibles.
        
        Recibe:
            player_color: 'B' para blancas o 'N' para negras
            available_dice: lista de valores de dados disponibles
        Hace: Busca todos los movimientos posibles en el tablero
        Devuelve: Lista de tuplas (from_point, die_value) con movimientos válidos
        """
        valid_moves = []
        
        if self.has_checkers_on_bar(player_color):
            for die in available_dice:
                if self.can_move(None, die, player_color):
                    valid_moves.append((None, die))
            return valid_moves
        
        for point in range(24):
            owner, count = self.point_owner_count(point)
            if owner == player_color and count > 0:
                for die in available_dice:
                    if self.can_move(point, die, player_color):
                        valid_moves.append((point, die))
        
        return valid_moves
    
    def has_valid_moves(self, player_color, available_dice):
        """
        Verifica si el jugador tiene movimientos válidos disponibles.
        
        Recibe:
            player_color: 'B' para blancas o 'N' para negras
            available_dice: lista de valores de dados disponibles
        Hace: Consulta si existen movimientos posibles
        Devuelve: True si hay movimientos válidos, False si no
        """
        return len(self.get_valid_moves(player_color, available_dice)) > 0