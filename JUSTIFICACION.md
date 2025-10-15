# Checker
## class Board:
Representa el tablero de Backgammon con 24 puntos.
Maneja la disposición de las fichas, validación de movimientos, captura de fichas y el bar (fichas capturadas).
    
### def __init__(self):
Inicializa el tablero con 24 puntos vacíos y configura la posición inicial.

### def _put(self, idx, color, n):
Coloca n fichas de un color en un punto específico.

### def _setup(self):
Configura la disposición inicial estándar del backgammon.
 
### def point_owner_count(self, idx):
Obtiene el dueño y cantidad de fichas en un punto.

### def points(self):
Obtiene la lista de todos los puntos del tablero.
    
### def bar(self):
Obtiene el estado actual del bar (fichas capturadas).
    
### def has_checkers_on_bar(self, color):
Verifica si un jugador tiene fichas en el bar.
  
### def can_move(self, from_point, die_value, player_color):
Valida si un movimiento es legal según las reglas del backgammon.

### def _can_land_on(self, point, player_color):
Verifica si se puede aterrizar en un punto específico.
    
### def move(self, from_point, die_value, player_color):
Ejecuta un movimiento en el tablero.

### def _handle_capture(self, point, attacking_color):
Maneja la captura de una ficha enemiga solitaria (blot).

### def get_valid_moves(self, player_color, available_dice):
Obtiene lista de todos los movimientos válidos disponibles.
        
### def has_valid_moves(self, player_color, available_dice):
Verifica si el jugador tiene movimientos válidos disponibles.
