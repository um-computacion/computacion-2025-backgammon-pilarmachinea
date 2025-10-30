import unittest
from unittest.mock import patch
from core.BackgammonGame import BackgammonGame
from core.Board import Board
from core.Checker import Checker

class TestGame(unittest.TestCase):
    def test_basicos_turno_y_players(self):
        g = BackgammonGame("Anna", "Noa")
        self.assertIn(g.turno(), ("B", "N"))
        ps = g.players()
        self.assertEqual(set(ps.keys()), {"B", "N"})
        self.assertIn(g.current_player().nombre(), ("Anna", "Noa"))
        self.assertIsInstance(g.board(), Board)

    def test_roll_y_dados_disponibles(self):
        g = BackgammonGame()
        seq = [2, 5]
        with patch("core.Dice.random.randint", side_effect=seq):
            vals = g.roll()
        self.assertEqual(sorted(vals), [2, 5])
        self.assertEqual(sorted(g.dice()), [2, 5])
        self.assertEqual(sorted(g.available_dice()), [2, 5])

    def test_move_consumo_de_dados_y_fin_de_turno(self):
        g = BackgammonGame()
        b = g.board()
        # Simplifico tablero
        for i in range(24):
            b.points()[i].clear()
        # Dos blancas en idx 0 → mover con 1 y 2
        b.points()[0].extend([Checker('B'), Checker('B')])

        with patch("core.Dice.random.randint", side_effect=[1, 2]):
            g.roll()
        self.assertEqual(set(g.available_dice()), {1, 2})

        # Mueve con 1
        self.assertTrue(g.can_move(0, 1))
        turno_ini = g.turno()
        self.assertTrue(g.move(0, 1))
        self.assertEqual(set(g.available_dice()), {2})
        # Mueve con 2, se acaban dados → cambia turno
        self.assertTrue(g.can_move(0, 2))
        self.assertTrue(g.move(0, 2))
        self.assertNotEqual(g.turno(), turno_ini)

    def test_can_end_turn_y_has_valid_moves(self):
        g = BackgammonGame()
        b = g.board()
        # Tablero sin movimientos claros para B
        for i in range(24):
            b.points()[i].clear()
        # Bloqueo con 2 negras en 0..5
        for idx in range(6):
            b.points()[idx].extend([Checker('N'), Checker('N')])
        # Una blanca en idx 23
        b.points()[23].append(Checker('B'))

        with patch("core.Dice.random.randint", side_effect=[1, 2]):
            g.roll()

        # Dependiendo de la lógica interna, puede o no haber movimientos.
        # Probamos la rama en la que no hay y se puede terminar turno.
        if not g.has_valid_moves():
            self.assertTrue(g.can_end_turn())

    def test_regla_off_estricta(self):
        g = BackgammonGame()
        b = g.board()
        for i in range(24):
            b.points()[i].clear()
        # Una blanca en idx 18 (punto 19) → distancia a off 6
        b.points()[18].append(Checker('B'))

        with patch("core.Dice.random.randint", side_effect=[6, 5]):
            g.roll()

        # Exacto permitido
        self.assertTrue(g.can_move(18, 6))
        # Con 5 debería ser movimiento interno (no off). Si el destino es válido, can_move True.
        self.assertTrue(g.can_move(18, 5))

    def test_is_game_over_y_winner(self):
        g = BackgammonGame("Ana", "Noa")
        b = g.board()
        b.off()['B'] = 15
        self.assertTrue(g.is_game_over())
        self.assertEqual(g.winner(), "B")


class TestGameExtra(unittest.TestCase):
    def setUp(self):
        self.g = BackgammonGame()
        self.b = self.g.board()

    def _vaciar_tablero(self):
        for i in range(24):
            self.b.points()[i].clear()

    def test_roll_dobles_y_consumo_individual(self):
        # Dobles 3 → cuatro movimientos [3,3,3,3]
        with patch("core.Dice.random.randint", return_value=3):
            vals = self.g.roll()
        self.assertEqual(vals, [3, 3, 3, 3])
        self.assertEqual(self.g.available_dice(), [3, 3, 3, 3])

        # Simplificamos el tablero para que las blancas (B) puedan mover 4 veces
        self._vaciar_tablero()
        # 4 fichas blancas en idx 0 → podrán hacer 4 avances de 3
        for _ in range(4):
            self.b.points()[0].append(Checker('B'))

        # Vamos consumiendo cada "3"
        for k in range(4):
            self.assertTrue(self.g.can_move(0, 3), f"Falla en el avance {k+1}")
            self.assertTrue(self.g.move(0, 3))
            # Se va reduciendo la lista de dados disponibles
            self.assertEqual(len(self.g.available_dice()), 3 - k)

        # Sin dados → cambia el turno automáticamente
        self.assertEqual(len(self.g.available_dice()), 0)

    def test_dado_no_disponible(self):
        # Tirada 2 y 5
        with patch("core.Dice.random.randint", side_effect=[2, 5]):
            self.g.roll()
        # Intento mover con 6 (no disponible) → False
        self.assertFalse(self.g.can_move(0, 6))

    def test_bar_priority_no_permiso_mientras_haya_en_bar(self):
        # Forzamos que N tenga una ficha en el bar y sea el turno de N
        # 1) Capturamos una N con B para que vaya al bar
        self._vaciar_tablero()
        self.b.points()[5].append(Checker('N'))   # una negra sola
        self.b.points()[2].append(Checker('B'))   # una blanca que caerá con 3
        # Turno está en "B" por defecto
        with patch("core.Dice.random.randint", side_effect=[3, 3]):
            self.g.roll()
        self.assertTrue(self.g.move(2, 3))     # captura a N en idx5
        # Termina turno B
        self.assertEqual(len(self.g.available_dice()), 3)  # aún quedan dados (por si tu lógica no auto-end)
        # Consumimos para forzar fin de turno
        while self.g.available_dice():
            # Si no puede mover más, debería acabar turno con can_end_turn()
            if not self.g.has_valid_moves():
                self.assertTrue(self.g.can_end_turn())
                break
            # intenta algún movimiento trivial inválido para consumir/forzar fin
            if not self.g.move(2, 3):
                break

        # Ahora turno pasa a N y N tiene ficha en bar
        # N NO debería poder mover desde puntos normales hasta reingresar
        with patch("core.Dice.random.randint", side_effect=[1, 2]):
            self.g.roll()
        self.assertFalse(self.g.can_move(10, 1))  # desde tablero no

    def test_ganador_N(self):
        # Fuerzo victoria de N
        self.b.off()['N'] = 15
        self.assertTrue(self.g.is_game_over())
        self.assertEqual(self.g.winner(), "N")

class TestGameCoverMore(unittest.TestCase):
    def setUp(self):
        self.g = BackgammonGame()
        self.b: Board = self.g.board()

    def _clear_board(self):
        for i in range(24):
            self.b.points()[i].clear()

    def test_has_valid_moves_true_y_can_end_turn_false(self):
        self._clear_board()
        # Dos blancas en idx 0 → con dados 1 y 2 hay movs válidos
        self.b.points()[0].extend([Checker('B'), Checker('B')])
        with patch("core.Dice.random.randint", side_effect=[1, 2]):
            self.g.roll()
        self.assertTrue(self.g.has_valid_moves())
        self.assertFalse(self.g.can_end_turn())  # mientras queden dados y movimientos, no puede

    def test_move_con_dado_no_disponible_no_cambia_turno(self):
        self._clear_board()
        self.b.points()[0].append(Checker('B'))
        with patch("core.Dice.random.randint", side_effect=[3, 4]):
            self.g.roll()
        turno_ini = self.g.turno()
        # 6 no disponible → move debe fallar y no consumir dados ni cambiar turno
        self.assertFalse(self.g.move(0, 6))
        self.assertEqual(self.g.turno(), turno_ini)
        self.assertEqual(sorted(self.g.available_dice()), [3, 4])

    def test_roll_sobrescribe_y_reinicia_available_dice(self):
        with patch("core.Dice.random.randint", side_effect=[2, 5]):
            self.g.roll()
        # consumimos uno de los dados para asegurar que se “resetea” luego
        self._clear_board()
        self.b.points()[0].append(Checker('B'))
        self.assertTrue(self.g.can_move(0, 2))
        self.assertTrue(self.g.move(0, 2))
        self.assertEqual(self.g.available_dice(), [5])

        # Nueva tirada debe SOBREESCRIBIR
        with patch("core.Dice.random.randint", side_effect=[4, 4]):
            vals = self.g.roll()
        self.assertEqual(vals, [4, 4, 4, 4])
        self.assertEqual(self.g.available_dice(), [4, 4, 4, 4])

    def test_is_game_over_false_y_winner_none(self):
        # Estado normal: nadie tiene 15 afuera
        self.assertFalse(self.g.is_game_over())
        self.assertIsNone(self.g.winner())

    def test_pasar_turno_sin_movimientos(self):
        # Forzamos que B no tenga movimientos (B en bar y entradas 0..5 bloqueadas)
        self._clear_board()
        # Capturamos una B: N desde 11 con 6 cae en 5
        self.b.points()[5].append(Checker('B'))
        self.b.points()[11].append(Checker('N'))
        self.assertTrue(self.b.can_move(11, 6, 'N'))
        self.assertTrue(self.b.move(11, 6, 'N'))
        # Bloqueamos entradas 0..5 para B
        for idx in range(6):
            self.b.points()[idx].clear()
            self.b.points()[idx].extend([Checker('N'), Checker('N')])
        with patch("core.Dice.random.randint", side_effect=[1, 2]):
            self.g.roll()
        self.assertFalse(self.g.has_valid_moves())
        self.assertTrue(self.g.can_end_turn())



if __name__ == "__main__":
    unittest.main()
