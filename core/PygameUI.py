#!/usr/bin/env python3
"""
Backgammon con Pygame - Interfaz gráfica
"""

import pygame
import sys
# Asegúrate de que este import sea correcto para tu estructura de carpetas
from core.BackgammonGame import BackgammonGame

# Constantes de colores
BEIGE = (245, 222, 179)
MARRON_CLARO = (210, 180, 140)
MARRON_OSCURO = (139, 90, 43)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (34, 139, 34)
AZUL = (70, 130, 180)
GRIS = (128, 128, 128)
ROJO = (255, 0, 0) # Para resaltar el área OFF

# Constantes del tablero
ANCHO_VENTANA = 1200
ALTO_VENTANA = 800
MARGEN = 50
ANCHO_TABLERO = ANCHO_VENTANA - 2 * MARGEN
ALTO_TABLERO = 600
ANCHO_PUNTO = ANCHO_TABLERO // 14
ALTO_PUNTO = ALTO_TABLERO // 2 - 20
RADIO_FICHA = 25

# Posiciones
TABLERO_X = MARGEN
TABLERO_Y = MARGEN
BAR_X = TABLERO_X + 6 * ANCHO_PUNTO + ANCHO_PUNTO // 2
OFF_X = TABLERO_X + ANCHO_TABLERO - ANCHO_PUNTO + 10 # Área a la derecha de los últimos puntos
OFF_WIDTH = ANCHO_PUNTO - 20

class BackgammonUI:
    def __init__(self, nombre1="Blancas", nombre2="Negras"):
        pygame.init()
        self.game = BackgammonGame(nombre1, nombre2)
        self.screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Backgammon")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.punto_seleccionado = None
        self.movimientos_validos = []

    # --- Ayudantes de Coordenadas ---

    def punto_a_coords(self, idx):
        """Mapea el índice de un punto (0-23) a las coordenadas del centro de su base."""
        if idx in range(0, 6):
            # Abajo, izquierda
            x = TABLERO_X + (5 - idx) * ANCHO_PUNTO + ANCHO_PUNTO // 2
            y = TABLERO_Y + ALTO_TABLERO
        elif idx in range(6, 12):
            # Abajo, derecha (salta la barra)
            x = BAR_X + ANCHO_PUNTO + (11 - idx) * ANCHO_PUNTO + ANCHO_PUNTO // 2
            y = TABLERO_Y + ALTO_TABLERO
        elif idx in range(12, 18):
            # Arriba, derecha
            x = BAR_X + ANCHO_PUNTO + (idx - 12) * ANCHO_PUNTO + ANCHO_PUNTO // 2
            y = TABLERO_Y
        elif idx in range(18, 24):
            # Arriba, izquierda
            x = TABLERO_X + (idx - 18) * ANCHO_PUNTO + ANCHO_PUNTO // 2
            y = TABLERO_Y
        else:
            return None
        return x, y

    def coords_a_punto(self, x, y):
        """Mapea coordenadas de click al índice de un punto (0-23)."""
        x_rel = x - TABLERO_X
        y_rel = y - TABLERO_Y

        if not (0 <= y_rel <= ALTO_TABLERO):
            return None

        # Determinar el cuadrante (arriba/abajo)
        if y_rel < ALTO_TABLERO // 2: # Arriba
            # Calcular columna
            if x_rel < 6 * ANCHO_PUNTO: # Arriba Izquierda (18-23)
                col = x_rel // ANCHO_PUNTO
                idx = 18 + col
            elif x_rel > 6 * ANCHO_PUNTO + ANCHO_PUNTO: # Arriba Derecha (12-17)
                col = (x_rel - ANCHO_PUNTO * 7) // ANCHO_PUNTO
                idx = 12 + col
            else:
                return None # Barra
            
        else: # Abajo
            # Calcular columna
            if x_rel < 6 * ANCHO_PUNTO: # Abajo Izquierda (0-5)
                col = x_rel // ANCHO_PUNTO
                idx = 5 - col
            elif x_rel > 6 * ANCHO_PUNTO + ANCHO_PUNTO: # Abajo Derecha (6-11)
                col = (x_rel - ANCHO_PUNTO * 7) // ANCHO_PUNTO
                idx = 11 - col
            else:
                return None # Barra
                
        # Verificar que el click esté cerca de la base del triángulo
        if (0 <= y_rel <= ALTO_PUNTO or ALTO_TABLERO - ALTO_PUNTO <= y_rel <= ALTO_TABLERO):
            return idx
        return None
    
    def es_area_dados(self, x, y):
        """Verifica si el click está en el área de dados (alrededor de la barra)."""
        DADO_AREA_X = BAR_X - 60
        DADO_AREA_Y = TABLERO_Y + ALTO_TABLERO // 2 - 25 
        DADO_AREA_WIDTH = 140
        DADO_AREA_HEIGHT = 70
        
        return DADO_AREA_X <= x <= DADO_AREA_X + DADO_AREA_WIDTH and \
               DADO_AREA_Y <= y <= DADO_AREA_Y + DADO_AREA_HEIGHT
               
    def es_area_bar(self, x, y):
        """Verifica si el click está en el área de la barra."""
        return BAR_X - ANCHO_PUNTO // 2 <= x <= BAR_X + ANCHO_PUNTO // 2 and \
               TABLERO_Y <= y <= TABLERO_Y + ALTO_TABLERO

    def es_area_off(self, x, y):
        """Verifica si el click está en el área de retirada (Off)."""
        return OFF_X <= x <= OFF_X + OFF_WIDTH and \
               TABLERO_Y <= y <= TABLERO_Y + ALTO_TABLERO

    def punto_idx_a_die(self, idx):
        """Calcula el valor del dado para el reingreso desde la barra"""
        if self.game.turno() == 'B':
            return idx + 1 # B reingresa al punto 0 con dado 1, al 5 con dado 6.
        else: # 'N'
            return 24 - idx # N reingresa al punto 23 con dado 1, al 18 con dado 6.
        
    # --- Métodos de Dibujo ---

    def dibujar_tablero(self):
        """Dibuja el marco y los triángulos del tablero."""
        self.screen.fill(BEIGE)
        
        # Marco del tablero
        pygame.draw.rect(self.screen, MARRON_OSCURO, 
                         (TABLERO_X, TABLERO_Y, ANCHO_TABLERO, ALTO_TABLERO), 5)

        # Triángulos (puntos)
        for i in range(24):
            x, y = self.punto_a_coords(i)
            color_punto = MARRON_CLARO if i % 2 == 0 else MARRON_OSCURO
            
            # Ajustar coordenadas para Pygame
            if i in range(0, 12): # Abajo (base en y=ALTO_TABLERO)
                puntos = [(x, y), 
                          (x - ANCHO_PUNTO // 2, y - ALTO_PUNTO), 
                          (x + ANCHO_PUNTO // 2, y - ALTO_PUNTO)]
            else: # Arriba (base en y=TABLERO_Y)
                puntos = [(x, y), 
                          (x - ANCHO_PUNTO // 2, y + ALTO_PUNTO), 
                          (x + ANCHO_PUNTO // 2, y + ALTO_PUNTO)]
            
            pygame.draw.polygon(self.screen, color_punto, puntos)

        # Barra Central
        pygame.draw.line(self.screen, MARRON_OSCURO, 
                         (BAR_X, TABLERO_Y), (BAR_X, TABLERO_Y + ALTO_TABLERO), ANCHO_PUNTO)
        
        # Área de Retirada (Off)
        pygame.draw.rect(self.screen, GRIS, 
                         (OFF_X, TABLERO_Y, OFF_WIDTH, ALTO_TABLERO), 0)
        pygame.draw.rect(self.screen, MARRON_OSCURO, 
                         (OFF_X, TABLERO_Y, OFF_WIDTH, ALTO_TABLERO), 3)

    def dibujar_fichas(self):
        """Dibuja las fichas en el tablero, la barra y el área de retirada."""
        
        # Dibujar fichas en los puntos
        for i in range(24):
            x, y = self.punto_a_coords(i)
            stack = self.game.board().points()[i] # Usar points() corregido
            
            for j, checker in enumerate(stack):
                color = BLANCO if checker.color() == 'B' else NEGRO
                
                # Calcular posición Y de la ficha
                if i in range(0, 12): # Abajo (stack crece hacia arriba)
                    # y - ALTO_TABLERO (base) + 20 (borde) + radio + j * 2 * radio
                    y_centro = y - ALTO_PUNTO + RADIO_FICHA + j * 2 * RADIO_FICHA
                else: # Arriba (stack crece hacia abajo)
                    # y + ALTO_PUNTO (borde) - radio - j * 2 * radio
                    y_centro = y + ALTO_PUNTO - RADIO_FICHA - j * 2 * RADIO_FICHA
                
                pygame.draw.circle(self.screen, color, (int(x), int(y_centro)), RADIO_FICHA)
                pygame.draw.circle(self.screen, MARRON_OSCURO, (int(x), int(y_centro)), RADIO_FICHA, 2)
        
        # Dibujar fichas en la barra
        bar = self.game.board().bar()
        # Blancas (arriba)
        for i, _ in enumerate(bar['B']):
            y_centro = TABLERO_Y + RADIO_FICHA + i * 2 * RADIO_FICHA
            pygame.draw.circle(self.screen, BLANCO, (BAR_X, int(y_centro)), RADIO_FICHA)
            pygame.draw.circle(self.screen, MARRON_OSCURO, (BAR_X, int(y_centro)), RADIO_FICHA, 2)
        # Negras (abajo)
        for i, _ in enumerate(bar['N']):
            y_centro = TABLERO_Y + ALTO_TABLERO - RADIO_FICHA - i * 2 * RADIO_FICHA
            pygame.draw.circle(self.screen, NEGRO, (BAR_X, int(y_centro)), RADIO_FICHA)
            pygame.draw.circle(self.screen, MARRON_OSCURO, (BAR_X, int(y_centro)), RADIO_FICHA, 2)
            
        # Dibujar fichas retiradas (Off)
        off = self.game.board().off()
        # Blancas (arriba)
        for i in range(off['B']):
            y_centro = TABLERO_Y + RADIO_FICHA + i * 2 * RADIO_FICHA
            x_centro = OFF_X + OFF_WIDTH // 2
            pygame.draw.circle(self.screen, BLANCO, (int(x_centro), int(y_centro)), RADIO_FICHA)
            pygame.draw.circle(self.screen, MARRON_OSCURO, (int(x_centro), int(y_centro)), RADIO_FICHA, 2)
        # Negras (abajo)
        for i in range(off['N']):
            y_centro = TABLERO_Y + ALTO_TABLERO - RADIO_FICHA - i * 2 * RADIO_FICHA
            x_centro = OFF_X + OFF_WIDTH // 2
            pygame.draw.circle(self.screen, NEGRO, (int(x_centro), int(y_centro)), RADIO_FICHA)
            pygame.draw.circle(self.screen, MARRON_OSCURO, (int(x_centro), int(y_centro)), RADIO_FICHA, 2)


    def dibujar_dados(self):
        """Dibuja los dados actuales y resalta los disponibles."""
        dados = self.game.dice()
        disponibles = self.game.available_dice()
        
        x_start = BAR_X - 60
        y_start = TABLERO_Y + ALTO_TABLERO // 2 - 25
        
        # Dibujar área de dados
        pygame.draw.rect(self.screen, AZUL, (x_start - 10, y_start - 10, 140, 70), 0)
        text = self.font.render("TIRAR", True, BLANCO)
        self.screen.blit(text, (x_start + 10, y_start + 5))
        
        # Dibujar valores de los dados
        for i, die_val in enumerate(dados):
            
            # Si hay dobles, hay 4 slots. Usamos solo los dos primeros para dibujar el valor
            if i < 2 or (len(dados) > 2 and i == 2):
                x = BAR_X + 20 + (i % 2) * 35 
                y = TABLERO_Y + ALTO_TABLERO // 2 - 10 
                
                # Para resaltar los disponibles, verificamos si el valor de este dado 
                # (en la tirada original) todavía está en available_dice.
                # Nota: Esto es una simplificación visual, la lógica del juego está en BackgammonGame
                die_color = VERDE if die_val in disponibles else GRIS
                
                pygame.draw.rect(self.screen, die_color, (x, y, 30, 30), 0, 5)
                text_dado = self.font.render(str(die_val), True, NEGRO)
                self.screen.blit(text_dado, (x + 5, y + 5))
                
    def dibujar_info(self):
        """Muestra información del turno y el juego."""
        color_turno = "BLANCAS" if self.game.turno() == 'B' else "NEGRAS"
        color_rgb = BLANCO if self.game.turno() == 'B' else NEGRO

        # Información del Turno
        text_turno = self.font.render(f"Turno de: {color_turno}", True, color_rgb)
        self.screen.blit(text_turno, (10, ALTO_VENTANA - 40))
        
        # Puntuación de Fichas Retiradas (Off)
        off_B = self.game.board().off()['B']
        off_N = self.game.board().off()['N']
        text_off = self.font.render(f"Retiradas - B: {off_B} | N: {off_N}", True, MARRON_OSCURO)
        self.screen.blit(text_off, (ANCHO_VENTANA - text_off.get_width() - 10, ALTO_VENTANA - 40))

        # Mensaje de Final de Juego
        if self.game.is_game_over():
            ganador = "BLANCAS" if self.game.winner() == 'B' else "NEGRAS"
            text_ganador = self.font.render(f"¡JUEGO TERMINADO! GANADOR: {ganador}", True, ROJO)
            self.screen.blit(text_ganador, (ANCHO_VENTANA // 2 - text_ganador.get_width() // 2, 10))

    # --- LÓGICA DE EVENTOS ---
    
    def manejar_click_dado(self, x, y):
        """Maneja el click sobre el área de dados y tira/termina turno."""
        
        if self.game.is_game_over():
            return
            
        # 1. Tirar dados si es el inicio del turno
        if not self.game.dice():
            self.game.roll()
            self.punto_seleccionado = None
            
        # 2. Terminar turno si ya se tiró y no quedan movimientos válidos
        elif not self.game.available_dice() or not self.game.has_valid_moves():
            if self.game.can_end_turn():
                self.game.end_turn()
            
        else:
            # Si ya se tiró y quedan movimientos, el click no hace nada
            pass

    def manejar_click_punto(self, x, y):
        """Maneja el click en los puntos del tablero, la barra o el área de retirada."""
        
        punto_idx = self.coords_a_punto(x, y)
        if punto_idx is None:
            if self.es_area_bar(x, y):
                punto_idx = "bar"
            elif self.es_area_off(x, y):
                punto_idx = 24 
            else:
                self.punto_seleccionado = None
                return

        if not self.game.dice():
            # No se puede mover antes de tirar
            self.punto_seleccionado = None
            return

        # Si hay ficha seleccionada (Origen)
        if self.punto_seleccionado is not None:
            origen = self.punto_seleccionado
            destino = punto_idx
            
            # Buscar un dado válido para esta transición
            valid_moves = self.game.get_valid_moves()
            found_die = None
            
            for src, die in valid_moves:
                
                # Checkear movimientos normales o desde la barra
                if origen in range(24) and destino in range(24):
                    if src == origen and abs(origen - destino) == die:
                        found_die = die
                        break
                elif origen == "bar" and destino in range(24):
                    if src == None and (destino + 1 == die if self.game.turno() == 'B' else 24 - destino == die):
                        found_die = die
                        break
                
                # Checkear Bearing Off (Retirada)
                elif origen in range(24) and destino == 24:
                    if src == origen and die not in range(1, 7) and self.game.can_move(origen, die, destino): 
                        # can_move a 24 retorna True solo si die_value es suficiente
                        # Al hacer move, pasamos el die_value que can_move validó.
                        # Para la UI, simplemente chequeamos que exista un movimiento válido desde origen a 24
                        found_die = die
                        break
                        
            # Ejecutar el movimiento
            if found_die is not None:
                if self.game.move(origen, found_die):
                    self.punto_seleccionado = None
                else:
                    self.punto_seleccionado = destino
            else:
                # Movimiento inválido, deseleccionar o seleccionar el nuevo punto
                self.punto_seleccionado = destino if destino != self.punto_seleccionado else None
                
        else:
            # Seleccionar ficha (Origen)
            if punto_idx in range(24):
                 owner, count = self.game.board().point_owner_count(punto_idx)
                 if owner == self.game.turno() and count > 0:
                     self.punto_seleccionado = punto_idx
                 else:
                     self.punto_seleccionado = None
            elif punto_idx == "bar":
                 if self.game.board().has_checkers_on_bar(self.game.turno()):
                     self.punto_seleccionado = "bar"
                 else:
                     self.punto_seleccionado = None
            elif punto_idx == 24:
                # Se selecciona el área OFF si se intenta retirar
                self.punto_seleccionado = 24

    def run(self):
        """Bucle principal de Pygame."""
        running = True
        
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.es_area_dados(x, y):
                        self.manejar_click_dado(x, y)
                    else:
                        self.manejar_click_punto(x, y)

            self.dibujar_tablero()
            self.dibujar_fichas()
            self.dibujar_dados()
            self.dibujar_info()
            
            # Resaltar la selección
            
            if self.punto_seleccionado == "bar":
                pygame.draw.rect(self.screen, VERDE, 
                               (BAR_X - ANCHO_PUNTO // 4, TABLERO_Y,
                                ANCHO_PUNTO // 2, ALTO_TABLERO), 4)
                                
            elif self.punto_seleccionado is not None and self.punto_seleccionado != 24:
                coords = self.punto_a_coords(self.punto_seleccionado)
                if coords:
                    x, y = coords
                    stack_size = len(self.game.board().points()[self.punto_seleccionado])
                    
                    # Calcular el centro de la ficha más alta
                    if 12 <= self.punto_seleccionado <= 23:
                        # Puntos superiores (el stack crece hacia abajo)
                        y_center = y + ALTO_PUNTO - RADIO_FICHA
                    else:
                        # Puntos inferiores (el stack crece hacia arriba)
                        y_center = y - ALTO_PUNTO + RADIO_FICHA
                        
                    # Dibuja el círculo selector centrado en la ficha superior:
                    pygame.draw.circle(self.screen, VERDE, (int(x), int(y_center)), RADIO_FICHA + 3, 3)
            
            # Resaltar el área de retirada si está seleccionada
            elif self.punto_seleccionado == 24:
                 pygame.draw.rect(self.screen, VERDE, 
                         (OFF_X, TABLERO_Y, OFF_WIDTH, ALTO_TABLERO), 4)

            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


def main():
    print("\n=== BACKGAMMON ===\n")
    nombre1 = input("Nombre jugador BLANCAS (Enter = 'Blancas'): ").strip() or "Blancas"
    nombre2 = input("Nombre jugador NEGRAS (Enter = 'Negras'): ").strip() or "Negras"
    
    ui = BackgammonUI(nombre1, nombre2)
    ui.run()


if __name__ == "__main__":
    main()