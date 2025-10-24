#!/usr/bin/env python3
"""
Backgammon con Pygame - Interfaz gráfica
"""

import pygame
import sys
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
ROJO = (255, 0, 0)

# Constantes del tablero
ANCHO_VENTANA = 1200
ALTO_VENTANA = 1000  # AUMENTADO para que se vean todas las instrucciones
MARGEN = 120  # AUMENTADO para que quepa el área OFF a la izquierda
ANCHO_TABLERO = ANCHO_VENTANA - 2 * MARGEN
ALTO_TABLERO = 600
ANCHO_PUNTO = ANCHO_TABLERO // 14
ALTO_PUNTO = ALTO_TABLERO // 2 - 20
RADIO_FICHA = 25

# Posiciones
TABLERO_X = MARGEN
TABLERO_Y = MARGEN
BAR_X = TABLERO_X + 6 * ANCHO_PUNTO + ANCHO_PUNTO // 2
OFF_X = TABLERO_X - ANCHO_PUNTO - 10  # CORREGIDO: A la IZQUIERDA del tablero
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

    def punto_a_coords(self, idx):
        """Mapea el índice de un punto (0-23) a las coordenadas del centro de su base."""
        
        # CORRECCIÓN: Invertir el orden dentro de cada cuadrante
        
        # Puntos 0-11 van ARRIBA
        if idx in range(0, 6):
            # Arriba, IZQUIERDA - INVERTIDO (0 a la izquierda, 5 a la derecha)
            x = BAR_X + ANCHO_PUNTO + (5 - idx) * ANCHO_PUNTO + ANCHO_PUNTO // 2
            y = TABLERO_Y
        elif idx in range(6, 12):
            # Arriba, DERECHA - INVERTIDO (6 a la derecha, 11 a la izquierda)
            x = TABLERO_X + (11 - idx) * ANCHO_PUNTO + ANCHO_PUNTO // 2
            y = TABLERO_Y
        
        # Puntos 12-23 van ABAJO
        elif idx in range(12, 18):
            # Abajo, DERECHA - INVERTIDO (12 a la izquierda, 17 a la derecha)
            x = TABLERO_X + (idx - 12) * ANCHO_PUNTO + ANCHO_PUNTO // 2
            y = TABLERO_Y + ALTO_TABLERO
        elif idx in range(18, 24):
            # Abajo, IZQUIERDA - INVERTIDO (18 a la derecha, 23 a la izquierda)
            x = BAR_X + ANCHO_PUNTO + (idx - 18) * ANCHO_PUNTO + ANCHO_PUNTO // 2
            y = TABLERO_Y + ALTO_TABLERO
        else:
            return None
        return x, y

    def coords_a_punto(self, x, y):
        """Mapea coordenadas de click al índice de un punto (0-23)."""
        x_rel = x - TABLERO_X
        y_rel = y - TABLERO_Y

        if not (0 <= y_rel <= ALTO_TABLERO):
            return None

        # Determinar si está arriba o abajo
        if y_rel < ALTO_TABLERO // 2:  # Arriba (puntos 0-11)
            if x_rel < 6 * ANCHO_PUNTO:  # Lado DERECHO (6-11)
                col = x_rel // ANCHO_PUNTO
                idx = 11 - col  # INVERTIDO
            elif x_rel > 6 * ANCHO_PUNTO + ANCHO_PUNTO:  # Lado IZQUIERDO (0-5)
                col = (x_rel - ANCHO_PUNTO * 7) // ANCHO_PUNTO
                idx = 5 - col  # INVERTIDO
            else:
                return None  # Barra
                
        else:  # Abajo (puntos 12-23)
            if x_rel < 6 * ANCHO_PUNTO:  # Lado DERECHO (12-17)
                col = x_rel // ANCHO_PUNTO
                idx = 12 + col  # Normal
            elif x_rel > 6 * ANCHO_PUNTO + ANCHO_PUNTO:  # Lado IZQUIERDO (18-23)
                col = (x_rel - ANCHO_PUNTO * 7) // ANCHO_PUNTO
                idx = 18 + col  # Normal
            else:
                return None  # Barra
                
        # Verificar que el click esté dentro del triángulo
        if (0 <= y_rel <= ALTO_PUNTO or ALTO_TABLERO - ALTO_PUNTO <= y_rel <= ALTO_TABLERO):
            return idx
        return None
    
    def es_area_bar(self, x, y):
        """Verifica si el click está en el área de la barra."""
        return BAR_X - ANCHO_PUNTO // 2 <= x <= BAR_X + ANCHO_PUNTO // 2 and \
               TABLERO_Y <= y <= TABLERO_Y + ALTO_TABLERO

    def es_area_off(self, x, y):
        """Verifica si el click está en el área de retirada (Off)."""
        return OFF_X <= x <= OFF_X + OFF_WIDTH and \
               TABLERO_Y <= y <= TABLERO_Y + ALTO_TABLERO

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
            
            # Puntos 0-11 están arriba, apuntando hacia ABAJO
            if i in range(0, 12):
                puntos = [(x - ANCHO_PUNTO // 2, y),  # Base izquierda
                          (x + ANCHO_PUNTO // 2, y),  # Base derecha
                          (x, y + ALTO_PUNTO)]        # Punta hacia abajo
            else:  # Puntos 12-23 están abajo, apuntando hacia ARRIBA
                puntos = [(x - ANCHO_PUNTO // 2, y),  # Base izquierda
                          (x + ANCHO_PUNTO // 2, y),  # Base derecha
                          (x, y - ALTO_PUNTO)]        # Punta hacia arriba
            
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
            stack = self.game.board().points()[i]
            
            for j, checker in enumerate(stack):
                color = BLANCO if checker.color() == 'B' else NEGRO
                
                # Calcular posición Y de la ficha
                if i in range(0, 12):  # Arriba (stack crece hacia abajo)
                    y_centro = y + ALTO_PUNTO - RADIO_FICHA - j * 2 * RADIO_FICHA
                else:  # Abajo (stack crece hacia arriba)
                    y_centro = y - ALTO_PUNTO + RADIO_FICHA + j * 2 * RADIO_FICHA
                
                pygame.draw.circle(self.screen, color, (int(x), int(y_centro)), RADIO_FICHA)
                pygame.draw.circle(self.screen, MARRON_OSCURO, (int(x), int(y_centro)), RADIO_FICHA, 2)

        # Dibujar fichas en la Barra
        bar = self.game.board().bar()
        # CORRECCIÓN: Fichas blancas en la barra (arriba, lado izquierdo de la barra)
        if bar['B']:
            for j, _ in enumerate(bar['B']):
                y_centro = TABLERO_Y + 30 + j * 2 * RADIO_FICHA
                x_centro = BAR_X - 20  # Lado izquierdo de la barra
                pygame.draw.circle(self.screen, BLANCO, (int(x_centro), int(y_centro)), RADIO_FICHA)
                pygame.draw.circle(self.screen, MARRON_OSCURO, (int(x_centro), int(y_centro)), RADIO_FICHA, 2)
        
        # CORRECCIÓN: Fichas negras en la barra (abajo, lado izquierdo de la barra)        
        if bar['N']:
            for j, _ in enumerate(bar['N']):
                y_centro = TABLERO_Y + ALTO_TABLERO - 30 - j * 2 * RADIO_FICHA
                x_centro = BAR_X - 20  # Lado izquierdo de la barra
                pygame.draw.circle(self.screen, NEGRO, (int(x_centro), int(y_centro)), RADIO_FICHA)
                pygame.draw.circle(self.screen, MARRON_OSCURO, (int(x_centro), int(y_centro)), RADIO_FICHA, 2)

        # Dibujar fichas retiradas
        off = self.game.board().off()
        if off['B']:
            for j in range(min(off['B'], 15)):
                y_centro = TABLERO_Y + 30 + j * 2 * RADIO_FICHA
                pygame.draw.circle(self.screen, BLANCO, (int(OFF_X + OFF_WIDTH // 2), int(y_centro)), RADIO_FICHA)
                pygame.draw.circle(self.screen, MARRON_OSCURO, (int(OFF_X + OFF_WIDTH // 2), int(y_centro)), RADIO_FICHA, 2)
        
        if off['N']:
            for j in range(min(off['N'], 15)):
                y_centro = TABLERO_Y + ALTO_TABLERO - 30 - j * 2 * RADIO_FICHA
                pygame.draw.circle(self.screen, NEGRO, (int(OFF_X + OFF_WIDTH // 2), int(y_centro)), RADIO_FICHA)
                pygame.draw.circle(self.screen, MARRON_OSCURO, (int(OFF_X + OFF_WIDTH // 2), int(y_centro)), RADIO_FICHA, 2)

    def dibujar_dados(self):
        """Dibuja los dados en fila horizontal debajo del tablero."""
        dice = self.game.dice()
        disponibles = self.game.available_dice()
        
        if dice:
            dado_size = 50
            espacio_entre_dados = 15
            total_width = len(dice) * dado_size + (len(dice) - 1) * espacio_entre_dados
            x_base = ANCHO_VENTANA // 2 - total_width // 2
            y_base = TABLERO_Y + ALTO_TABLERO + 50
            
            for i, die_val in enumerate(dice):
                x = x_base + i * (dado_size + espacio_entre_dados)
                y = y_base
                
                die_color = VERDE if die_val in disponibles else GRIS
                
                pygame.draw.rect(self.screen, die_color, (x, y, dado_size, dado_size), 0, 5)
                pygame.draw.rect(self.screen, NEGRO, (x, y, dado_size, dado_size), 2, 5)
                
                text_dado = self.font.render(str(die_val), True, NEGRO)
                text_rect = text_dado.get_rect(center=(x + dado_size // 2, y + dado_size // 2))
                self.screen.blit(text_dado, text_rect)
                
    def dibujar_info(self):
        """Muestra información del turno y el juego."""
        color_turno = "BLANCAS" if self.game.turno() == 'B' else "NEGRAS"
        color_rgb = BLANCO if self.game.turno() == 'B' else NEGRO

        # Instrucciones dinámicas arriba
        if not self.game.dice():
            text_instruccion = self.font.render("Presiona ESPACIO para tirar dados", True, AZUL)
            rect_instruccion = text_instruccion.get_rect(center=(ANCHO_VENTANA // 2, TABLERO_Y - 20))
            self.screen.blit(text_instruccion, rect_instruccion)
        elif self.punto_seleccionado is None and self.game.dice():
            text_instruccion = self.font.render("Selecciona una de tus fichas", True, VERDE)
            rect_instruccion = text_instruccion.get_rect(center=(ANCHO_VENTANA // 2, TABLERO_Y - 20))
            self.screen.blit(text_instruccion, rect_instruccion)
        elif self.punto_seleccionado is not None:
            text_instruccion = self.font.render("Ahora selecciona el destino", True, VERDE)
            rect_instruccion = text_instruccion.get_rect(center=(ANCHO_VENTANA // 2, TABLERO_Y - 20))
            self.screen.blit(text_instruccion, rect_instruccion)
        elif self.game.can_end_turn():
            text_instruccion = self.font.render("Presiona ESPACIO para terminar turno", True, AZUL)
            rect_instruccion = text_instruccion.get_rect(center=(ANCHO_VENTANA // 2, TABLERO_Y - 20))
            self.screen.blit(text_instruccion, rect_instruccion)
        
        # Info de retiradas y turno
        off_B = self.game.board().off()['B']
        off_N = self.game.board().off()['N']
        text_off = self.font.render(f"Retiradas - B: {off_B} | N: {off_N}", True, MARRON_OSCURO)
        self.screen.blit(text_off, (ANCHO_VENTANA - text_off.get_width() - 20, TABLERO_Y + ALTO_TABLERO + 120))

        text_turno = self.font.render(f"Turno: {color_turno}", True, color_rgb)
        self.screen.blit(text_turno, (20, TABLERO_Y + ALTO_TABLERO + 120))

        # Instrucciones
        font_pequeña = pygame.font.Font(None, 28)
        instrucciones = [
            "CÓMO JUGAR:",
            "1. Presiona ESPACIO para tirar los dados",
            "2. Haz CLICK en una de tus fichas (origen)",
            "3. Haz CLICK en el punto de destino",
            "4. El juego usa automáticamente el dado correcto",
            "• Dados VERDES = disponibles | Dados GRISES = ya usados",
            "• Blancas mueven de derecha a izquierda (23→0)",
            "• Negras mueven de izquierda a derecha (0→23)",
        ]
        
        y_inicial = TABLERO_Y + ALTO_TABLERO + 160
        for i, linea in enumerate(instrucciones):
            if i == 0:
                color_texto = MARRON_OSCURO
                font_usada = self.font
            else:
                color_texto = NEGRO
                font_usada = font_pequeña
            text_inst = font_usada.render(linea, True, color_texto)
            self.screen.blit(text_inst, (20, y_inicial + i * 32))

        # Mensaje de victoria
        if self.game.is_game_over():
            ganador = "BLANCAS" if self.game.winner() == 'B' else "NEGRAS"
            text_ganador = self.font.render(f"¡JUEGO TERMINADO! GANADOR: {ganador}", True, ROJO)
            self.screen.blit(text_ganador, (ANCHO_VENTANA // 2 - text_ganador.get_width() // 2, 10))

    def manejar_espacio(self):
        """Maneja la tecla ESPACIO para tirar dados o terminar turno."""
        if self.game.is_game_over():
            return
            
        if not self.game.dice():
            self.game.roll()
            self.punto_seleccionado = None
        elif not self.game.available_dice() or not self.game.has_valid_moves():
            if self.game.can_end_turn():
                self.game.end_turn()
                self.punto_seleccionado = None

    def manejar_click_punto(self, x, y):
        """Maneja el click en los puntos del tablero."""
        
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
            self.punto_seleccionado = None
            return

        # Si NO hay ficha seleccionada, intentar seleccionar
        if self.punto_seleccionado is None:
            # Verificar que hay una ficha del jugador actual
            if punto_idx == "bar":
                if self.game.board().has_checkers_on_bar(self.game.turno()):
                    self.punto_seleccionado = "bar"
            elif punto_idx in range(24):
                owner, count = self.game.board().point_owner_count(punto_idx)
                # CORRECCIÓN CRÍTICA: Solo permite seleccionar fichas del turno actual
                if owner == self.game.turno() and count > 0:
                    self.punto_seleccionado = punto_idx
            return
        
        # Si YA hay ficha seleccionada, intentar mover
        origen = self.punto_seleccionado
        destino = punto_idx
        
        # CORRECCIÓN: Calcular la distancia y encontrar el dado correcto
        movimiento_realizado = False
        
        # Intentar con cada dado disponible
        for die_val in self.game.available_dice():
            # Verificar si este dado permite el movimiento
            if origen == "bar":
                # Movimiento desde la barra
                if self.game.can_move(None, die_val):
                    # Calcular destino esperado
                    destino_esperado = 24 - die_val if self.game.turno() == 'B' else die_val - 1
                    if destino == destino_esperado:
                        if self.game.move(None, die_val):
                            movimiento_realizado = True
                            break
            elif destino == 24:
                # Bearing off (retirada)
                if self.game.can_move(origen, die_val):
                    if self.game.move(origen, die_val):
                        movimiento_realizado = True
                        break
            elif destino in range(24):
                # Movimiento normal
                # CORRECCIÓN: Calcular la distancia según la dirección del jugador
                if self.game.turno() == 'B':
                    # Blancas mueven de 23 -> 0 (restando)
                    distancia = origen - destino
                else:
                    # Negras mueven de 0 -> 23 (sumando)
                    distancia = destino - origen
                
                # Verificar que la distancia sea positiva y coincida con un dado
                if distancia > 0 and distancia == die_val:
                    if self.game.can_move(origen, die_val):
                        if self.game.move(origen, die_val):
                            movimiento_realizado = True
                            break
        
        if movimiento_realizado:
            self.punto_seleccionado = None
        else:
            # Si no se pudo mover, deseleccionar
            self.punto_seleccionado = None

    def run(self):
        """Bucle principal de Pygame."""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.manejar_espacio()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
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
                    
                    if self.punto_seleccionado in range(0, 12):
                        y_center = y + ALTO_PUNTO - RADIO_FICHA
                    else:
                        y_center = y - ALTO_PUNTO + RADIO_FICHA
                        
                    pygame.draw.circle(self.screen, VERDE, (int(x), int(y_center)), RADIO_FICHA + 3, 3)
            
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