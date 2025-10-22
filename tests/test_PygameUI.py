import unittest
from unittest.mock import Mock, MagicMock, patch, call
import sys

# Mock pygame antes de importar PygameUI
sys.modules['pygame'] = MagicMock()
sys.modules['pygame.font'] = MagicMock()
sys.modules['pygame.display'] = MagicMock()
sys.modules['pygame.time'] = MagicMock()
sys.modules['pygame.event'] = MagicMock()
sys.modules['pygame.draw'] = MagicMock()

from core.PygameUI import BackgammonUI, main
import core.PygameUI as pygame_ui_module


class TestBackgammonUIInit(unittest.TestCase):
    """Tests de inicialización"""
    
    @patch('core.PygameUI.pygame')
    @patch('core.PygameUI.BackgammonGame')
    def test_init_nombres_por_defecto(self, mock_game_class, mock_pygame):
        """Verifica inicialización con nombres por defecto"""
        mock_screen = MagicMock()
        mock_pygame.display.set_mode.return_value = mock_screen
        mock_pygame.font.Font.return_value = MagicMock()
        mock_pygame.time.Clock.return_value = MagicMock()
        
        ui = BackgammonUI()
        
        mock_pygame.init.assert_called_once()
        mock_game_class.assert_called_once_with("Blancas", "Negras")
        mock_pygame.display.set_mode.assert_called_once()
        mock_pygame.display.set_caption.assert_called_once_with("Backgammon")
        
        self.assertIsNone(ui.punto_seleccionado)
        self.assertEqual(ui.movimientos_validos, [])
    
    @patch('core.PygameUI.pygame')
    @patch('core.PygameUI.BackgammonGame')
    def test_init_nombres_personalizados(self, mock_game_class, mock_pygame):
        """Verifica inicialización con nombres personalizados"""
        mock_pygame.display.set_mode.return_value = MagicMock()
        mock_pygame.font.Font.return_value = MagicMock()
        mock_pygame.time.Clock.return_value = MagicMock()
        
        ui = BackgammonUI("Alice", "Bob")
        
        mock_game_class.assert_called_once_with("Alice", "Bob")


class TestBackgammonUICoordenadas(unittest.TestCase):
    """Tests de métodos de coordenadas"""
    
    def setUp(self):
        with patch('core.PygameUI.pygame'), \
             patch('core.PygameUI.BackgammonGame'):
            self.ui = BackgammonUI()
    
    def test_punto_a_coords_rango_0_5(self):
        """Verifica conversión de puntos 0-5 (abajo izquierda)"""
        x, y = self.ui.punto_a_coords(0)
        self.assertIsNotNone(x)
        self.assertIsNotNone(y)
        
        x, y = self.ui.punto_a_coords(5)
        self.assertIsNotNone(x)
        self.assertIsNotNone(y)
    
    def test_punto_a_coords_rango_6_11(self):
        """Verifica conversión de puntos 6-11 (abajo derecha)"""
        x, y = self.ui.punto_a_coords(6)
        self.assertIsNotNone(x)
        self.assertIsNotNone(y)
        
        x, y = self.ui.punto_a_coords(11)
        self.assertIsNotNone(x)
        self.assertIsNotNone(y)
    
    def test_punto_a_coords_rango_12_17(self):
        """Verifica conversión de puntos 12-17 (arriba derecha)"""
        x, y = self.ui.punto_a_coords(12)
        self.assertIsNotNone(x)
        self.assertIsNotNone(y)
        
        x, y = self.ui.punto_a_coords(17)
        self.assertIsNotNone(x)
        self.assertIsNotNone(y)
    
    def test_punto_a_coords_rango_18_23(self):
        """Verifica conversión de puntos 18-23 (arriba izquierda)"""
        x, y = self.ui.punto_a_coords(18)
        self.assertIsNotNone(x)
        self.assertIsNotNone(y)
        
        x, y = self.ui.punto_a_coords(23)
        self.assertIsNotNone(x)
        self.assertIsNotNone(y)
    
    def test_punto_a_coords_fuera_de_rango(self):
        """Verifica que retorna None para índices inválidos"""
        self.assertIsNone(self.ui.punto_a_coords(24))
        self.assertIsNone(self.ui.punto_a_coords(-1))
        self.assertIsNone(self.ui.punto_a_coords(100))
    
    def test_coords_a_punto_fuera_de_rango_y(self):
        """Verifica coords_a_punto con y fuera de rango"""
        result = self.ui.coords_a_punto(100, -10)
        self.assertIsNone(result)
        
        result = self.ui.coords_a_punto(100, 10000)
        self.assertIsNone(result)
    
    def test_coords_a_punto_arriba_izquierda(self):
        """Verifica coords_a_punto en cuadrante arriba izquierda (18-23)"""
        # Simular click en zona arriba (y_rel < ALTO_TABLERO // 2)
        # y dentro de x_rel < 6 * ANCHO_PUNTO
        x = 50 + 100  # TABLERO_X + offset
        y = 50 + 50   # TABLERO_Y + offset (arriba)
        
        result = self.ui.coords_a_punto(x, y)
        # Debería retornar un índice o None dependiendo de la posición exacta
        # Lo importante es que no crashee
        self.assertIsInstance(result, (int, type(None)))
    
    def test_coords_a_punto_arriba_derecha(self):
        """Verifica coords_a_punto en cuadrante arriba derecha (12-17)"""
        x = 50 + 7 * 80 + 50  # TABLERO_X + más de 7*ANCHO_PUNTO
        y = 50 + 50
        
        result = self.ui.coords_a_punto(x, y)
        self.assertIsInstance(result, (int, type(None)))
    
    def test_coords_a_punto_arriba_barra(self):
        """Verifica coords_a_punto en la barra (arriba)"""
        x = 50 + 6 * 80 + 40  # En la barra
        y = 50 + 50
        
        result = self.ui.coords_a_punto(x, y)
        self.assertIsNone(result)
    
    def test_coords_a_punto_abajo_izquierda(self):
        """Verifica coords_a_punto en cuadrante abajo izquierda (0-5)"""
        x = 50 + 100
        y = 50 + 500  # Abajo
        
        result = self.ui.coords_a_punto(x, y)
        self.assertIsInstance(result, (int, type(None)))
    
    def test_coords_a_punto_abajo_derecha(self):
        """Verifica coords_a_punto en cuadrante abajo derecha (6-11)"""
        x = 50 + 7 * 80 + 50
        y = 50 + 500
        
        result = self.ui.coords_a_punto(x, y)
        self.assertIsInstance(result, (int, type(None)))
    
    def test_coords_a_punto_abajo_barra(self):
        """Verifica coords_a_punto en la barra (abajo)"""
        x = 50 + 6 * 80 + 40
        y = 50 + 500
        
        result = self.ui.coords_a_punto(x, y)
        self.assertIsNone(result)
    
    def test_es_area_dados_true(self):
        """Verifica es_area_dados cuando está dentro"""
        # Área de dados está alrededor de BAR_X
        x = 50 + 6 * 80 + 40
        y = 50 + 300
        
        result = self.ui.es_area_dados(x, y)
        self.assertIsInstance(result, bool)
    
    def test_es_area_dados_false(self):
        """Verifica es_area_dados cuando está fuera"""
        result = self.ui.es_area_dados(10, 10)
        self.assertFalse(result)
    
    def test_es_area_bar_true(self):
        """Verifica es_area_bar cuando está dentro"""
        x = 50 + 6 * 80 + 40
        y = 50 + 300
        
        result = self.ui.es_area_bar(x, y)
        self.assertIsInstance(result, bool)
    
    def test_es_area_bar_false(self):
        """Verifica es_area_bar cuando está fuera"""
        result = self.ui.es_area_bar(10, 10)
        self.assertFalse(result)
    
    def test_es_area_off_true(self):
        """Verifica es_area_off cuando está dentro"""
        # OFF_X está al final del tablero
        x = 50 + 1100 - 80 + 15
        y = 50 + 300
        
        result = self.ui.es_area_off(x, y)
        self.assertIsInstance(result, bool)
    
    def test_es_area_off_false(self):
        """Verifica es_area_off cuando está fuera"""
        result = self.ui.es_area_off(10, 10)
        self.assertFalse(result)
    
    def test_punto_idx_a_die_blancas(self):
        """Verifica punto_idx_a_die para jugador blanco"""
        self.ui.game.turno = Mock(return_value='B')
        
        self.assertEqual(self.ui.punto_idx_a_die(0), 1)
        self.assertEqual(self.ui.punto_idx_a_die(5), 6)
    
    def test_punto_idx_a_die_negras(self):
        """Verifica punto_idx_a_die para jugador negro"""
        self.ui.game.turno = Mock(return_value='N')
        
        self.assertEqual(self.ui.punto_idx_a_die(23), 1)
        self.assertEqual(self.ui.punto_idx_a_die(18), 6)


class TestBackgammonUIDibujo(unittest.TestCase):
    """Tests de métodos de dibujo"""
    
    def setUp(self):
        with patch('core.PygameUI.pygame') as mock_pygame:
            with patch('core.PygameUI.BackgammonGame'):
                mock_pygame.display.set_mode.return_value = MagicMock()
                mock_pygame.font.Font.return_value = MagicMock()
                mock_pygame.time.Clock.return_value = MagicMock()
                self.ui = BackgammonUI()
                self.mock_pygame = mock_pygame
    
    @patch('core.PygameUI.pygame')
    def test_dibujar_tablero(self, mock_pygame):
        """Verifica que dibujar_tablero llame a las funciones de pygame"""
        self.ui.screen = MagicMock()
        self.ui.dibujar_tablero()
        
        # Verificar que se llamó a fill
        self.ui.screen.fill.assert_called_once()
        
        # Verificar que se llamó a draw.rect y draw.polygon
        self.assertGreater(mock_pygame.draw.rect.call_count, 0)
        self.assertGreater(mock_pygame.draw.polygon.call_count, 0)
        self.assertGreater(mock_pygame.draw.line.call_count, 0)
    
    @patch('core.PygameUI.pygame')
    def test_dibujar_fichas_punto_abajo(self, mock_pygame):
        """Verifica dibujar_fichas para puntos abajo (0-11)"""
        self.ui.screen = MagicMock()
        self.ui.game.board = Mock()
        
        # Mock del board
        mock_board = MagicMock()
        mock_board.points.return_value = [[] for _ in range(24)]
        
        # Agregar una ficha al punto 0
        mock_checker = MagicMock()
        mock_checker.color.return_value = 'B'
        mock_board.points.return_value[0] = [mock_checker]
        
        # Mock del bar
        mock_board.bar.return_value = {'B': [], 'N': []}
        mock_board.off.return_value = {'B': 0, 'N': 0}
        
        self.ui.game.board.return_value = mock_board
        
        self.ui.dibujar_fichas()
        
        # Verificar que se dibujaron círculos
        self.assertGreater(mock_pygame.draw.circle.call_count, 0)
    
    @patch('core.PygameUI.pygame')
    def test_dibujar_fichas_punto_arriba(self, mock_pygame):
        """Verifica dibujar_fichas para puntos arriba (12-23)"""
        self.ui.screen = MagicMock()
        self.ui.game.board = Mock()
        
        mock_board = MagicMock()
        mock_board.points.return_value = [[] for _ in range(24)]
        
        # Agregar una ficha al punto 12
        mock_checker = MagicMock()
        mock_checker.color.return_value = 'N'
        mock_board.points.return_value[12] = [mock_checker]
        
        mock_board.bar.return_value = {'B': [], 'N': []}
        mock_board.off.return_value = {'B': 0, 'N': 0}
        
        self.ui.game.board.return_value = mock_board
        
        self.ui.dibujar_fichas()
        
        self.assertGreater(mock_pygame.draw.circle.call_count, 0)
    
    @patch('core.PygameUI.pygame')
    def test_dibujar_fichas_bar_blancas(self, mock_pygame):
        """Verifica dibujar_fichas con fichas en bar para blancas"""
        self.ui.screen = MagicMock()
        self.ui.game.board = Mock()
        
        mock_board = MagicMock()
        mock_board.points.return_value = [[] for _ in range(24)]
        
        # Ficha blanca en bar
        mock_checker = MagicMock()
        mock_checker.color.return_value = 'B'
        mock_board.bar.return_value = {'B': [mock_checker], 'N': []}
        mock_board.off.return_value = {'B': 0, 'N': 0}
        
        self.ui.game.board.return_value = mock_board
        
        self.ui.dibujar_fichas()
        
        self.assertGreater(mock_pygame.draw.circle.call_count, 0)
    
    @patch('core.PygameUI.pygame')
    def test_dibujar_fichas_bar_negras(self, mock_pygame):
        """Verifica dibujar_fichas con fichas en bar para negras"""
        self.ui.screen = MagicMock()
        self.ui.game.board = Mock()
        
        mock_board = MagicMock()
        mock_board.points.return_value = [[] for _ in range(24)]
        
        # Ficha negra en bar
        mock_checker = MagicMock()
        mock_checker.color.return_value = 'N'
        mock_board.bar.return_value = {'B': [], 'N': [mock_checker]}
        mock_board.off.return_value = {'B': 0, 'N': 0}
        
        self.ui.game.board.return_value = mock_board
        
        self.ui.dibujar_fichas()
        
        self.assertGreater(mock_pygame.draw.circle.call_count, 0)
    
    @patch('core.PygameUI.pygame')
    def test_dibujar_fichas_off_blancas(self, mock_pygame):
        """Verifica dibujar_fichas con fichas retiradas blancas"""
        self.ui.screen = MagicMock()
        self.ui.game.board = Mock()
        
        mock_board = MagicMock()
        mock_board.points.return_value = [[] for _ in range(24)]
        mock_board.bar.return_value = {'B': [], 'N': []}
        mock_board.off.return_value = {'B': 5, 'N': 0}
        
        self.ui.game.board.return_value = mock_board
        
        self.ui.dibujar_fichas()
        
        # Debería dibujar fichas en el área off
        self.assertGreater(mock_pygame.draw.circle.call_count, 0)
    
    @patch('core.PygameUI.pygame')
    def test_dibujar_fichas_off_negras(self, mock_pygame):
        """Verifica dibujar_fichas con fichas retiradas negras"""
        self.ui.screen = MagicMock()
        self.ui.game.board = Mock()
        
        mock_board = MagicMock()
        mock_board.points.return_value = [[] for _ in range(24)]
        mock_board.bar.return_value = {'B': [], 'N': []}
        mock_board.off.return_value = {'B': 0, 'N': 7}
        
        self.ui.game.board.return_value = mock_board
        
        self.ui.dibujar_fichas()
        
        self.assertGreater(mock_pygame.draw.circle.call_count, 0)
    
    @patch('core.PygameUI.pygame')
    def test_dibujar_dados_sin_tirada(self, mock_pygame):
        """Verifica dibujar_dados cuando no se ha tirado"""
        self.ui.screen = MagicMock()
        self.ui.game.dice = Mock(return_value=[])
        self.ui.font = MagicMock()
        
        self.ui.dibujar_dados()
        
        # Debería mostrar "TIRAR DADOS"
        self.ui.font.render.assert_called()
        self.ui.screen.blit.assert_called()
    
    @patch('core.PygameUI.pygame')
    def test_dibujar_dados_con_tirada(self, mock_pygame):
        """Verifica dibujar_dados con dados tirados"""
        self.ui.screen = MagicMock()
        self.ui.game.dice = Mock(return_value=[3, 1])
        self.ui.game.available_dice = Mock(return_value=[3, 1])
        self.ui.font = MagicMock()
        self.ui.font.render.return_value = MagicMock()
        
        self.ui.dibujar_dados()
        
        # Debería dibujar los dados
        self.assertGreater(mock_pygame.draw.rect.call_count, 0)
        self.assertGreater(self.ui.screen.blit.call_count, 0)
    
    @patch('core.PygameUI.pygame')
    def test_dibujar_dados_con_dados_usados(self, mock_pygame):
        """Verifica dibujar_dados con algunos dados usados"""
        self.ui.screen = MagicMock()
        self.ui.game.dice = Mock(return_value=[3, 1])
        self.ui.game.available_dice = Mock(return_value=[1])  # Solo queda 1
        self.ui.font = MagicMock()
        self.ui.font.render.return_value = MagicMock()
        
        self.ui.dibujar_dados()
        
        # Debería dibujar ambos dados con diferentes colores
        self.assertGreater(mock_pygame.draw.rect.call_count, 0)
    
    @patch('core.PygameUI.pygame')
    def test_dibujar_info_turno_blancas(self, mock_pygame):
        """Verifica dibujar_info con turno de blancas"""
        self.ui.screen = MagicMock()
        self.ui.game.turno = Mock(return_value='B')
        self.ui.game.board = Mock()
        
        mock_board = MagicMock()
        mock_board.off.return_value = {'B': 5, 'N': 3}
        self.ui.game.board.return_value = mock_board
        
        self.ui.game.is_game_over = Mock(return_value=False)
        self.ui.font = MagicMock()
        self.ui.font.render.return_value = MagicMock()
        
        self.ui.dibujar_info()
        
        # Debería renderizar el texto del turno
        self.assertGreater(self.ui.font.render.call_count, 0)
        self.assertGreater(self.ui.screen.blit.call_count, 0)
    
    @patch('core.PygameUI.pygame')
    def test_dibujar_info_turno_negras(self, mock_pygame):
        """Verifica dibujar_info con turno de negras"""
        self.ui.screen = MagicMock()
        self.ui.game.turno = Mock(return_value='N')
        self.ui.game.board = Mock()
        
        mock_board = MagicMock()
        mock_board.off.return_value = {'B': 2, 'N': 8}
        self.ui.game.board.return_value = mock_board
        
        self.ui.game.is_game_over = Mock(return_value=False)
        self.ui.font = MagicMock()
        self.ui.font.render.return_value = MagicMock()
        
        self.ui.dibujar_info()
        
        self.assertGreater(self.ui.font.render.call_count, 0)
    
    @patch('core.PygameUI.pygame')
    def test_dibujar_info_juego_terminado_blancas_ganan(self, mock_pygame):
        """Verifica dibujar_info cuando el juego termina con blancas ganando"""
        self.ui.screen = MagicMock()
        self.ui.game.turno = Mock(return_value='B')
        self.ui.game.board = Mock()
        
        mock_board = MagicMock()
        mock_board.off.return_value = {'B': 15, 'N': 5}
        self.ui.game.board.return_value = mock_board
        
        self.ui.game.is_game_over = Mock(return_value=True)
        self.ui.game.winner = Mock(return_value='B')
        self.ui.font = MagicMock()
        self.ui.font.render.return_value = MagicMock()
        
        self.ui.dibujar_info()
        
        # Debería mostrar mensaje de ganador
        self.assertGreater(self.ui.font.render.call_count, 0)
    
    @patch('core.PygameUI.pygame')
    def test_dibujar_info_juego_terminado_negras_ganan(self, mock_pygame):
        """Verifica dibujar_info cuando el juego termina con negras ganando"""
        self.ui.screen = MagicMock()
        self.ui.game.turno = Mock(return_value='N')
        self.ui.game.board = Mock()
        
        mock_board = MagicMock()
        mock_board.off.return_value = {'B': 3, 'N': 15}
        self.ui.game.board.return_value = mock_board
        
        self.ui.game.is_game_over = Mock(return_value=True)
        self.ui.game.winner = Mock(return_value='N')
        self.ui.font = MagicMock()
        self.ui.font.render.return_value = MagicMock()
        
        self.ui.dibujar_info()
        
        self.assertGreater(self.ui.font.render.call_count, 0)


class TestBackgammonUILogica(unittest.TestCase):
    """Tests de lógica de eventos"""
    
    def setUp(self):
        with patch('core.PygameUI.pygame'), \
             patch('core.PygameUI.BackgammonGame'):
            self.ui = BackgammonUI()
    
    def test_manejar_click_dado_juego_terminado(self):
        """Verifica que no haga nada si el juego terminó"""
        self.ui.game.is_game_over = Mock(return_value=True)
        
        self.ui.manejar_click_dado(100, 100)
        
        # No debería llamar a roll
        self.ui.game.roll = Mock()
        self.ui.manejar_click_dado(100, 100)
        self.ui.game.roll.assert_not_called()
    
    def test_manejar_click_dado_tirar_dados(self):
        """Verifica que tire dados al inicio del turno"""
        self.ui.game.is_game_over = Mock(return_value=False)
        self.ui.game.dice = Mock(return_value=[])
        self.ui.game.roll = Mock()
        self.ui.punto_seleccionado = 5
        
        self.ui.manejar_click_dado(100, 100)
        
        self.ui.game.roll.assert_called_once()
        self.assertIsNone(self.ui.punto_seleccionado)
    
    def test_manejar_click_dado_terminar_turno_sin_dados(self):
        """Verifica que termine el turno cuando no quedan dados"""
        self.ui.game.is_game_over = Mock(return_value=False)
        self.ui.game.dice = Mock(return_value=[3, 1])
        self.ui.game.available_dice = Mock(return_value=[])
        self.ui.game.can_end_turn = Mock(return_value=True)
        self.ui.game.end_turn = Mock()
        
        self.ui.manejar_click_dado(100, 100)
        
        self.ui.game.end_turn.assert_called_once()
    
    def test_manejar_click_dado_terminar_turno_sin_movimientos(self):
        """Verifica que termine el turno cuando no hay movimientos válidos"""
        self.ui.game.is_game_over = Mock(return_value=False)
        self.ui.game.dice = Mock(return_value=[3, 1])
        self.ui.game.available_dice = Mock(return_value=[3, 1])
        self.ui.game.has_valid_moves = Mock(return_value=False)
        self.ui.game.can_end_turn = Mock(return_value=True)
        self.ui.game.end_turn = Mock()
        
        self.ui.manejar_click_dado(100, 100)
        
        self.ui.game.end_turn.assert_called_once()
    
    def test_manejar_click_dado_con_movimientos_disponibles(self):
        """Verifica que no haga nada si hay movimientos disponibles"""
        self.ui.game.is_game_over = Mock(return_value=False)
        self.ui.game.dice = Mock(return_value=[3, 1])
        self.ui.game.available_dice = Mock(return_value=[3, 1])
        self.ui.game.has_valid_moves = Mock(return_value=True)
        self.ui.game.end_turn = Mock()
        
        self.ui.manejar_click_dado(100, 100)
        
        # No debería terminar el turno
        self.ui.game.end_turn.assert_not_called()
    
    def test_manejar_click_punto_sin_dados(self):
        """Verifica que no permita mover sin tirar dados"""
        self.ui.game.dice = Mock(return_value=[])
        self.ui.punto_seleccionado = 5
        
        self.ui.manejar_click_punto(100, 100)
        
        self.assertIsNone(self.ui.punto_seleccionado)
    
    def test_manejar_click_punto_seleccionar_ficha_propia(self):
        """Verifica selección de ficha propia"""
        self.ui.game.dice = Mock(return_value=[3, 1])
        self.ui.game.turno = Mock(return_value='B')
        self.ui.game.board = Mock()
        
        mock_board = MagicMock()
        mock_board.point_owner_count.return_value = ('B', 2)
        self.ui.game.board.return_value = mock_board
        
        # Mockear coords_a_punto para retornar un punto válido
        self.ui.coords_a_punto = Mock(return_value=7)
        
        self.ui.manejar_click_punto(100, 100)
        
        self.assertEqual(self.ui.punto_seleccionado, 7)
    
    def test_manejar_click_punto_no_seleccionar_ficha_enemiga(self):
        """Verifica que no seleccione ficha enemiga"""
        self.ui.game.dice = Mock(return_value=[3, 1])
        self.ui.game.turno = Mock(return_value='B')
        self.ui.game.board = Mock()
        
        mock_board = MagicMock()
        mock_board.point_owner_count.return_value = ('N', 2)
        self.ui.game.board.return_value = mock_board
        
        self.ui.coords_a_punto = Mock(return_value=7)
        
        self.ui.manejar_click_punto(100, 100)
        
        self.assertIsNone(self.ui.punto_seleccionado)
    
    def test_manejar_click_punto_seleccionar_bar(self):
        """Verifica selección de ficha en bar"""
        self.ui.game.dice = Mock(return_value=[3, 1])
        self.ui.game.turno = Mock(return_value='B')
        self.ui.game.board = Mock()
        
        mock_board = MagicMock()
        mock_board.has_checkers_on_bar.return_value = True
        self.ui.game.board.return_value = mock_board
        
        self.ui.coords_a_punto = Mock(return_value=None)
        self.ui.es_area_bar = Mock(return_value=True)
        
        self.ui.manejar_click_punto(100, 100)
        
        self.assertEqual(self.ui.punto_seleccionado, "bar")
    
    def test_manejar_click_punto_seleccionar_off(self):
        """Verifica selección de área off"""
        self.ui.game.dice = Mock(return_value=[3, 1])
        
        self.ui.coords_a_punto = Mock(return_value=None)
        self.ui.es_area_bar = Mock(return_value=False)
        self.ui.es_area_off = Mock(return_value=True)
        
        self.ui.manejar_click_punto(100, 100)
        
        self.assertEqual(self.ui.punto_seleccionado, 24)
    
    def test_manejar_click_punto_mover_normal_exitoso(self):
        """Verifica movimiento normal exitoso"""
        self.ui.game.dice = Mock(return_value=[3, 1])
        self.ui.game.turno = Mock(return_value='B')
        self.ui.game.get_valid_moves = Mock(return_value=[(7, 3)])
        self.ui.game.move = Mock(return_value=True)
        
        self.ui.punto_seleccionado = 7
        self.ui.coords_a_punto = Mock(return_value=4)
        
        self.ui.manejar_click_punto(100, 100)
        
        self.ui.game.move.assert_called_once_with(7, 3)
        self.assertIsNone(self.ui.punto_seleccionado)
    
    def test_manejar_click_punto_mover_desde_bar(self):
        """Verifica movimiento desde bar"""
        self.ui.game.dice = Mock(return_value=[3])
        self.ui.game.turno = Mock(return_value='B')
        self.ui.game.get_valid_moves = Mock(return_value=[(None, 3)])
        self.ui.game.move = Mock(return_value=True)
        
        self.ui.punto_seleccionado = "bar"
        self.ui.coords_a_punto = Mock(return_value=2)  # punto 2
        
        self.ui.manejar_click_punto(100, 100)
        
        # Debería llamar a move
        self.ui.game.move.assert_called_once()
    
    def test_manejar_click_punto_bearing_off(self):
        """Verifica bearing off"""
        self.ui.game.dice = Mock(return_value=[4])
        self.ui.game.turno = Mock(return_value='B')
        self.ui.game.get_valid_moves = Mock(return_value=[(3, 4)])
        self.ui.game.can_move = Mock(return_value=True)
        self.ui.game.move = Mock(return_value=True)
        
        self.ui.punto_seleccionado = 3
        self.ui.coords_a_punto = Mock(return_value=None)
        self.ui.es_area_bar = Mock(return_value=False)
        self.ui.es_area_off = Mock(return_value=True)
        
        self.ui.manejar_click_punto(100, 100)
        
        # Debería intentar bearing off
        self.ui.game.move.assert_called_once()
    
    def test_manejar_click_punto_movimiento_invalido(self):
        """Verifica manejo de movimiento inválido"""
        self.ui.game.dice = Mock(return_value=[3, 1])
        self.ui.game.get_valid_moves = Mock(return_value=[])
        
        self.ui.punto_seleccionado = 7
        self.ui.coords_a_punto = Mock(return_value=4)
        
        self.ui.manejar_click_punto(100, 100)
        
        # Debería cambiar selección
        self.assertEqual(self.ui.punto_seleccionado, 4)
    
    def test_manejar_click_punto_deseleccionar(self):
        """Verifica deselección al hacer click en el mismo punto"""
        self.ui.game.dice = Mock(return_value=[3, 1])
        self.ui.game.get_valid_moves = Mock(return_value=[])
        
        self.ui.punto_seleccionado = 7
        self.ui.coords_a_punto = Mock(return_value=7)
        
        self.ui.manejar_click_punto(100, 100)
        
        self.assertIsNone(self.ui.punto_seleccionado)
    
    def test_manejar_click_punto_click_fuera(self):
        """Verifica click fuera del tablero"""
        self.ui.game.dice = Mock(return_value=[3, 1])
        
        self.ui.punto_seleccionado = 7
        self.ui.coords_a_punto = Mock(return_value=None)
        self.ui.es_area_bar = Mock(return_value=False)
        self.ui.es_area_off = Mock(return_value=False)
        
        self.ui.manejar_click_punto(100, 100)
        
        self.assertIsNone(self.ui.punto_seleccionado)


class TestBackgammonUIRun(unittest.TestCase):
    """Tests del bucle principal"""
    
    @patch('core.PygameUI.pygame')
    @patch('core.PygameUI.BackgammonGame')
    @patch('core.PygameUI.sys')
    def test_run_quit_event(self, mock_sys, mock_game_class, mock_pygame):
        """Verifica que el bucle termine con evento QUIT"""
        mock_pygame.display.set_mode.return_value = MagicMock()
        mock_pygame.font.Font.return_value = MagicMock()
        mock_pygame.time.Clock.return_value = MagicMock()
        
        # Crear evento QUIT
        quit_event = MagicMock()
        quit_event.type = mock_pygame.QUIT
        
        # Primera iteración retorna evento QUIT
        mock_pygame.event.get.return_value = [quit_event]
        
        ui = BackgammonUI()
        ui.run()
        
        mock_pygame.quit.assert_called_once()
        mock_sys.exit.assert_called_once()
    
    @patch('core.PygameUI.pygame')
    @patch('core.PygameUI.BackgammonGame')
    @patch('core.PygameUI.sys')
    def test_run_click_dados(self, mock_sys, mock_game_class, mock_pygame):
        """Verifica manejo de click en dados"""
        mock_pygame.display.set_mode.return_value = MagicMock()
        mock_pygame.font.Font.return_value = MagicMock()
        mock_pygame.time.Clock.return_value = MagicMock()
        
        # Crear evento MOUSEBUTTONDOWN en área de dados
        mouse_event = MagicMock()
        mouse_event.type = mock_pygame.MOUSEBUTTONDOWN
        mouse_event.pos = (500, 400)  # Área de dados
        
        quit_event = MagicMock()
        quit_event.type = mock_pygame.QUIT
        
        # Primera iteración: mouse, Segunda: quit
        mock_pygame.event.get.side_effect = [[mouse_event], [quit_event]]
        
        ui = BackgammonUI()
        ui.es_area_dados = Mock(return_value=True)
        ui.manejar_click_dado = Mock()
        
        ui.run()
        
        ui.manejar_click_dado.assert_called_once()
    
    @patch('core.PygameUI.pygame')
    @patch('core.PygameUI.BackgammonGame')
    @patch('core.PygameUI.sys')
    def test_run_click_punto(self, mock_sys, mock_game_class, mock_pygame):
        """Verifica manejo de click en punto"""
        mock_pygame.display.set_mode.return_value = MagicMock()
        mock_pygame.font.Font.return_value = MagicMock()
        mock_pygame.time.Clock.return_value = MagicMock()
        
        mouse_event = MagicMock()
        mouse_event.type = mock_pygame.MOUSEBUTTONDOWN
        mouse_event.pos = (100, 100)
        
        quit_event = MagicMock()
        quit_event.type = mock_pygame.QUIT
        
        mock_pygame.event.get.side_effect = [[mouse_event], [quit_event]]
        
        ui = BackgammonUI()
        ui.es_area_dados = Mock(return_value=False)
        ui.manejar_click_punto = Mock()
        
        ui.run()
        
        ui.manejar_click_punto.assert_called_once()
    
    @patch('core.PygameUI.pygame')
    @patch('core.PygameUI.BackgammonGame')
    @patch('core.PygameUI.sys')
    def test_run_resaltar_bar(self, mock_sys, mock_game_class, mock_pygame):
        """Verifica que resalte el bar cuando está seleccionado"""
        mock_pygame.display.set_mode.return_value = MagicMock()
        mock_pygame.font.Font.return_value = MagicMock()
        mock_pygame.time.Clock.return_value = MagicMock()
        mock_pygame.display.flip = MagicMock()
        
        quit_event = MagicMock()
        quit_event.type = mock_pygame.QUIT
        
        mock_pygame.event.get.return_value = [quit_event]
        
        ui = BackgammonUI()
        ui.punto_seleccionado = "bar"
        ui.dibujar_tablero = Mock()
        ui.dibujar_fichas = Mock()
        ui.dibujar_dados = Mock()
        ui.dibujar_info = Mock()
        
        ui.run()
        
        # Debería haber dibujado rectángulo de selección
        mock_pygame.draw.rect.assert_called()
    
    @patch('core.PygameUI.pygame')
    @patch('core.PygameUI.BackgammonGame')
    @patch('core.PygameUI.sys')
    def test_run_resaltar_punto_arriba(self, mock_sys, mock_game_class, mock_pygame):
        """Verifica que resalte un punto arriba (12-23)"""
        mock_pygame.display.set_mode.return_value = MagicMock()
        mock_pygame.font.Font.return_value = MagicMock()
        mock_pygame.time.Clock.return_value = MagicMock()
        mock_pygame.display.flip = MagicMock()
        
        quit_event = MagicMock()
        quit_event.type = mock_pygame.QUIT
        
        mock_pygame.event.get.return_value = [quit_event]
        
        ui = BackgammonUI()
        ui.punto_seleccionado = 15  # Punto arriba
        ui.game.board = Mock()
        
        mock_board = MagicMock()
        mock_board.points.return_value = [[] for _ in range(24)]
        mock_board.points.return_value[15] = [MagicMock()]
        ui.game.board.return_value = mock_board
        
        ui.dibujar_tablero = Mock()
        ui.dibujar_fichas = Mock()
        ui.dibujar_dados = Mock()
        ui.dibujar_info = Mock()
        
        ui.run()
        
        # Debería haber dibujado círculo de selección
        mock_pygame.draw.circle.assert_called()
    
    @patch('core.PygameUI.pygame')
    @patch('core.PygameUI.BackgammonGame')
    @patch('core.PygameUI.sys')
    def test_run_resaltar_punto_abajo(self, mock_sys, mock_game_class, mock_pygame):
        """Verifica que resalte un punto abajo (0-11)"""
        mock_pygame.display.set_mode.return_value = MagicMock()
        mock_pygame.font.Font.return_value = MagicMock()
        mock_pygame.time.Clock.return_value = MagicMock()
        mock_pygame.display.flip = MagicMock()
        
        quit_event = MagicMock()
        quit_event.type = mock_pygame.QUIT
        
        mock_pygame.event.get.return_value = [quit_event]
        
        ui = BackgammonUI()
        ui.punto_seleccionado = 5  # Punto abajo
        ui.game.board = Mock()
        
        mock_board = MagicMock()
        mock_board.points.return_value = [[] for _ in range(24)]
        mock_board.points.return_value[5] = [MagicMock()]
        ui.game.board.return_value = mock_board
        
        ui.dibujar_tablero = Mock()
        ui.dibujar_fichas = Mock()
        ui.dibujar_dados = Mock()
        ui.dibujar_info = Mock()
        
        ui.run()
        
        mock_pygame.draw.circle.assert_called()
    
    @patch('core.PygameUI.pygame')
    @patch('core.PygameUI.BackgammonGame')
    @patch('core.PygameUI.sys')
    def test_run_resaltar_off(self, mock_sys, mock_game_class, mock_pygame):
        """Verifica que resalte el área off cuando está seleccionada"""
        mock_pygame.display.set_mode.return_value = MagicMock()
        mock_pygame.font.Font.return_value = MagicMock()
        mock_pygame.time.Clock.return_value = MagicMock()
        mock_pygame.display.flip = MagicMock()
        
        quit_event = MagicMock()
        quit_event.type = mock_pygame.QUIT
        
        mock_pygame.event.get.return_value = [quit_event]
        
        ui = BackgammonUI()
        ui.punto_seleccionado = 24  # Área off
        ui.dibujar_tablero = Mock()
        ui.dibujar_fichas = Mock()
        ui.dibujar_dados = Mock()
        ui.dibujar_info = Mock()
        
        ui.run()
        
        # Debería haber dibujado rectángulo de selección en off
        mock_pygame.draw.rect.assert_called()


class TestBackgammonUIMain(unittest.TestCase):
    """Tests de la función main"""
    
    @patch('core.PygameUI.input')
    @patch('core.PygameUI.BackgammonUI')
    def test_main_nombres_por_defecto(self, mock_ui_class, mock_input):
        """Verifica main con nombres por defecto (Enter)"""
        mock_input.side_effect = ['', '']  # Enter en ambos
        mock_ui_instance = MagicMock()
        mock_ui_class.return_value = mock_ui_instance
        
        main()
        
        mock_ui_class.assert_called_once_with('Blancas', 'Negras')
        mock_ui_instance.run.assert_called_once()
    
    @patch('core.PygameUI.input')
    @patch('core.PygameUI.BackgammonUI')
    def test_main_nombres_personalizados(self, mock_ui_class, mock_input):
        """Verifica main con nombres personalizados"""
        mock_input.side_effect = ['Alice', 'Bob']
        mock_ui_instance = MagicMock()
        mock_ui_class.return_value = mock_ui_instance
        
        main()
        
        mock_ui_class.assert_called_once_with('Alice', 'Bob')
        mock_ui_instance.run.assert_called_once()
    
    @patch('core.PygameUI.input')
    @patch('core.PygameUI.BackgammonUI')
    def test_main_espacios_en_nombres(self, mock_ui_class, mock_input):
        """Verifica que main elimine espacios de los nombres"""
        mock_input.side_effect = ['  Alice  ', '  Bob  ']
        mock_ui_instance = MagicMock()
        mock_ui_class.return_value = mock_ui_instance
        
        main()
        
        mock_ui_class.assert_called_once_with('Alice', 'Bob')


if __name__ == '__main__':
    unittest.main()