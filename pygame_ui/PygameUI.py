"""
Backgammon con Pygame - Interfaz grafica
Layout estandar de backgammon
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
AMARILLO = (255, 215, 0)

# Constantes del tablero
ANCHO_VENTANA = 1200
ALTO_VENTANA = 1150
MARGEN = 120
ANCHO_TABLERO = ANCHO_VENTANA - 2 * MARGEN
ALTO_TABLERO = 600
ANCHO_PUNTO = ANCHO_TABLERO // 14
ALTO_PUNTO = ALTO_TABLERO // 2 - 20
RADIO_FICHA = 25

# Posiciones
TABLERO_X = MARGEN
TABLERO_Y = MARGEN
BAR_X = TABLERO_X + 6 * ANCHO_PUNTO + ANCHO_PUNTO // 2
OFF_X = TABLERO_X + ANCHO_TABLERO + 10  # DERECHA: despues del tablero
OFF_WIDTH = ANCHO_PUNTO - 20



class BackgammonUI:
    def __init__(self, nombre1="Blancas", nombre2="Negras"):
        pygame.init()
        self.game = BackgammonGame(nombre1, nombre2)
        self.screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Backgammon")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.info_message = None
        self.info_time = 0
        self.info_duration = 2000  # ms que permanece visible (2s)
        self.pending_end_turn = False  # si True, al expirar el mensaje, se pasa el turno
        self.punto_seleccionado = None
        self.dado_seleccionado = None

    def punto_a_coords(self, idx):
        """
        Mapea i­ndice (0-23) a coordenadas visuales.
        Layout personalizado (colores intercambiados):
        
        ARRIBA:   13-18 | BAR | 19-24
        ABAJO:    12-7  | BAR |  6-1
        """
        
        # ARRIBA IZQUIERDA: idx 12-17 â†’ puntos 13-18
        if 12 <= idx <= 17:
            col = idx - 12  # 0 a 5
            x = TABLERO_X + col * ANCHO_PUNTO + ANCHO_PUNTO // 2
            y = TABLERO_Y
            
        # ARRIBA DERECHA: idx 18-23 â†’ puntos 19-24
        elif 18 <= idx <= 23:
            col = idx - 18  # 0 a 5
            x = BAR_X + ANCHO_PUNTO + col * ANCHO_PUNTO + ANCHO_PUNTO // 2
            y = TABLERO_Y
            
        # ABAJO IZQUIERDA: idx 11-6 â†’ puntos 12-7
        elif 6 <= idx <= 11:
            col = 11 - idx  # 0 a 5
            x = TABLERO_X + col * ANCHO_PUNTO + ANCHO_PUNTO // 2
            y = TABLERO_Y + ALTO_TABLERO
            
        # ABAJO DERECHA: idx 5-0 â†’ puntos 6-1
        elif 0 <= idx <= 5:
            col = 5 - idx  # 0 a 5
            x = BAR_X + ANCHO_PUNTO + col * ANCHO_PUNTO + ANCHO_PUNTO // 2
            y = TABLERO_Y + ALTO_TABLERO
            
        else:
            return None
            
        return x, y

    def coords_a_punto(self, x, y):
        """Mapea coordenadas de click al i­ndice de un punto."""
        x_rel = x - TABLERO_X
        y_rel = y - TABLERO_Y

        if not (0 <= y_rel <= ALTO_TABLERO):
            return None

        # Determinar si estÃ¡ arriba o abajo
        if y_rel < ALTO_TABLERO // 2:  # ARRIBA
            if x_rel < 6 * ANCHO_PUNTO:  # IZQUIERDA (13-18)
                col = x_rel // ANCHO_PUNTO
                idx = 12 + col
            elif x_rel > 6 * ANCHO_PUNTO + ANCHO_PUNTO:  # DERECHA (19-24)
                col = (x_rel - ANCHO_PUNTO * 7) // ANCHO_PUNTO
                idx = 18 + col
            else:
                return None  # Barra
                
        else:  # ABAJO
            if x_rel < 6 * ANCHO_PUNTO:  # IZQUIERDA (12-7)
                col = x_rel // ANCHO_PUNTO
                idx = 11 - col
            elif x_rel > 6 * ANCHO_PUNTO + ANCHO_PUNTO:  # DERECHA (6-1)
                col = (x_rel - ANCHO_PUNTO * 7) // ANCHO_PUNTO
                idx = 5 - col
            else:
                return None  # Barra
                
        # Verificar que el click esta dentro del triangulo
        if (0 <= y_rel <= ALTO_PUNTO or ALTO_TABLERO - ALTO_PUNTO <= y_rel <= ALTO_TABLERO):
            return idx
        return None
    
    def es_area_bar(self, x, y):
        """Verifica si el click esta en el area de la barra."""
        return BAR_X - ANCHO_PUNTO // 2 <= x <= BAR_X + ANCHO_PUNTO // 2 and \
               TABLERO_Y <= y <= TABLERO_Y + ALTO_TABLERO

    def es_area_off(self, x, y):
        """Verifica si el click esta en el area de retirada (Off)."""
        return OFF_X <= x <= OFF_X + OFF_WIDTH and \
               TABLERO_Y <= y <= TABLERO_Y + ALTO_TABLERO

    def get_dado_at_pos(self, x, y):
        """Retorna el valor del dado en la posicion del click, o None."""
        dice = self.game.dice()
        disponibles = self.game.available_dice()
        
        if not dice:
            return None
            
        dado_size = 50
        espacio_entre_dados = 15
        total_width = len(dice) * dado_size + (len(dice) - 1) * espacio_entre_dados
        x_base = ANCHO_VENTANA // 2 - total_width // 2
        y_base = TABLERO_Y + ALTO_TABLERO + 50
        
        for i, die_val in enumerate(dice):
            dado_x = x_base + i * (dado_size + espacio_entre_dados)
            dado_y = y_base
            
            if dado_x <= x <= dado_x + dado_size and dado_y <= y <= dado_y + dado_size:
                if die_val in disponibles:
                    return die_val
                    
        return None

    def dibujar_tablero(self):
        """Dibuja el marco y los triangulos del tablero."""
        self.screen.fill(BEIGE)
        
        # Marco del tablero
        pygame.draw.rect(self.screen, MARRON_OSCURO, 
                         (TABLERO_X, TABLERO_Y, ANCHO_TABLERO, ALTO_TABLERO), 5)

        # Triangulos
        for i in range(24):
            coords = self.punto_a_coords(i)
            if coords is None:
                continue
            x, y = coords
            color_punto = MARRON_CLARO if i % 2 == 0 else MARRON_OSCURO
            
            # TODOS los triangulos de ARRIBA (12-23) apuntan HACIA ABAJO
            if 12 <= i <= 23:
                puntos = [(x - ANCHO_PUNTO // 2, y),      # Base izquierda
                          (x + ANCHO_PUNTO // 2, y),      # Base derecha
                          (x, y + ALTO_PUNTO)]            # Punta hacia abajo
            # TODOS los triangulos de ABAJO (0-11) apuntan HACIA ARRIBA
            else:
                puntos = [(x - ANCHO_PUNTO // 2, y),      # Base izquierda
                          (x + ANCHO_PUNTO // 2, y),      # Base derecha
                          (x, y - ALTO_PUNTO)]            # Punta hacia arriba
            
            pygame.draw.polygon(self.screen, color_punto, puntos)

        # Barra Central
        pygame.draw.line(self.screen, MARRON_OSCURO, 
                         (BAR_X, TABLERO_Y), (BAR_X, TABLERO_Y + ALTO_TABLERO), ANCHO_PUNTO)
        
        # area de Retirada
        pygame.draw.rect(self.screen, GRIS, 
                         (OFF_X, TABLERO_Y, OFF_WIDTH, ALTO_TABLERO), 0)
        pygame.draw.rect(self.screen, MARRON_OSCURO, 
                         (OFF_X, TABLERO_Y, OFF_WIDTH, ALTO_TABLERO), 3)

    def dibujar_fichas(self):
        """Dibuja las fichas en el tablero, la barra y el area de retirada."""
        # Dibujar fichas en los puntos (apoyadas en la base, con +n si hay más de 5)
        MAX_VISIBLE_STACK = 5   # cuántas se muestran por punto
        PADDING_BASE = 6        # espacio entre base y la primera ficha
        GAP_STACK = 2           # (opcional) espacio entre fichas visibles

        for i in range(24):
            coords = self.punto_a_coords(i)
            if coords is None:
                continue

            x, y = coords
            stack = self.game.board().points()[i]
            count = len(stack)
            if count == 0:
                continue

            # Color (todas las fichas de un punto son del mismo color si count>1)
            color = BLANCO if stack[0].color() == 'B' else NEGRO

            visible = min(count, MAX_VISIBLE_STACK)

            if 12 <= i <= 23:
                # TRIANGULOS DE ARRIBA (apuntan hacia abajo) -> base en y (arriba)
                # Apilar desde la base hacia adentro del triángulo
                start_y = y + PADDING_BASE + RADIO_FICHA
                for k in range(visible):
                    y_centro = start_y + k * (2 * RADIO_FICHA + GAP_STACK)
                    pygame.draw.circle(self.screen, color, (int(x), int(y_centro)), RADIO_FICHA)
                    pygame.draw.circle(self.screen, MARRON_OSCURO, (int(x), int(y_centro)), RADIO_FICHA, 2)

                # Indicador +n si hay más de las visibles
                if count > visible:
                    font_small = pygame.font.Font(None, 24)
                    extra = count - visible
                    text = font_small.render(f"+{extra}", True, color)
                    # Lo colocamos debajo de la última visible, pegadito
                    tx = int(x - text.get_width() // 2)
                    ty = int(start_y + visible * (2 * RADIO_FICHA + GAP_STACK))
                    # Evitar salirnos del triángulo
                    ty = min(ty, y + ALTO_PUNTO - text.get_height() - 2)
                    self.screen.blit(text, (tx, ty))

            else:
                # TRIÁNGULOS DE ABAJO (apuntan hacia arriba) -> base en y (abajo)
                # Apilar desde la base hacia adentro del triángulo
                start_y = y - PADDING_BASE - RADIO_FICHA
                for k in range(visible):
                    y_centro = start_y - k * (2 * RADIO_FICHA + GAP_STACK)
                    pygame.draw.circle(self.screen, color, (int(x), int(y_centro)), RADIO_FICHA)
                    pygame.draw.circle(self.screen, MARRON_OSCURO, (int(x), int(y_centro)), RADIO_FICHA, 2)

                # Indicador +n si hay más de las visibles
                if count > visible:
                    font_small = pygame.font.Font(None, 24)
                    extra = count - visible
                    text = font_small.render(f"+{extra}", True, color)
                    # Lo colocamos arriba de la última visible, pegadito
                    tx = int(x - text.get_width() // 2)
                    ty = int(start_y - visible * (2 * RADIO_FICHA + GAP_STACK) - text.get_height())
                    # Evitar salirnos del triángulo
                    ty = max(ty, y - ALTO_PUNTO + 2)
                    self.screen.blit(text, (tx, ty))

        # Dibujar fichas en la Barra
        bar = self.game.board().bar()
        if bar['B']:
            for j, _ in enumerate(bar['B']):
                y_centro = TABLERO_Y + 30 + j * 2 * RADIO_FICHA
                x_centro = BAR_X - 20
                pygame.draw.circle(self.screen, BLANCO, (int(x_centro), int(y_centro)), RADIO_FICHA)
                pygame.draw.circle(self.screen, MARRON_OSCURO, (int(x_centro), int(y_centro)), RADIO_FICHA, 2)
        
        if bar['N']:
            for j, _ in enumerate(bar['N']):
                y_centro = TABLERO_Y + ALTO_TABLERO - 30 - j * 2 * RADIO_FICHA
                x_centro = BAR_X - 20
                pygame.draw.circle(self.screen, NEGRO, (int(x_centro), int(y_centro)), RADIO_FICHA)
                pygame.draw.circle(self.screen, MARRON_OSCURO, (int(x_centro), int(y_centro)), RADIO_FICHA, 2)

                # Dibujar fichas retiradas como "tiritas" horizontales apiladas
        off = self.game.board().off()

        SEG_ANCHO = OFF_WIDTH - 10     # ancho de la tirita
        SEG_ALTO  = 6                  # alto de la tirita
        SEG_GAP   = 4                  # espacio entre tiritas
        x_seg = OFF_X + (OFF_WIDTH - SEG_ANCHO) // 2

        # BLANCAS: de arriba hacia abajo
        if off['B'] > 0:
            max_draw = min(off['B'], 15)
            for j in range(max_draw):
                y_seg = TABLERO_Y + 10 + j * (SEG_ALTO + SEG_GAP)
                pygame.draw.rect(self.screen, BLANCO, (x_seg, y_seg, SEG_ANCHO, SEG_ALTO))
                pygame.draw.rect(self.screen, MARRON_OSCURO, (x_seg, y_seg, SEG_ANCHO, SEG_ALTO), 1)
            # Mostrar +n si hay más de 15
            if off['B'] > 15:
                font_num = pygame.font.Font(None, 24)
                extra = off['B'] - 15
                text_num = font_num.render(f"+{extra}", True, BLANCO)
                self.screen.blit(text_num, (x_seg, TABLERO_Y + 10 + max_draw * (SEG_ALTO + SEG_GAP) + 4))

        # NEGRAS: de abajo hacia arriba
        if off['N'] > 0:
            max_draw = min(off['N'], 15)
            for j in range(max_draw):
                # j=0 dibuja pegado abajo; luego sube
                y_seg = TABLERO_Y + ALTO_TABLERO - 10 - (j + 1) * (SEG_ALTO + SEG_GAP)
                pygame.draw.rect(self.screen, NEGRO, (x_seg, y_seg, SEG_ANCHO, SEG_ALTO))
                pygame.draw.rect(self.screen, MARRON_OSCURO, (x_seg, y_seg, SEG_ANCHO, SEG_ALTO), 1)
            if off['N'] > 15:
                font_num = pygame.font.Font(None, 24)
                extra = off['N'] - 15
                text_num = font_num.render(f"+{extra}", True, NEGRO)
                self.screen.blit(text_num, (x_seg, TABLERO_Y + ALTO_TABLERO - 10 - max_draw * (SEG_ALTO + SEG_GAP) - 24))


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
                
                # Color del dado segun estado
                if die_val in disponibles:
                    die_color = VERDE
                else:
                    die_color = GRIS
                
                pygame.draw.rect(self.screen, die_color, (x, y, dado_size, dado_size), 0, 5)
                pygame.draw.rect(self.screen, NEGRO, (x, y, dado_size, dado_size), 2, 5)
                
                text_dado = self.font.render(str(die_val), True, NEGRO)
                text_rect = text_dado.get_rect(center=(x + dado_size // 2, y + dado_size // 2))
                self.screen.blit(text_dado, text_rect)
                
    def dibujar_info(self):
        """Muestra informacion del turno y el juego."""
        color_turno = "BLANCAS" if self.game.turno() == 'B' else "NEGRAS"
        color_rgb = BLANCO if self.game.turno() == 'B' else NEGRO
        
        jugador_actual = self.game.current_player()
        nombre_jugador = jugador_actual.nombre()

        # Instrucciones dinÃ¡micas arriba
        if not self.game.dice():
            text_instruccion = self.font.render("Presiona ESPACIO para tirar dados", True, AZUL)
        elif self.game.board().has_checkers_on_bar(self.game.turno()):
            # MENSAJE ESPECIAL: Hay fichas en el bar
            if self.puede_sacar_del_bar():
                text_instruccion = self.font.render("¡DEBES SACAR TUS FICHAS DEL BAR PRIMERO!", True, ROJO)
            else:
                text_instruccion = self.font.render("BLOQUEADO - Presiona ESPACIO para pasar turno", True, ROJO)
        elif self.punto_seleccionado is None:
            text_instruccion = self.font.render("1. Selecciona una de tus fichas (clic para cambiar)", True, VERDE)
        elif self.dado_seleccionado is None:
            text_instruccion = self.font.render("2. Haz CLICK en un DADO (se movera automaticamente)", True, AMARILLO)
        else:
            text_instruccion = self.font.render("Presiona ESPACIO para terminar turno", True, AZUL)
            
        rect_instruccion = text_instruccion.get_rect(center=(ANCHO_VENTANA // 2, TABLERO_Y - 20))
        self.screen.blit(text_instruccion, rect_instruccion)
        
        # Info de retiradas y turno
        off_B = self.game.board().off()['B']
        off_N = self.game.board().off()['N']
        text_off = self.font.render(f"Retiradas - B: {off_B} | N: {off_N}", True, MARRON_OSCURO)
        self.screen.blit(text_off, (ANCHO_VENTANA - text_off.get_width() - 20, TABLERO_Y + ALTO_TABLERO + 120))

        text_turno = self.font.render(f"Turno: {color_turno} ({nombre_jugador})", True, color_rgb)
        self.screen.blit(text_turno, (20, TABLERO_Y + ALTO_TABLERO + 120))

        # Instrucciones
        font_pequena = pygame.font.Font(None, 28)
        instrucciones = [
            "COMO JUGAR:",
            "1. Presiona ESPACIO para tirar los dados",
            "2. Haz CLICK en una de tus fichas (o en el BAR si tienes ahi­)",
            "3. Haz CLICK en el DADO que quieres usar (la ficha se mueve automaticamente)",
        ]
        
        y_inicial = TABLERO_Y + ALTO_TABLERO + 160
        for i, linea in enumerate(instrucciones):
            if i == 0:
                color_texto = MARRON_OSCURO
                font_usada = self.font
            else:
                color_texto = NEGRO
                font_usada = font_pequena
            text_inst = font_usada.render(linea, True, color_texto)
            self.screen.blit(text_inst, (20, y_inicial + i * 32))

        # Mensaje de victoria
        if self.game.is_game_over():
            ganador = "BLANCAS" if self.game.winner() == 'B' else "NEGRAS"
            text_ganador = self.font.render(f"¡JUEGO TERMINADO! GANADOR: {ganador}", True, ROJO)
            self.screen.blit(text_ganador, (ANCHO_VENTANA // 2 - text_ganador.get_width() // 2, 10))

    def puede_sacar_del_bar(self):
        """Verifica si el jugador puede sacar alguna ficha del bar con los dados disponibles."""
        if not self.game.board().has_checkers_on_bar(self.game.turno()):
            return True  # No hay fichas en el bar, no aplica
        
        dados_disponibles = self.game.available_dice()
        if not dados_disponibles:
            return False
        
        # Verificar si algún dado permite sacar del bar
        for dado in dados_disponibles:
            if self.game.can_move(None, dado):  # None = desde el bar
                return True
        
        return False

    def manejar_espacio(self):
        """Maneja la tecla ESPACIO para tirar dados o terminar turno."""
        try:
            if self.game.is_game_over():
                return

            if not self.game.dice():
                self.game.roll()
                self.punto_seleccionado = None
                self.dado_seleccionado = None
            else:
                dados_disponibles = self.game.available_dice()

                # Caso especial: hay fichas en el bar
                if self.game.board().has_checkers_on_bar(self.game.turno()):
                    if not self.puede_sacar_del_bar():
                        # Antes pasabas el turno directo: ahora mostramos aviso y lo pasamos tras 2s
                        self.info_message = "Sin movimientos válidos desde la barra. Se pasa el turno…"
                        self.info_time = pygame.time.get_ticks()
                        self.pending_end_turn = True
                        # limpiar selecciones
                        self.punto_seleccionado = None
                        self.dado_seleccionado = None
                        return

                # Caso normal: sin dados disponibles o sin movimientos válidos
                if not dados_disponibles or not self.game.has_valid_moves():
                    if self.game.can_end_turn():
                        # Antes: self.game.end_turn()
                        self.info_message = "Sin movimientos válidos. Se pasa el turno…"
                        self.info_time = pygame.time.get_ticks()
                        self.pending_end_turn = True
                        self.punto_seleccionado = None
                        self.dado_seleccionado = None

        except Exception as e:
            print(f"Error en manejar_espacio: {e}")
            import traceback
            traceback.print_exc()
            self.punto_seleccionado = None
            self.dado_seleccionado = None
            raise

    def manejar_click(self, x, y):
        """Maneja todos los clicks del mouse."""
        try:
            if self.game.is_game_over():
                return
                
            if not self.game.dice():
                return
            
            # Si NO hay ficha seleccionada, intentar seleccionar ficha
            if self.punto_seleccionado is None:
                punto_idx = self.coords_a_punto(x, y)
                
                if punto_idx is None:
                    if self.es_area_bar(x, y):
                        if self.game.board().has_checkers_on_bar(self.game.turno()):
                            self.punto_seleccionado = "bar"
                            self.dado_seleccionado = None
                    return
                
                # REGLA: Si hay fichas en el bar, SOLO se puede seleccionar del bar
                if self.game.board().has_checkers_on_bar(self.game.turno()):
                    # No permitir seleccionar fichas del tablero
                    return
                
                if punto_idx in range(24):
                    owner, count = self.game.board().point_owner_count(punto_idx)
                    if owner == self.game.turno() and count > 0:
                        self.punto_seleccionado = punto_idx
                        self.dado_seleccionado = None
                return
            
            # Si hay ficha seleccionada pero NO hay dado seleccionado
            if self.dado_seleccionado is None:
                # Primero verificar si se hizo click en un dado
                dado_clickeado = self.get_dado_at_pos(x, y)
                if dado_clickeado is not None:
                    # Convertir "bar" a None para la llamada a can_move
                    origen = None if self.punto_seleccionado == "bar" else self.punto_seleccionado
                    if self.game.can_move(origen, dado_clickeado):
                        self.dado_seleccionado = dado_clickeado
                        # Ejecutar el movimiento INMEDIATAMENTE después de seleccionar el dado
                        if self.game.move(origen, self.dado_seleccionado):
                            pass
                        # Resetear las selecciones
                        self.punto_seleccionado = None
                        self.dado_seleccionado = None
                    return
                
                # Si no se hizo click en un dado, verificar si se quiere cambiar de ficha
                punto_idx = self.coords_a_punto(x, y)
                
                # Click en el bar para cambiar la selección
                if punto_idx is None:
                    if self.es_area_bar(x, y):
                        if self.game.board().has_checkers_on_bar(self.game.turno()):
                            self.punto_seleccionado = "bar"
                            self.dado_seleccionado = None
                        return
                    # Click en área vacía: deseleccionar
                    self.punto_seleccionado = None
                    self.dado_seleccionado = None
                    return
                
                # Click en otro punto: cambiar selección si es del jugador actual
                # REGLA: Si hay fichas en el bar, NO se puede cambiar a fichas del tablero
                if punto_idx in range(24):
                    if self.game.board().has_checkers_on_bar(self.game.turno()):
                        # No permitir cambiar a fichas del tablero si hay fichas en el bar
                        return
                    
                    owner, count = self.game.board().point_owner_count(punto_idx)
                    if owner == self.game.turno() and count > 0:
                        self.punto_seleccionado = punto_idx
                        self.dado_seleccionado = None
                    else:
                        # Click en punto vacío o del oponente: deseleccionar
                        self.punto_seleccionado = None
                        self.dado_seleccionado = None
                return
                
        except Exception as e:
            print(f"Error en manejar_click: {e}")
            import traceback
            traceback.print_exc()
            # Resetear estado en caso de error
            self.punto_seleccionado = None
            self.dado_seleccionado = None
            raise  # Re-lanzar para que lo capture el bucle principal

    def run(self):
        """Bucle principal de Pygame."""
        running = True
        error_message = None
        error_time = 0
        
        while running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.manejar_espacio()
                        elif event.key == pygame.K_ESCAPE and error_message:
                            # Presionar ESC para cerrar mensaje de error
                            error_message = None
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        self.manejar_click(x, y)

                self.dibujar_tablero()
                self.dibujar_fichas()
                self.dibujar_dados()
                self.dibujar_info()
                
                # Resaltar área del bar si hay fichas bloqueadas
                if self.game.dice() and self.game.board().has_checkers_on_bar(self.game.turno()):
                    if not self.puede_sacar_del_bar():
                        # Resaltar en ROJO para indicar bloqueo
                        pygame.draw.rect(self.screen, ROJO, 
                                       (BAR_X - ANCHO_PUNTO // 4, TABLERO_Y,
                                        ANCHO_PUNTO // 2, ALTO_TABLERO), 5)
                
                # Resaltar la seleccion
                if self.punto_seleccionado == "bar":
                    pygame.draw.rect(self.screen, VERDE, 
                                   (BAR_X - ANCHO_PUNTO // 4, TABLERO_Y,
                                    ANCHO_PUNTO // 2, ALTO_TABLERO), 4)
                                    
                elif self.punto_seleccionado is not None and self.punto_seleccionado != 24:
                    coords = self.punto_a_coords(self.punto_seleccionado)
                    if coords:
                        x, y = coords
                        
                        # ARRIBA (12-23): fichas estan en punta hacia abajo
                        if 12 <= self.punto_seleccionado <= 23:
                            y_center = y + ALTO_PUNTO - RADIO_FICHA
                        # ABAJO (0-11): fichas estan en punta hacia arriba
                        else:
                            y_center = y - ALTO_PUNTO + RADIO_FICHA
                            
                        pygame.draw.circle(self.screen, VERDE, (int(x), int(y_center)), RADIO_FICHA + 3, 3)
                
                # Mostrar mensaje de error si existe
                if error_message:
                    current_time = pygame.time.get_ticks()
                    if current_time - error_time < 10000:  # Mostrar por 10 segundos
                        error_surf = pygame.Surface((ANCHO_VENTANA - 40, 150))
                        error_surf.fill(ROJO)
                        pygame.draw.rect(error_surf, NEGRO, (0, 0, error_surf.get_width(), error_surf.get_height()), 3)
                        
                        font_error = pygame.font.Font(None, 24)
                        lines = error_message.split('\n')
                        y_offset = 10
                        for line in lines:
                            text = font_error.render(line, True, BLANCO)
                            error_surf.blit(text, (10, y_offset))
                            y_offset += 30
                        
                        self.screen.blit(error_surf, (20, ALTO_VENTANA // 2 - 75))
                    else:
                        error_message = None
                # Cartel informativo (amarillo) y auto "end turn" si corresponde
                if self.info_message:
                    current_time = pygame.time.get_ticks()
                    # Render del cartel
                    info_surf = pygame.Surface((ANCHO_VENTANA - 40, 120))
                    info_surf.fill(AMARILLO)
                    pygame.draw.rect(info_surf, NEGRO, (0, 0, info_surf.get_width(), info_surf.get_height()), 3)
                    font_info_title = pygame.font.Font(None, 32)
                    font_info_text  = pygame.font.Font(None, 26)

                    t1 = font_info_title.render("Aviso", True, NEGRO)
                    t2 = font_info_text.render(self.info_message, True, NEGRO)
                    info_surf.blit(t1, (12, 10))
                    info_surf.blit(t2, (12, 55))
                    self.screen.blit(info_surf, (20, ALTO_VENTANA // 2 - 60))

                    # Al expirar el tiempo, ejecutamos acción pendiente (si la hay)
                    if current_time - self.info_time >= self.info_duration:
                        self.info_message = None
                        if self.pending_end_turn and self.game.can_end_turn():
                            self.game.end_turn()
                        self.pending_end_turn = False

                pygame.display.flip()
                self.clock.tick(60)
                
            except Exception as e:
                # Capturar cualquier error y mostrarlo
                import traceback
                error_message = f"ERROR: {str(e)}\nPresiona ESC para continuar"
                error_time = pygame.time.get_ticks()
                print("\n=== ERROR CAPTURADO ===")
                print(traceback.format_exc())
                print("=======================\n")
                # Resetear selecciones para intentar recuperarse
                self.punto_seleccionado = None
                self.dado_seleccionado = None
        
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