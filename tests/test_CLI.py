"""
Tests completos para CLI.py - Parte 2
Comandos: legal y move
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import cli.CLI as CLI_module


class TestMainLegalCommand(unittest.TestCase):
    """Tests para el comando 'legal'"""
    
    def setUp(self):
        CLI_module.HISTORY.clear()
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_legal_uso_incorrecto_sin_parametro(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica error cuando 'legal' no tiene parámetro"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game_class.return_value = MagicMock()
        
        mock_input.side_effect = ['legal', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Uso: legal' in str(call) for call in calls))
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_legal_parametro_no_numerico(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica error cuando el parámetro no es número"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game_class.return_value = MagicMock()
        
        mock_input.side_effect = ['legal abc', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Uso: legal' in str(call) for call in calls))
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_legal_fuera_de_rango(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica error cuando el punto está fuera de rango"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game_class.return_value = MagicMock()
        
        mock_input.side_effect = ['legal 25', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('entre 1 y 24' in str(call) for call in calls))
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_legal_punto_vacio(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica error cuando no hay fichas en el punto"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game = MagicMock()
        mock_board = MagicMock()
        mock_board.points.return_value = [[] for _ in range(24)]  # Todos vacíos
        mock_game.board.return_value = mock_board
        mock_game_class.return_value = mock_game
        
        mock_input.side_effect = ['legal 12', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('No hay fichas' in str(call) for call in calls))
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_legal_ficha_enemiga(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica error cuando la ficha no es del jugador actual"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game = MagicMock()
        mock_board = MagicMock()
        
        # Crear ficha negra
        mock_checker = MagicMock()
        mock_checker.color.return_value = 'N'
        
        mock_board.points.return_value = [[] for _ in range(24)]
        mock_board.points.return_value[11] = [mock_checker]  # Punto 12 en humano
        
        mock_game.board.return_value = mock_board
        mock_game.turno.return_value = 'B'  # Turno de blancas
        mock_game_class.return_value = mock_game
        
        mock_input.side_effect = ['legal 12', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('no es tuya' in str(call) for call in calls))
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_legal_sin_dados(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica error cuando no se han tirado los dados"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game = MagicMock()
        mock_board = MagicMock()
        
        mock_checker = MagicMock()
        mock_checker.color.return_value = 'B'
        
        mock_board.points.return_value = [[] for _ in range(24)]
        mock_board.points.return_value[11] = [mock_checker]
        
        mock_game.board.return_value = mock_board
        mock_game.turno.return_value = 'B'
        mock_game.dice.return_value = []  # Sin dados
        mock_game_class.return_value = mock_game
        
        mock_input.side_effect = ['legal 12', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Primero tirá' in str(call) for call in calls))
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_legal_sin_movimientos_validos(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica mensaje cuando no hay movimientos válidos"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game = MagicMock()
        mock_board = MagicMock()
        
        mock_checker = MagicMock()
        mock_checker.color.return_value = 'B'
        
        mock_board.points.return_value = [[] for _ in range(24)]
        mock_board.points.return_value[11] = [mock_checker]
        
        # Mock para que no haya movimientos válidos
        mock_board.point_owner_count = Mock(return_value=('N', 2))  # Bloqueado
        
        mock_game.board.return_value = mock_board
        mock_game.turno.return_value = 'B'
        mock_game.dice.return_value = [3, 1]
        mock_game_class.return_value = mock_game
        
        mock_input.side_effect = ['legal 12', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('No hay destinos válidos' in str(call) for call in calls))
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_legal_con_opciones(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica que muestre opciones válidas"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game = MagicMock()
        mock_board = MagicMock()
        
        mock_checker = MagicMock()
        mock_checker.color.return_value = 'B'
        
        mock_board.points.return_value = [[] for _ in range(24)]
        mock_board.points.return_value[22] = [mock_checker]  # Punto 23 en humano
        
        # Mock para que haya movimientos válidos
        mock_board.point_owner_count = Mock(return_value=(None, 0))  # Vacío
        
        mock_game.board.return_value = mock_board
        mock_game.turno.return_value = 'B'
        mock_game.dice.return_value = [3, 1]
        mock_game_class.return_value = mock_game
        
        mock_input.side_effect = ['legal 23', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Opciones desde' in str(call) for call in calls))
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_l_shortcut(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica atajo 'l' para legal"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game = MagicMock()
        mock_board = MagicMock()
        
        mock_board.points.return_value = [[] for _ in range(24)]
        mock_game.board.return_value = mock_board
        mock_game_class.return_value = mock_game
        
        mock_input.side_effect = ['l 12', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        # Debería procesar el comando legal
        self.assertEqual(mock_input.call_count, 2)


class TestMainMoveCommand(unittest.TestCase):
    """Tests para el comando 'move'"""
    
    def setUp(self):
        CLI_module.HISTORY.clear()
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_move_uso_incorrecto(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica error con uso incorrecto de move"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game_class.return_value = MagicMock()
        
        mock_input.side_effect = ['move 12', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Uso: move' in str(call) for call in calls))
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_move_sin_dados(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica error cuando no se han tirado dados"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game = MagicMock()
        mock_game.dice.return_value = []
        mock_game_class.return_value = mock_game
        
        mock_input.side_effect = ['move 23 20', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Primero tirá' in str(call) for call in calls))
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_move_fuera_de_rango(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica error con puntos fuera de rango"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game = MagicMock()
        mock_game.dice.return_value = [3, 1]
        mock_game_class.return_value = mock_game
        
        mock_input.side_effect = ['move 25 20', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('entre 1 y 24' in str(call) for call in calls))
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_move_punto_origen_vacio(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica error cuando el origen está vacío"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game = MagicMock()
        mock_board = MagicMock()
        mock_board.points.return_value = [[] for _ in range(24)]
        
        mock_game.board.return_value = mock_board
        mock_game.dice.return_value = [3, 1]
        mock_game_class.return_value = mock_game
        
        mock_input.side_effect = ['move 12 9', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('No hay fichas' in str(call) for call in calls))
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_move_ficha_enemiga(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica error cuando se intenta mover ficha enemiga"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game = MagicMock()
        mock_board = MagicMock()
        
        mock_checker = MagicMock()
        mock_checker.color.return_value = 'N'
        
        mock_board.points.return_value = [[] for _ in range(24)]
        mock_board.points.return_value[11] = [mock_checker]
        
        mock_game.board.return_value = mock_board
        mock_game.turno.return_value = 'B'
        mock_game.dice.return_value = [3, 1]
        mock_game_class.return_value = mock_game
        
        mock_input.side_effect = ['move 12 9', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('no es tuya' in str(call) for call in calls))
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_move_direccion_invalida(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica error con dirección inválida"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game = MagicMock()
        mock_board = MagicMock()
        
        mock_checker = MagicMock()
        mock_checker.color.return_value = 'B'
        
        mock_board.points.return_value = [[] for _ in range(24)]
        mock_board.points.return_value[11] = [mock_checker]
        
        mock_game.board.return_value = mock_board
        mock_game.turno.return_value = 'B'
        mock_game.dice.return_value = [3, 1]
        mock_game_class.return_value = mock_game
        
        # Blancas intentan moverse hacia adelante (incorrecto)
        mock_input.side_effect = ['move 12 15', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Dirección inválida' in str(call) for call in calls))
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_move_destino_bloqueado(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica error cuando el destino está bloqueado"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game = MagicMock()
        mock_board = MagicMock()
        
        mock_checker = MagicMock()
        mock_checker.color.return_value = 'B'
        
        mock_board.points.return_value = [[] for _ in range(24)]
        mock_board.points.return_value[22] = [mock_checker]  # Punto 23
        
        # Destino bloqueado
        mock_board.point_owner_count.return_value = ('N', 2)
        
        mock_game.board.return_value = mock_board
        mock_game.turno.return_value = 'B'
        mock_game.dice.return_value = [3, 1]
        mock_game_class.return_value = mock_game
        
        mock_input.side_effect = ['move 23 20', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('bloqueado' in str(call) for call in calls))
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_move_dado_no_disponible(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica error cuando el dado no está disponible"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game = MagicMock()
        mock_board = MagicMock()
        
        mock_checker = MagicMock()
        mock_checker.color.return_value = 'B'
        
        mock_board.points.return_value = [[] for _ in range(24)]
        mock_board.points.return_value[22] = [mock_checker]
        
        mock_board.point_owner_count.return_value = (None, 0)
        
        mock_game.board.return_value = mock_board
        mock_game.turno.return_value = 'B'
        mock_game.dice.return_value = [3, 1]  # Solo tiene 3 y 1
        mock_game_class.return_value = mock_game
        
        # Intenta mover 5 espacios (no disponible)
        mock_input.side_effect = ['move 23 18', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('No tenés el valor' in str(call) for call in calls))
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_move_exitoso(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica movimiento exitoso"""
        CLI_module.HISTORY.clear()
        
        mock_prompt.return_value = ('P1', 'P2')
        mock_game = MagicMock()
        mock_board = MagicMock()
        
        mock_checker = MagicMock()
        mock_checker.color.return_value = 'B'
        
        mock_board.points.return_value = [[] for _ in range(24)]
        mock_board.points.return_value[22] = [mock_checker]  # Punto 23
        
        mock_board.point_owner_count.return_value = (None, 0)
        
        mock_game.board.return_value = mock_board
        mock_game.turno.return_value = 'B'
        mock_game.dice.return_value = [3, 1]
        mock_game_class.return_value = mock_game
        
        mock_input.side_effect = ['move 23 20', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        # Verificar que se movió la ficha
        self.assertEqual(len(mock_board.points.return_value[22]), 0)  # Origen vacío
        self.assertEqual(len(mock_board.points.return_value[19]), 1)  # Destino con ficha
        
        # Verificar mensaje de éxito
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Movida OK' in str(call) for call in calls))
        
        # Verificar historial
        self.assertTrue(any('movió' in entry for entry in CLI_module.HISTORY))
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_move_con_captura(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica movimiento con captura (blot)"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game = MagicMock()
        mock_board = MagicMock()
        
        mock_checker_b = MagicMock()
        mock_checker_b.color.return_value = 'B'
        
        mock_checker_n = MagicMock()
        mock_checker_n.color.return_value = 'N'
        
        mock_board.points.return_value = [[] for _ in range(24)]
        mock_board.points.return_value[22] = [mock_checker_b]  # Punto 23 - Blanca
        mock_board.points.return_value[19] = [mock_checker_n]  # Punto 20 - Negra sola (blot)
        
        mock_board.point_owner_count.return_value = ('N', 1)  # Blot
        
        mock_game.board.return_value = mock_board
        mock_game.turno.return_value = 'B'
        mock_game.dice.return_value = [3, 1]
        mock_game_class.return_value = mock_game
        
        mock_input.side_effect = ['move 23 20', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        # La ficha negra debería haber sido capturada
        self.assertEqual(len(mock_board.points.return_value[19]), 1)  # Solo queda la blanca
    
    @patch('cli.CLI.prompt_nombres')
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_m_shortcut(self, mock_print, mock_input, mock_game_class, mock_prompt):
        """Verifica atajo 'm' para move"""
        mock_prompt.return_value = ('P1', 'P2')
        mock_game = MagicMock()
        mock_board = MagicMock()
        
        mock_checker = MagicMock()
        mock_checker.color.return_value = 'B'
        
        mock_board.points.return_value = [[] for _ in range(24)]
        mock_board.points.return_value[22] = [mock_checker]
        
        mock_board.point_owner_count.return_value = (None, 0)
        
        mock_game.board.return_value = mock_board
        mock_game.turno.return_value = 'B'
        mock_game.dice.return_value = [3]
        mock_game_class.return_value = mock_game
        
        mock_input.side_effect = ['m 23 20', 'quit']
        
        with patch('cli.CLI.render_board_ascii', return_value='board'):
            CLI_module.main()
        
        # Debería haber procesado el movimiento
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Movida OK' in str(call) for call in calls))


if __name__ == '__main__':
    unittest.main()