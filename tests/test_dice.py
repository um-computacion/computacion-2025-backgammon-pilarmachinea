import unittest
from unittest.mock import patch
from core.Dice import Dice


class TestDice(unittest.TestCase):
    def test_last_inicia_vacio(self):
        d = Dice()
        self.assertEqual(d.last(), [])

    def test_roll_no_dobles(self):
        d = Dice()
        seq = [3, 5]

        with patch("core.Dice.random.randint", side_effect=seq):
            vals = d.roll()

        self.assertEqual(sorted(vals), [3, 5])
        # Aseguramos que last es una copia defensiva
        vals.append(99)
        self.assertEqual(d.last(), [3, 5])

    def test_roll_dobles(self):
        d = Dice()
        with patch("core.Dice.random.randint", return_value=4):
            vals = d.roll()
        self.assertEqual(vals, [4, 4, 4, 4])
        self.assertEqual(d.last(), [4, 4, 4, 4])

class TestDiceExtra(unittest.TestCase):
    def test_last_resetea_correcto_y_copia_defensiva(self):
        d = Dice()
        with patch("core.Dice.random.randint", side_effect=[2, 5]):
            v1 = d.roll()
        self.assertEqual(v1, [2, 5])
        self.assertEqual(d.last(), [2, 5])
        # Siguiente tirada cambia los valores
        with patch("core.Dice.random.randint", return_value=4):
            v2 = d.roll()  # dobles
        self.assertEqual(v2, [4, 4, 4, 4])
        self.assertEqual(d.last(), [4, 4, 4, 4])
        # Mutar el retorno no debe afectar el estado interno
        v2.append(99)
        self.assertEqual(d.last(), [4, 4, 4, 4])

if __name__ == "__main__":
    unittest.main()
