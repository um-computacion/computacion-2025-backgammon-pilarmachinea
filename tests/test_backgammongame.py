import unittest
from core.BackgammonGame import BackgammonGame
from core.Dice import Dice 
from unittest.mock import MagicMock, patch

# --- TESTS BÁSICOS ---

class TestBackgammonGameBasico(unittest.TestCase):
    def test_turno_inicial(self):
        g = BackgammonGame()
        self.assertEqual(g.turno(), 'B') 

    def test_jugadores_diccionario(self):
        g = BackgammonGame()
        jugadores = g.players()
        self.assertIsInstance(jugadores, dict)
        self.assertEqual(len(jugadores), 2)
        self.assertIn('B', jugadores)
        self.assertIn('N', jugadores)

    def test_nombres_por_defecto(self):
        g = BackgammonGame()
        jugadores = g.players()
        self.assertEqual(jugadores['B'].nombre(), 'Blancas')
        self.assertEqual(jugadores['N'].nombre(), 'Negras')

    def test_nombres_personalizados(self):
        """Test para nombres personalizados de jugadores"""
        g = BackgammonGame(player1="Alice", player2="Bob")
        jugadores = g.players()
        self.assertEqual(jugadores['B'].nombre(), 'Alice')
        self.assertEqual(jugadores['N'].nombre(), 'Bob')

    def test_board_existe(self):
        g = BackgammonGame()
        tablero = g.board()
        self.assertIsNotNone(tablero)
        self.assertTrue(hasattr(tablero, 'point_owner_count'))

    def test_roll_y_dice_cache(self):
        g = BackgammonGame()
        tirada = g.roll()
        self.assertIn(len(tirada), [2, 4])
        cache = g.dice()
        self.assertEqual(cache, tirada)
        self.assertIsNot(cache, tirada) 


# --- TESTS FUNCIONALES (Críticos para la Cobertura) ---

class TestBackgammonGameFuncional(unittest.TestCase):

    def setUp(self):
        self.g = BackgammonGame() 
        
    # Test 1: available_dice_inicial 
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_available_dice_inicial(self, mock_roll):
        """Verifica que available_dice retorne los dados no usados inmediatamente después de roll."""
        self.g.roll() 
        self.assertCountEqual(self.g.available_dice(), [3, 1])

    # Test 2: move_consume_dice
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_move_consume_dice(self, mock_roll):
        """Verifica que un movimiento exitoso consuma el dado."""
        self.g.roll()
        
        with patch.object(self.g.board(), 'move', return_value=True):
            with patch.object(self.g.board(), 'can_move', return_value=True):
                with patch.object(self.g, 'is_game_over', return_value=False):
                    self.assertTrue(self.g.move(7, 3)) 
            
        self.assertCountEqual(self.g.available_dice(), [1]) 

    # Test 3: move_ilegal_no_consume_dice
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_move_ilegal_no_consume_dice(self, mock_roll):
        """Verifica que un movimiento ilegal no consuma el dado."""
        self.g.roll()
        
        # Falla por dado no disponible
        self.assertFalse(self.g.move(7, 5)) 
        
        # Falla por lógica de tablero
        self.assertFalse(self.g.move(0, 3)) 
        
        self.assertCountEqual(self.g.available_dice(), [3, 1]) 

    # Test 4: test_dice_cache_persists_after_consumption
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_dice_cache_persists_after_consumption(self, mock_roll):
        """Verifica que dice() retorne el cache original de la tirada."""
        self.g.roll() 
        
        with patch.object(self.g.board(), 'move', return_value=True):
            with patch.object(self.g.board(), 'can_move', return_value=True):
                with patch.object(self.g, 'is_game_over', return_value=False):
                    with patch.object(self.g, 'available_dice', side_effect=[[3, 1], [1], []]):
                        self.g.move(7, 3)
        
        # El cache original debe persistir
        self.assertCountEqual(self.g.dice(), [3, 1]) 

    # Test 5: test_can_end_turn_bloqueado
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_can_end_turn_bloqueado(self, mock_roll):
        """Verifica can_end_turn cuando quedan dados pero no hay movimientos válidos."""
        self.g.roll()

        with patch.object(self.g, 'has_valid_moves', return_value=False):
            self.assertTrue(self.g.can_end_turn()) 

    # Test 6: test_can_end_turn_no_dados_disponibles
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_can_end_turn_no_dados_disponibles(self, mock_roll):
        """Verifica can_end_turn cuando no quedan dados."""
        self.g.roll()
        
        # Simular que no hay dados disponibles
        with patch.object(self.g, 'available_dice', return_value=[]):
            self.assertTrue(self.g.can_end_turn())

    # Test 7: test_end_turn_alterna_jugador
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_end_turn_alterna_jugador(self, mock_roll):
        """Verifica que end_turn cambie el turno y limpie el estado."""
        
        self.g.roll()
        self.assertEqual(self.g.turno(), 'B') 
        
        self.g.end_turn()
        self.assertEqual(self.g.turno(), 'N')
        
        self.g.end_turn()
        self.assertEqual(self.g.turno(), 'B')
        
        self.assertCountEqual(self.g.dice(), [])


# --- TESTS ADICIONALES PARA COBERTURA COMPLETA ---

class TestBackgammonGameCoberturaCompleta(unittest.TestCase):
    
    def setUp(self):
        self.g = BackgammonGame()
    
    # TEST: current_player con turno de Blancas
    def test_current_player_blancas(self):
        """Verifica que current_player retorne el jugador blanco cuando es su turno."""
        # El turno inicial es 'B'
        player = self.g.current_player()
        self.assertEqual(player.obtener_color(), 'blanco')
    
    # TEST: current_player con turno de Negras
    def test_current_player_negras(self):
        """Verifica que current_player retorne el jugador negro cuando es su turno."""
        # Cambiar al turno de negras
        self.g.end_turn()
        player = self.g.current_player()
        self.assertEqual(player.obtener_color(), 'negro')
    
    # TEST: can_move retorna False cuando dado no disponible
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_can_move_dado_no_disponible(self, mock_roll):
        """Verifica que can_move retorne False si el dado no está disponible."""
        self.g.roll()
        self.assertFalse(self.g.can_move(7, 5))  # 5 no está en [3, 1]
    
    # TEST: can_move delega correctamente al board
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_can_move_delega_a_board(self, mock_roll):
        """Verifica que can_move delegue correctamente al board."""
        self.g.roll()
        
        with patch.object(self.g.board(), 'can_move', return_value=True) as mock_board:
            result = self.g.can_move(7, 3)
            self.assertTrue(result)
            mock_board.assert_called_once_with(7, 3, 'B')
    
    # TEST: get_valid_moves delega al board
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_get_valid_moves(self, mock_roll):
        """Verifica que get_valid_moves delegue al board con dados disponibles."""
        self.g.roll()
        
        expected_moves = [(7, 3), (23, 1)]
        with patch.object(self.g.board(), 'get_valid_moves', return_value=expected_moves) as mock_board:
            moves = self.g.get_valid_moves()
            self.assertEqual(moves, expected_moves)
            mock_board.assert_called_once_with('B', [3, 1])
    
    # TEST: has_valid_moves retorna True cuando hay movimientos
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_has_valid_moves_true(self, mock_roll):
        """Verifica que has_valid_moves retorne True cuando hay movimientos válidos."""
        self.g.roll()
        
        with patch.object(self.g, 'get_valid_moves', return_value=[(7, 3), (23, 1)]):
            self.assertTrue(self.g.has_valid_moves())
    
    # TEST: has_valid_moves retorna False cuando no hay movimientos
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_has_valid_moves_false(self, mock_roll):
        """Verifica que has_valid_moves retorne False cuando no hay movimientos válidos."""
        self.g.roll()
        
        with patch.object(self.g, 'get_valid_moves', return_value=[]):
            self.assertFalse(self.g.has_valid_moves())
    
    # TEST: can_end_turn retorna False si no se ha tirado
    def test_can_end_turn_sin_tirada(self):
        """Verifica que can_end_turn retorne False si no se ha tirado."""
        self.assertFalse(self.g.can_end_turn())
    
    # TEST: can_end_turn retorna True si no hay dados disponibles
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_can_end_turn_sin_dados_disponibles(self, mock_roll):
        """Verifica que can_end_turn retorne True cuando no quedan dados."""
        self.g.roll()
        
        # Simular que no hay dados disponibles
        with patch.object(self.g, 'available_dice', return_value=[]):
            self.assertTrue(self.g.can_end_turn())
    
    # TEST: can_end_turn retorna True si hay dados pero no hay movimientos válidos
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_can_end_turn_sin_movimientos_validos(self, mock_roll):
        """Verifica que can_end_turn retorne True cuando hay dados pero no movimientos."""
        self.g.roll()
        
        with patch.object(self.g, 'has_valid_moves', return_value=False):
            self.assertTrue(self.g.can_end_turn())
    
    # TEST: move retorna False cuando dado no disponible
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_move_dado_no_disponible(self, mock_roll):
        """Verifica que move retorne False si el dado no está disponible."""
        self.g.roll()
        self.assertFalse(self.g.move(7, 5))
    
    # TEST: move retorna False cuando can_move retorna False
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_move_can_move_false(self, mock_roll):
        """Verifica que move retorne False cuando can_move retorna False."""
        self.g.roll()
        
        with patch.object(self.g, 'can_move', return_value=False):
            self.assertFalse(self.g.move(7, 3))
    
    # TEST: move retorna False cuando board.move falla
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_move_board_move_false(self, mock_roll):
        """Verifica que move retorne False cuando board.move falla."""
        self.g.roll()
        
        with patch.object(self.g, 'can_move', return_value=True):
            with patch.object(self.g.board(), 'move', return_value=False):
                self.assertFalse(self.g.move(7, 3))
    
    # TEST: move exitoso consume dado
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_move_exitoso_consume_dado(self, mock_roll):
        """Verifica que un movimiento exitoso consume el dado."""
        self.g.roll()
        
        with patch.object(self.g, 'can_move', return_value=True):
            with patch.object(self.g.board(), 'move', return_value=True):
                with patch.object(self.g, 'is_game_over', return_value=False):
                    with patch.object(self.g, 'available_dice', side_effect=[[3, 1], [1]]):
                        self.assertTrue(self.g.move(7, 3))
    
    # TEST: move con victoria imprime mensaje
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_move_con_victoria(self, mock_roll):
        """Verifica que move detecte victoria."""
        self.g.roll()
        
        # Simular que el dado está disponible inicialmente
        original_available = self.g.available_dice
        
        with patch.object(self.g, 'can_move', return_value=True):
            with patch.object(self.g.board(), 'move', return_value=True):
                with patch.object(self.g, 'is_game_over', return_value=True):
                    with patch('builtins.print') as mock_print:
                        # available_dice debe retornar [3,1] primero (check inicial)
                        # luego [1] después de usar el dado
                        result = self.g.move(7, 3)
                        self.assertTrue(result)
                        # Verifica que se imprimió el mensaje de victoria
                        mock_print.assert_called()
    
    # TEST: move termina turno automáticamente cuando no quedan dados
    @patch.object(Dice, 'roll', return_value=[3])
    def test_move_termina_turno_sin_dados(self, mock_roll):
        """Verifica que move termine el turno automáticamente cuando no quedan dados."""
        self.g.roll()
        turno_inicial = self.g.turno()
        
        with patch.object(self.g, 'can_move', return_value=True):
            with patch.object(self.g.board(), 'move', return_value=True):
                with patch.object(self.g, 'is_game_over', return_value=False):
                    # El movimiento consume el único dado, triggereando end_turn automático
                    self.g.move(7, 3)
                    
                    # Verificar que el turno cambió
                    self.assertNotEqual(self.g.turno(), turno_inicial)
    
    # TEST: is_game_over retorna False al inicio
    def test_is_game_over_false(self):
        """Verifica que is_game_over retorne False al inicio del juego."""
        self.assertFalse(self.g.is_game_over())
    
    # TEST: is_game_over retorna True cuando Blancas ganan
    def test_is_game_over_blancas_ganan(self):
        """Verifica que is_game_over retorne True cuando Blancas retiran 15 fichas."""
        with patch.object(self.g.board(), 'off', return_value={'B': 15, 'N': 0}):
            self.assertTrue(self.g.is_game_over())
    
    # TEST: is_game_over retorna True cuando Negras ganan
    def test_is_game_over_negras_ganan(self):
        """Verifica que is_game_over retorne True cuando Negras retiran 15 fichas."""
        with patch.object(self.g.board(), 'off', return_value={'B': 0, 'N': 15}):
            self.assertTrue(self.g.is_game_over())
    
    # TEST: winner retorna None al inicio
    def test_winner_none(self):
        """Verifica que winner retorne None cuando no hay ganador."""
        self.assertIsNone(self.g.winner())
    
    # TEST: winner retorna 'B' cuando Blancas ganan
    def test_winner_blancas(self):
        """Verifica que winner retorne 'B' cuando Blancas ganan."""
        with patch.object(self.g.board(), 'off', return_value={'B': 15, 'N': 0}):
            self.assertEqual(self.g.winner(), 'B')
    
    # TEST: winner retorna 'N' cuando Negras ganan
    def test_winner_negras(self):
        """Verifica que winner retorne 'N' cuando Negras ganan."""
        with patch.object(self.g.board(), 'off', return_value={'B': 0, 'N': 15}):
            self.assertEqual(self.g.winner(), 'N')
    
    # TEST: available_dice con dados duplicados (dobles)
    @patch.object(Dice, 'roll', return_value=[4, 4, 4, 4])
    def test_available_dice_dobles(self, mock_roll):
        """Verifica available_dice con dobles."""
        self.g.roll()
        self.assertEqual(len(self.g.available_dice()), 4)
        
        # Usar dos dados
        with patch.object(self.g, 'can_move', return_value=True):
            with patch.object(self.g.board(), 'move', return_value=True):
                with patch.object(self.g, 'is_game_over', return_value=False):
                    with patch.object(self.g, 'available_dice', side_effect=[[4,4,4,4], [4,4,4], [4,4], [4]]):
                        self.g.move(7, 4)
                        self.g.move(7, 4)
    
    # TEST: end_turn limpia dados y cambia turno correctamente
    @patch.object(Dice, 'roll', return_value=[3, 1])
    def test_end_turn_limpia_estado(self, mock_roll):
        """Verifica que end_turn limpie los dados y cambie el turno."""
        self.g.roll()
        
        turno_inicial = self.g.turno()
        self.g.end_turn()
        
        # Verificar que cambió el turno
        self.assertNotEqual(self.g.turno(), turno_inicial)
        
        # Verificar que se limpiaron los dados
        self.assertEqual(self.g.dice(), [])
        self.assertEqual(self.g.available_dice(), [])


if __name__ == '__main__':
    unittest.main()