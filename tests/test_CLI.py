import unittest
from unittest.mock import Mock, patch
import sys
from io import StringIO

# Importar desde la estructura del proyecto
from cli.CLI import (
    index_from_human,
    distance_for_move,
    consume_die,
    do_hit_if_single,
    legal_moves_from,
    render_board_ascii,
    print_help,
    prompt_nombres,
    main,
    OWNER_ICON
)

def setup_mock_game():
    """Helper para crear un mock de game completamente configurado"""
    mock_game = Mock()
    mock_board = Mock()
    mock_game.board.return_value = mock_board
    mock_game.turno.return_value = "B"
    mock_game.players.return_value = {"B": Mock(), "N": Mock()}
    mock_game.dice.return_value = None
    mock_board.point_owner_count.return_value = (None, 0)
    return mock_game, mock_board

class TestIndexFromHuman(unittest.TestCase):
    """Tests para la función index_from_human"""
    def test_valid_index_min(self):
        """Convierte 1 a índice 0"""
        self.assertEqual(index_from_human(1), 0)
    
    def test_valid_index_max(self):
        """Convierte 24 a índice 23"""
        self.assertEqual(index_from_human(24), 23)
    
    def test_valid_index_middle(self):
        """Convierte 12 a índice 11"""
        self.assertEqual(index_from_human(12), 11)
    
    def test_invalid_index_too_low(self):
        """Rechaza índice 0"""
        with self.assertRaises(ValueError) as context:
            index_from_human(0)
        self.assertIn("debe estar entre 1 y 24", str(context.exception))
    
    def test_invalid_index_too_high(self):
        """Rechaza índice mayor a 24"""
        with self.assertRaises(ValueError) as context:
            index_from_human(25)
        self.assertIn("debe estar entre 1 y 24", str(context.exception))
    
    def test_invalid_index_negative(self):
        """Rechaza índice negativo"""
        with self.assertRaises(ValueError):
            index_from_human(-1)

class TestDistanceForMove(unittest.TestCase):
    """Tests para la función distance_for_move"""
    
    def test_distance_white_player(self):
        """Jugador blanco mueve de mayor a menor índice"""
        self.assertEqual(distance_for_move(20, 15, "B"), 5)
    
    def test_distance_black_player(self):
        """Jugador negro mueve de menor a mayor índice"""
        self.assertEqual(distance_for_move(5, 10, "N"), 5)
    
    def test_distance_zero(self):
        """Distancia cero cuando src == dst"""
        self.assertEqual(distance_for_move(10, 10, "B"), 0)
    
    def test_distance_negative_white(self):
        """Distancia negativa cuando blanco mueve en dirección incorrecta"""
        self.assertEqual(distance_for_move(10, 15, "B"), -5)

class TestConsumeDie(unittest.TestCase):
    """Tests para la función consume_die"""
    
    def test_consume_existing_die(self):
        """Consume un dado que existe en la lista"""
        dice = [3, 5, 6]
        result = consume_die(dice, 5)
        self.assertTrue(result)
        self.assertEqual(dice, [3, 6])
    
    def test_consume_first_occurrence(self):
        """Consume la primera ocurrencia de un dado duplicado"""
        dice = [2, 4, 2]
        result = consume_die(dice, 2)
        self.assertTrue(result)
        self.assertEqual(dice, [4, 2])
    
    def test_consume_nonexistent_die(self):
        """No consume si el dado no existe"""
        dice = [1, 2, 3]
        result = consume_die(dice, 5)
        self.assertFalse(result)
        self.assertEqual(dice, [1, 2, 3])
    
    def test_consume_from_empty_list(self):
        """No consume de lista vacía"""
        dice = []
        result = consume_die(dice, 3)
        self.assertFalse(result)
        self.assertEqual(dice, [])

class TestDoHitIfSingle(unittest.TestCase):
    """Tests para la función do_hit_if_single"""
    
    def test_hit_single_opponent_checker(self):
        """Golpea una ficha única del oponente"""
        mock_board = Mock()
        mock_board.point_owner_count.return_value = ("N", 1)
        mock_points = {5: [Mock()]}
        mock_board.points.return_value = mock_points
        do_hit_if_single(mock_board, 5, "B")
        self.assertEqual(len(mock_points[5]), 0)
    
    def test_no_hit_two_opponent_checkers(self):
        """No golpea cuando hay 2+ fichas del oponente"""
        mock_board = Mock()
        mock_board.point_owner_count.return_value = ("N", 2)
        mock_points = {5: [Mock(), Mock()]}
        mock_board.points.return_value = mock_points
        do_hit_if_single(mock_board, 5, "B")
        self.assertEqual(len(mock_points[5]), 2)
    
    def test_no_hit_empty_point(self):
        """No golpea en punto vacío"""
        mock_board = Mock()
        mock_board.point_owner_count.return_value = (None, 0)
        mock_points = {5: []}
        mock_board.points.return_value = mock_points
        do_hit_if_single(mock_board, 5, "B")
        self.assertEqual(len(mock_points[5]), 0)
    
    def test_no_hit_own_checker(self):
        """No golpea fichas propias"""
        mock_board = Mock()
        mock_board.point_owner_count.return_value = ("B", 1)
        mock_points = {5: [Mock()]}
        mock_board.points.return_value = mock_points
        do_hit_if_single(mock_board, 5, "B")
        self.assertEqual(len(mock_points[5]), 1)

class TestLegalMovesFrom(unittest.TestCase):
    """Tests para la función legal_moves_from"""
    def test_legal_moves_white_player(self):
        """Movimientos legales para jugador blanco"""
        mock_board = Mock()
        mock_board.point_owner_count.side_effect = [
            (None, 0),  # punto 18 vacío
            ("B", 2),   # punto 17 con fichas blancas
        ] 
        moves = legal_moves_from(mock_board, 20, "B", [2, 3])
        self.assertEqual(len(moves), 2)
        self.assertIn((18, 2), moves)
        self.assertIn((17, 3), moves)
    
    def test_legal_moves_black_player(self):
        """Movimientos legales para jugador negro"""
        mock_board = Mock()
        mock_board.point_owner_count.side_effect = [
            (None, 0),  # punto 7 vacío
            ("N", 1),   # punto 8 con ficha negra
        ]
        moves = legal_moves_from(mock_board, 5, "N", [2, 3])
        self.assertEqual(len(moves), 2)
        self.assertIn((7, 2), moves)
        self.assertIn((8, 3), moves)
    
    def test_blocked_by_opponent(self):
        """Movimientos bloqueados por oponente con 2+ fichas"""
        mock_board = Mock()
        mock_board.point_owner_count.return_value = ("N", 2)
        moves = legal_moves_from(mock_board, 20, "B", [2])
        self.assertEqual(len(moves), 0)
    
    def test_out_of_bounds_move(self):
        """Movimientos fuera del tablero no son válidos"""
        mock_board = Mock()
        moves = legal_moves_from(mock_board, 1, "B", [5, 6])
        self.assertEqual(len(moves), 0)
    
    def test_duplicate_dice_values(self):
        """Dados duplicados (dobles) - solo retorna una opción"""
        mock_board = Mock()
        mock_board.point_owner_count.return_value = (None, 0)
        moves = legal_moves_from(mock_board, 10, "B", [3, 3, 3, 3])
        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0], (7, 3))

class TestRenderBoardAscii(unittest.TestCase):
    """Tests para la función render_board_ascii"""
    def test_render_basic_board(self):
        """Renderiza tablero básico con dados"""
        mock_game = Mock()
        mock_board = Mock()
        mock_player = Mock()
        mock_player.nombre.return_value = "Jugador1"
        mock_game.board.return_value = mock_board
        mock_game.turno.return_value = "B"
        mock_game.players.return_value = {"B": mock_player, "N": Mock()}
        mock_game.dice.return_value = [3, 5]
        mock_board.point_owner_count.return_value = (None, 0)
        result = render_board_ascii(mock_game)
        self.assertIn("Turno: B", result)
        self.assertIn("Jugador1", result)
        self.assertIn("Dados: 3 5", result)
        self.assertIn("Comandos:", result)
    
    def test_render_without_dice(self):
        """Renderiza tablero sin dados tirados"""
        mock_game = Mock()
        mock_board = Mock()
        mock_player = Mock()
        mock_player.nombre.return_value = "Jugador2"
        mock_game.board.return_value = mock_board
        mock_game.turno.return_value = "N"
        mock_game.players.return_value = {"B": Mock(), "N": mock_player}
        mock_game.dice.return_value = None
        mock_board.point_owner_count.return_value = (None, 0)
        result = render_board_ascii(mock_game)
        self.assertIn("(sin tirar)", result)
    
    def test_render_with_checkers(self):
        """Renderiza tablero con fichas"""
        mock_game = Mock()
        mock_board = Mock()
        mock_player = Mock(spec=[])  # Sin el método nombre
        mock_game.board.return_value = mock_board
        mock_game.turno.return_value = "B"
        mock_game.players.return_value = {"B": mock_player, "N": Mock()}
        mock_game.dice.return_value = [2]
        
        def point_owner_side_effect(idx):
            if idx == 0:
                return ("B", 3)
            elif idx == 23:
                return ("N", 2)
            return (None, 0)
        mock_board.point_owner_count.side_effect = point_owner_side_effect
        result = render_board_ascii(mock_game)
        self.assertIn("B3", result)
        self.assertIn("N2", result)
        self.assertIn("Blancas", result)

class TestPrintHelp(unittest.TestCase):
    """Tests para la función print_help"""
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_help_output(self, mock_stdout):
        """Verifica que print_help imprime todos los comandos"""
        print_help()
        output = mock_stdout.getvalue()
        self.assertIn("Comandos:", output)
        self.assertIn("show", output)
        self.assertIn("roll", output)
        self.assertIn("move", output)
        self.assertIn("legal", output)
        self.assertIn("history", output)
        self.assertIn("quit", output)

class TestPromptNombres(unittest.TestCase):
    """Tests para la función prompt_nombres"""
    @patch('builtins.input', side_effect=["Alice", "Bob"])
    def test_prompt_with_names(self, mock_input):
        """Prompt con nombres ingresados"""
        p1, p2 = prompt_nombres()
        self.assertEqual(p1, "Alice")
        self.assertEqual(p2, "Bob")
    @patch('builtins.input', side_effect=["", ""])
    def test_prompt_with_empty_names(self, mock_input):
        """Prompt con nombres vacíos usa defaults"""
        p1, p2 = prompt_nombres()
        self.assertEqual(p1, "Blancas")
        self.assertEqual(p2, "Negras")
    @patch('builtins.input', side_effect=["  Alice  ", "  Bob  "])
    def test_prompt_with_spaces(self, mock_input):
        """Prompt hace strip de espacios"""
        p1, p2 = prompt_nombres()
        self.assertEqual(p1, "Alice")
        self.assertEqual(p2, "Bob")
    @patch('builtins.input', side_effect=EOFError())
    def test_prompt_eoferror_first(self, mock_input):
        """EOFError en primer prompt usa defaults"""
        p1, p2 = prompt_nombres()
        self.assertEqual(p1, "Blancas")
        self.assertEqual(p2, "Negras")
    @patch('builtins.input', side_effect=["Alice", EOFError()])
    def test_prompt_eoferror_second(self, mock_input):
        """EOFError en segundo prompt usa default para segundo"""
        p1, p2 = prompt_nombres()
        self.assertEqual(p1, "Alice")
        self.assertEqual(p2, "Negras")
    @patch('builtins.input', side_effect=KeyboardInterrupt())
    def test_prompt_keyboard_interrupt(self, mock_input):
        """KeyboardInterrupt usa defaults"""
        p1, p2 = prompt_nombres()
        self.assertEqual(p1, "Blancas")
        self.assertEqual(p2, "Negras")

class TestMain(unittest.TestCase):
    """Tests para la función main"""
    def setUp(self):
        """Limpiar historial antes de cada test"""
        import cli.CLI as CLI_module
        CLI_module.HISTORY.clear()
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_quit_command(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando quit termina el juego"""
        mock_game, mock_board = setup_mock_game()
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("¡Chau!", output)
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["exit"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_exit_command(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando exit termina el juego"""
        mock_game, mock_board = setup_mock_game()
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("¡Chau!", output)
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["h", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_help_command(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando help muestra ayuda"""
        mock_game, mock_board = setup_mock_game()
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Comandos:", output)
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["s", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_show_command(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando show muestra tablero"""
        mock_game, mock_board = setup_mock_game()
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Turno:", output)
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["r", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_roll_command(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando roll tira los dados"""
        mock_game, mock_board = setup_mock_game()
        mock_game.dice.return_value = [3, 5]
        mock_game.roll.return_value = [3, 5]
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Tiraste:", output)
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["history", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_history_empty(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando history con historial vacío"""
        mock_game, mock_board = setup_mock_game()
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("vacío", output)
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["r", "history", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_history_with_entries(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando history con entradas"""
        mock_game, mock_board = setup_mock_game()
        mock_game.dice.return_value = [2, 4]
        mock_game.roll.return_value = [2, 4]
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("1.", output)
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["legal", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_legal_no_args(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando legal sin argumentos muestra error"""
        mock_game, mock_board = setup_mock_game()
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Uso: legal", output)
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["legal abc", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_legal_invalid_arg(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando legal con argumento no numérico"""
        mock_game, mock_board = setup_mock_game()
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Uso: legal", output)
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["legal 30", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_legal_out_of_range(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando legal con índice fuera de rango"""
        mock_game, mock_board = setup_mock_game()
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("debe estar entre", output)
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["r", "legal 1", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_legal_empty_point(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando legal en punto vacío"""
        mock_game, mock_board = setup_mock_game()
        mock_game.dice.return_value = [3]
        mock_game.roll.return_value = [3]
        mock_board.points.return_value = {i: [] for i in range(24)}
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("No hay fichas", output)
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["r", "legal 1", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_legal_wrong_color(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando legal con ficha del color equivocado"""
        mock_game, mock_board = setup_mock_game()
        mock_checker = Mock()
        mock_checker.color.return_value = "N"
        mock_game.dice.return_value = [3]
        mock_game.roll.return_value = [3]
        mock_board.points.return_value = {0: [mock_checker], **{i: [] for i in range(1, 24)}}
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("no es tuya", output)
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["legal 1", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_legal_no_dice(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando legal sin dados tirados"""
        mock_game, mock_board = setup_mock_game()
        mock_checker = Mock()
        mock_checker.color.return_value = "B"
        mock_board.points.return_value = {0: [mock_checker], **{i: [] for i in range(1, 24)}}
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Primero tirá los dados", output)
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["r", "legal 24", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_legal_no_valid_moves(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando legal sin movimientos válidos"""
        mock_game, mock_board = setup_mock_game()
        mock_checker = Mock()
        mock_checker.color.return_value = "B"
        mock_game.dice.return_value = [1]
        mock_game.roll.return_value = [1]
        mock_board.points.return_value = {23: [mock_checker], **{i: [] for i in range(23)}}
        mock_board.point_owner_count.return_value = ("N", 2)
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("No hay destinos", output)
    
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["r", "legal 24", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_legal_with_valid_moves(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando legal con movimientos válidos"""
        mock_game, mock_board = setup_mock_game()
        mock_checker = Mock()
        mock_checker.color.return_value = "B"
        mock_game.dice.return_value = [2, 3]
        mock_game.roll.return_value = [2, 3]
        mock_board.points.return_value = {23: [mock_checker], **{i: [] for i in range(23)}}
        mock_board.point_owner_count.return_value = (None, 0)
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Opciones desde 24:", output)
    
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["move", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_move_no_args(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando move sin argumentos"""
        mock_game, mock_board = setup_mock_game()
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Uso: move", output)
    
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["move 1", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_move_one_arg(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando move con un solo argumento"""
        mock_game, mock_board = setup_mock_game()
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Uso: move", output)
    
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["move abc def", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_move_invalid_args(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando move con argumentos no numéricos"""
        mock_game, mock_board = setup_mock_game()
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Uso: move", output)
    
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["move 1 2", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_move_no_dice(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando move sin dados tirados"""
        mock_game, mock_board = setup_mock_game()
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Primero tirá los dados", output)
    
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["r", "move 30 25", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_move_out_of_range(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando move fuera de rango"""
        mock_game, mock_board = setup_mock_game()
        mock_game.dice.return_value = [5]
        mock_game.roll.return_value = [5]
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("debe estar entre", output)
    
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["r", "move 1 2", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_move_empty_point(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando move desde punto vacío"""
        mock_game, mock_board = setup_mock_game()
        mock_game.dice.return_value = [1]
        mock_game.roll.return_value = [1]
        mock_board.points.return_value = {i: [] for i in range(24)}
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("No hay fichas", output)
    
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["r", "move 1 2", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_move_wrong_color(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando move con ficha del color equivocado"""
        mock_game, mock_board = setup_mock_game()
        mock_checker = Mock()
        mock_checker.color.return_value = "N"
        mock_game.dice.return_value = [1]
        mock_game.roll.return_value = [1]
        mock_board.points.return_value = {0: [mock_checker], **{i: [] for i in range(1, 24)}}
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("no es tuya", output)
    
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["r", "move 10 12", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_move_invalid_direction(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando move con dirección inválida"""
        mock_game, mock_board = setup_mock_game()
        mock_checker = Mock()
        mock_checker.color.return_value = "B"
        mock_game.dice.return_value = [2]
        mock_game.roll.return_value = [2]
        mock_board.points.return_value = {9: [mock_checker], **{i: [] for i in range(9)}, **{i: [] for i in range(10, 24)}}
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Dirección inválida", output)
    
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["r", "move 24 22", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_move_blocked_destination(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando move a destino bloqueado"""
        mock_game, mock_board = setup_mock_game()
        mock_checker = Mock()
        mock_checker.color.return_value = "B"
        mock_game.dice.return_value = [2]
        mock_game.roll.return_value = [2]
        mock_board.points.return_value = {23: [mock_checker], **{i: [] for i in range(23)}}
        def point_owner_side_effect(idx):
            if idx == 21:
                return ("N", 2)
            return (None, 0)
        mock_board.point_owner_count.side_effect = point_owner_side_effect
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("bloqueado", output)
    
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["r", "move 24 21", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_move_die_not_available(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando move con dado no disponible"""
        mock_game, mock_board = setup_mock_game()
        mock_checker = Mock()
        mock_checker.color.return_value = "B"
        mock_game.dice.return_value = [2]
        mock_game.roll.return_value = [2]
        mock_board.points.return_value = {23: [mock_checker], **{i: [] for i in range(23)}}
        mock_board.point_owner_count.return_value = (None, 0)
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("No tenés el valor", output)
    
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["r", "move 24 22", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_move_successful(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando move exitoso"""
        mock_game, mock_board = setup_mock_game()
        mock_checker = Mock()
        mock_checker.color.return_value = "B"
        mock_game.dice.return_value = [2]
        mock_game.roll.return_value = [2]
        points_dict = {23: [mock_checker], 21: [], **{i: [] for i in range(21)}, 22: []}
        mock_board.points.return_value = points_dict
        mock_board.point_owner_count.return_value = (None, 0)
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Movida OK", output)
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["r", "move 24 22", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_move_with_hit(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando move con golpe a ficha única"""
        mock_game, mock_board = setup_mock_game()
        mock_checker_b = Mock()
        mock_checker_b.color.return_value = "B"
        mock_checker_n = Mock()
        mock_checker_n.color.return_value = "N"
        mock_game.dice.return_value = [2]
        mock_game.roll.return_value = [2]
        points_dict = {23: [mock_checker_b], 21: [mock_checker_n], **{i: [] for i in range(21)}, 22: []}
        mock_board.points.return_value = points_dict
        def point_owner_side_effect(idx):
            if idx == 21 and len(points_dict[21]) > 0:
                return ("N", 1)
            return (None, 0)
        mock_board.point_owner_count.side_effect = point_owner_side_effect
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Movida OK", output)
        # Verificar que la ficha se movió y se hizo el hit
        self.assertEqual(len(points_dict[23]), 0)
        self.assertEqual(len(points_dict[21]), 1)
        self.assertEqual(points_dict[21][0].color(), "B")
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["e", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_end_turn_command(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando end termina el turno"""
        mock_game, mock_board = setup_mock_game()
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Turno terminado", output)
        mock_game.end_turn.assert_called_once()
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["unknown_command", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_unknown_command(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando no reconocido"""
        mock_game, mock_board = setup_mock_game()
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("no reconocido", output)
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=["", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_empty_command(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """Comando vacío se ignora"""
        mock_game, mock_board = setup_mock_game()
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        lines = output.split("¡Chau!")[0].split("Turno:")
        if len(lines) > 1:
            last_section = lines[-1]
            self.assertNotIn("no reconocido", last_section)
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=EOFError())
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_eoferror(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """EOFError durante el juego"""
        mock_game, mock_board = setup_mock_game()
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("¡Chau!", output)
    @patch('cli.CLI.prompt_nombres', return_value=("P1", "P2"))
    @patch('cli.CLI.BackgammonGame')
    @patch('builtins.input', side_effect=KeyboardInterrupt())
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_keyboard_interrupt(self, mock_stdout, mock_input, mock_game_class, mock_prompt):
        """KeyboardInterrupt durante el juego"""
        mock_game, mock_board = setup_mock_game()
        mock_game_class.return_value = mock_game
        main()
        output = mock_stdout.getvalue()
        self.assertIn("¡Chau!", output)

class TestOwnerIcon(unittest.TestCase):
    """Tests para la constante OWNER_ICON"""
    def test_owner_icon_values(self):
        """Verifica valores correctos en OWNER_ICON"""
        self.assertEqual(OWNER_ICON["B"], "B")
        self.assertEqual(OWNER_ICON["N"], "N")
        self.assertEqual(OWNER_ICON[None], ".")

if __name__ == '__main__':
    unittest.main(verbosity=2)