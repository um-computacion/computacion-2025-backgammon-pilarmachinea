#!/usr/bin/env python3
"""
Backgammon con Pygame
Interfaz gráfica para el juego de Backgammon
"""

import pygame
import sys
from .BackgammonGame import BackgammonGame

# Constantes de colores
BEIGE = (245, 222, 179)
MARRON_CLARO = (210, 180, 140)
MARRON_OSCURO = (139, 90, 43)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (34, 139, 34)
ROJO = (220, 20, 60)
GRIS = (128, 128, 128)
AZUL = (70, 130, 180)

# Constantes del tablero
ANCHO_VENTANA = 1200
ALTO_VENTANA = 800
MARGEN = 50
ANCHO_TABLERO = ANCHO_VENTANA - 2 * MARGEN
ALTO_TABLERO = 600
ANCHO_PUNTO = ANCHO_TABLERO // 14  # 12 puntos + 2 espacios para el bar
ALTO_PUNTO = ALTO_TABLERO // 2 - 20
RADIO_FICHA = 25

# Posiciones
TABLERO_X = MARGEN
TABLERO_Y = MARGEN
BAR_X = TABLERO_X + 6 * ANCHO_PUNTO + ANCHO_PUNTO // 2


class BackgammonUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Backgammon")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Juego
        self.game = BackgammonGame()
        
        # Estado de UI
        self.punto_seleccionado = None  # None = nada, número = punto, "bar" = bar
        self.dados_tirados = False
        self.mensaje = "Presiona ESPACIO para tirar los dados"
        
    def punto_a_coords(self, punto):
        """Convierte número de punto (0-23) a coordenadas (x, y)
        
        Backgammon estándar (ajustado a 0-23):
        ARRIBA:  23 22 21 20 19 18 | BAR | 17 16 15 14 13 12
        ABAJO:    0  1  2  3  4  5 | BAR |  6  7  8  9 10 11
        
        Las blancas van: 23→22→...→0 (sentido antihorario desde arriba izq)
        Las negras van: 0→1→...→23 (sentido horario desde abajo izq)
        """
        if punto < 0 or punto > 23:
            return None
        
        # Puntos 18-23 (arriba izquierda)
        if 18 <= punto <= 23:
            columna = 23 - punto  # 23->0, 22->1, ..., 18->5
            x = TABLERO_X + columna * ANCHO_PUNTO
            y = TABLERO_Y + 10
            
        # Puntos 12-17 (arriba derecha)
        elif 12 <= punto <= 17:
            columna = 17 - punto  # 17->0, 16->1, ..., 12->5
            x = TABLERO_X + (columna + 7) * ANCHO_PUNTO + ANCHO_PUNTO // 2
            y = TABLERO_Y + 10
            
        # Puntos 0-5 (abajo izquierda)
        elif 0 <= punto <= 5:
            columna = punto  # 0->0, 1->1, ..., 5->5
            x = TABLERO_X + columna * ANCHO_PUNTO
            y = TABLERO_Y + ALTO_TABLERO - ALTO_PUNTO - 10
            
        # Puntos 6-11 (abajo derecha)
        else:  # 6-11
            columna = punto - 6  # 6->0, 7->1, ..., 11->5
            x = TABLERO_X + (columna + 7) * ANCHO_PUNTO + ANCHO_PUNTO // 2
            y = TABLERO_Y + ALTO_TABLERO - ALTO_PUNTO - 10
            
        return (x + ANCHO_PUNTO // 2, y)
    
    def coords_a_punto(self, x, y):
        """Convierte coordenadas de mouse a número de punto
        
        Layout:
        ARRIBA:  23 22 21 20 19 18 | BAR | 17 16 15 14 13 12
        ABAJO:    0  1  2  3  4  5 | BAR |  6  7  8  9 10 11
        """
        if x < TABLERO_X or x > TABLERO_X + ANCHO_TABLERO:
            return None
        if y < TABLERO_Y or y > TABLERO_Y + ALTO_TABLERO:
            return None
        
        x_rel = x - TABLERO_X
        mitad_superior = y < TABLERO_Y + ALTO_TABLERO // 2
        
        columna = x_rel // ANCHO_PUNTO
        if columna > 6:
            columna -= 1
            
        if columna < 0 or columna > 12:
            return None
        
        if mitad_superior:
            # Parte superior (12-23)
            if columna <= 5:
                # Izquierda superior: 18-23
                punto = 23 - columna
            else:
                # Derecha superior: 12-17
                punto = 17 - (columna - 7)
        else:
            # Parte inferior (0-11)
            if columna <= 5:
                # Izquierda inferior: 0-5
                punto = columna
            else:
                # Derecha inferior: 6-11
                punto = 6 + (columna - 7)
            
        return punto if 0 <= punto <= 23 else None
    
    def dibujar_tablero(self):
        """Dibuja el tablero de backgammon"""
        # Fondo
        self.screen.fill(BEIGE)
        
        # Borde del tablero
        pygame.draw.rect(self.screen, MARRON_OSCURO, 
                        (TABLERO_X - 5, TABLERO_Y - 5, 
                         ANCHO_TABLERO + 10, ALTO_TABLERO + 10), 5)
        
        # Fondo del tablero
        pygame.draw.rect(self.screen, MARRON_CLARO,
                        (TABLERO_X, TABLERO_Y, ANCHO_TABLERO, ALTO_TABLERO))
        
        # Bar (centro)
        pygame.draw.rect(self.screen, MARRON_OSCURO,
                        (BAR_X - ANCHO_PUNTO // 4, TABLERO_Y,
                         ANCHO_PUNTO // 2, ALTO_TABLERO))
        
        # Dibujar puntos (triángulos)
        for i in range(24):
            coords = self.punto_a_coords(i)
            if coords:
                x, y = coords
                
                # Color alternado
                color = MARRON_OSCURO if (i % 2 == 0) else BLANCO
                
                # Puntos 12-23: ARRIBA con triángulos hacia ABAJO ▼
                # Puntos 0-11: ABAJO con triángulos hacia ARRIBA ▲
                
                if 12 <= i <= 23:
                    # Parte superior: hacia ABAJO ▼
                    puntos = [
                        (x, y),
                        (x - ANCHO_PUNTO // 2 + 5, y + ALTO_PUNTO),
                        (x + ANCHO_PUNTO // 2 - 5, y + ALTO_PUNTO)
                    ]
                else:  # 0-11
                    # Parte inferior: hacia ARRIBA ▲
                    puntos = [
                        (x, y + ALTO_PUNTO),
                        (x - ANCHO_PUNTO // 2 + 5, y),
                        (x + ANCHO_PUNTO // 2 - 5, y)
                    ]
                
                pygame.draw.polygon(self.screen, color, puntos)
                pygame.draw.polygon(self.screen, NEGRO, puntos, 2)
                
                # Número del punto
                texto = self.font_small.render(str(i), True, GRIS)
                texto_rect = texto.get_rect(center=(x, y + ALTO_PUNTO // 2))
                self.screen.blit(texto, texto_rect)
    
    def dibujar_fichas(self):
        """Dibuja las fichas en el tablero"""
        board = self.game.board()
        
        # Fichas en los puntos
        for i in range(24):
            owner, count = board.point_owner_count(i)
            if count > 0:
                coords = self.punto_a_coords(i)
                if coords:
                    x, y = coords
                    color = BLANCO if owner == 'B' else NEGRO
                    color_borde = NEGRO if owner == 'B' else BLANCO
                    
                    # Fichas se apilan desde la base del triángulo
                    if 12 <= i <= 23:  # Parte superior (triángulos hacia abajo)
                        y_start = y + 15
                        offset = RADIO_FICHA * 2 + 2
                    else:  # 0-11 - Parte inferior (triángulos hacia arriba)
                        y_start = y + ALTO_PUNTO - 15
                        offset = -(RADIO_FICHA * 2 + 2)
                    
                    # Dibujar hasta 5 fichas
                    for j in range(min(count, 5)):
                        y_ficha = y_start + j * offset
                        pygame.draw.circle(self.screen, color, 
                                         (int(x), int(y_ficha)), RADIO_FICHA)
                        pygame.draw.circle(self.screen, color_borde,
                                         (int(x), int(y_ficha)), RADIO_FICHA, 2)
                    
                    # Si hay más de 5, mostrar número
                    if count > 5:
                        texto = self.font_small.render(str(count), True, 
                                                      NEGRO if owner == 'B' else BLANCO)
                        y_ficha = y_start + 4 * offset
                        texto_rect = texto.get_rect(center=(int(x), int(y_ficha)))
                        self.screen.blit(texto, texto_rect)
        
        # Fichas en el bar
        bar = board.bar()
        for color_key in ['B', 'N']:
            count = len(bar[color_key])
            if count > 0:
                color = BLANCO if color_key == 'B' else NEGRO
                color_borde = NEGRO if color_key == 'B' else BLANCO
                
                y_base = TABLERO_Y + 100 if color_key == 'B' else TABLERO_Y + ALTO_TABLERO - 100
                
                for j in range(min(count, 5)):
                    y_ficha = y_base + j * (RADIO_FICHA * 2 + 2)
                    pygame.draw.circle(self.screen, color,
                                     (BAR_X, int(y_ficha)), RADIO_FICHA)
                    pygame.draw.circle(self.screen, color_borde,
                                     (BAR_X, int(y_ficha)), RADIO_FICHA, 2)
    
    def dibujar_dados(self):
        """Dibuja los dados disponibles"""
        dados = self.game.available_dice()
        
        if dados:
            # Centrar los dados horizontalmente
            total_ancho = len(dados) * 60  # 50 de dado + 10 de espacio
            x_start = (ANCHO_VENTANA - total_ancho) // 2
            y_start = TABLERO_Y + ALTO_TABLERO + 50
            
            for i, dado in enumerate(dados):
                x = x_start + i * 60
                y = y_start
                
                # Cuadrado del dado
                pygame.draw.rect(self.screen, BLANCO,
                               (x, y, 50, 50))
                pygame.draw.rect(self.screen, NEGRO,
                               (x, y, 50, 50), 3)
                
                # Número
                texto = self.font.render(str(dado), True, NEGRO)
                texto_rect = texto.get_rect(center=(x + 25, y + 25))
                self.screen.blit(texto, texto_rect)
    
    def dibujar_info(self):
        """Dibuja información del juego"""
        # Turno actual
        player = self.game.current_player()
        color_texto = "BLANCAS" if player.es_blanco() else "NEGRAS"
        
        y_pos = TABLERO_Y + ALTO_TABLERO + 30
        
        texto = self.font.render(f"Turno: {color_texto}", True, NEGRO)
        self.screen.blit(texto, (MARGEN, y_pos))
        
        # Mensaje
        texto_msg = self.font_small.render(self.mensaje, True, AZUL)
        self.screen.blit(texto_msg, (MARGEN, y_pos + 40))
        
        # Instrucciones
        instrucciones = [
            "ESPACIO: Tirar dados",
            "Click: Seleccionar punto",
            "Click dado: Mover ficha",
            "T: Terminar turno",
            "ESC: Salir"
        ]
        
        x_inst = ANCHO_VENTANA - 250
        y_inst = TABLERO_Y + ALTO_TABLERO + 30
        
        for i, inst in enumerate(instrucciones):
            texto = self.font_small.render(inst, True, NEGRO)
            self.screen.blit(texto, (x_inst, y_inst + i * 30))
    
    def manejar_click_punto(self, x, y):
        """Maneja el click en un punto del tablero"""
        # Primero verificar si hizo click en el bar
        if self.click_en_bar(x, y):
            color_actual = 'B' if self.game.current_player().es_blanco() else 'N'
            if self.game.board().has_checkers_on_bar(color_actual):
                if self.punto_seleccionado == "bar":
                    # Deseleccionar bar
                    self.punto_seleccionado = None
                    self.mensaje = "Bar deseleccionado"
                else:
                    # Seleccionar bar
                    self.punto_seleccionado = "bar"
                    self.mensaje = "Bar seleccionado. Click en un dado para mover."
            else:
                self.mensaje = "No tienes fichas en el bar"
            return
        
        # Si no fue en el bar, verificar puntos normales
        punto = self.coords_a_punto(x, y)
        
        if punto is not None:
            if self.punto_seleccionado is None or isinstance(self.punto_seleccionado, str):
                # Seleccionar punto origen
                owner, count = self.game.board().point_owner_count(punto)
                color_actual = 'B' if self.game.current_player().es_blanco() else 'N'
                
                if owner == color_actual and count > 0:
                    self.punto_seleccionado = punto
                    self.mensaje = f"Punto {punto} seleccionado. Click en un dado para mover."
                else:
                    self.mensaje = "No puedes mover desde ese punto"
            else:
                # Deseleccionar
                self.punto_seleccionado = None
                self.mensaje = "Punto deseleccionado"
    
    def click_en_bar(self, x, y):
        """Verifica si el click fue en el bar"""
        bar_izq = BAR_X - ANCHO_PUNTO // 4
        bar_der = BAR_X + ANCHO_PUNTO // 4
        
        if bar_izq <= x <= bar_der and TABLERO_Y <= y <= TABLERO_Y + ALTO_TABLERO:
            return True
        return False
    
    def manejar_click_dado(self, x, y):
        """Maneja el click en un dado"""
        if self.punto_seleccionado is None:
            self.mensaje = "Primero selecciona un punto o el bar"
            return
        
        dados = self.game.available_dice()
        if not dados:
            return
        
        # Calcular posiciones de los dados (centrados)
        total_ancho = len(dados) * 60
        x_start = (ANCHO_VENTANA - total_ancho) // 2
        y_start = TABLERO_Y + ALTO_TABLERO + 50
        
        for i, dado in enumerate(dados):
            dado_x = x_start + i * 60
            dado_y = y_start
            
            if (dado_x <= x <= dado_x + 50 and 
                dado_y <= y <= dado_y + 50):
                
                # Si es "bar", usar None; si es número, usar ese número
                from_point = None if self.punto_seleccionado == "bar" else self.punto_seleccionado
                
                # Intentar movimiento
                if self.game.move(from_point, dado):
                    origen = "BAR" if from_point is None else f"punto {from_point}"
                    self.mensaje = f"Movimiento exitoso: {origen} + dado {dado}"
                    self.punto_seleccionado = None
                else:
                    self.mensaje = "Movimiento inválido"
                return
    
    def ejecutar(self):
        """Loop principal del juego"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
                    elif event.key == pygame.K_SPACE:
                        if not self.game.available_dice():
                            dados = self.game.roll()
                            self.mensaje = f"Dados: {dados}"
                            self.dados_tirados = True
                        else:
                            self.mensaje = "Ya tiraste los dados"
                    
                    elif event.key == pygame.K_t:
                        if self.game.can_end_turn():
                            self.game.end_turn()
                            self.mensaje = "Turno terminado. Presiona ESPACIO para tirar dados"
                            self.dados_tirados = False
                            self.punto_seleccionado = None
                        else:
                            self.mensaje = "Aún tienes movimientos válidos"
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    
                    # Click en dado (ahora están centrados abajo)
                    if y > TABLERO_Y + ALTO_TABLERO + 30:
                        self.manejar_click_dado(x, y)
                    # Click en tablero o bar
                    else:
                        self.manejar_click_punto(x, y)
            
            # Dibujar
            self.dibujar_tablero()
            self.dibujar_fichas()
            self.dibujar_dados()
            self.dibujar_info()
            
            # Resaltar punto seleccionado o bar
            if self.punto_seleccionado == "bar":
                # Resaltar bar
                y_bar_centro = TABLERO_Y + ALTO_TABLERO // 2
                pygame.draw.rect(self.screen, VERDE, 
                               (BAR_X - ANCHO_PUNTO // 4, TABLERO_Y,
                                ANCHO_PUNTO // 2, ALTO_TABLERO), 4)
            elif self.punto_seleccionado is not None:
                coords = self.punto_a_coords(self.punto_seleccionado)
                if coords:
                    x, y = coords
                    # Centrar el círculo en la base del triángulo
                    if 12 <= self.punto_seleccionado <= 23:  # Parte superior (hacia abajo)
                        y_circulo = y + ALTO_PUNTO - 10
                    else:  # 0-11 - Parte inferior (hacia arriba)
                        y_circulo = y + 10
                    pygame.draw.circle(self.screen, VERDE, (int(x), int(y_circulo)), RADIO_FICHA + 5, 3)
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


def main():
    """Punto de entrada"""
    juego = BackgammonUI()
    juego.ejecutar()


if __name__ == "__main__":
    main()