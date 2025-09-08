import unittest
from core.Dice import Dice

class TestDice(unittest.TestCase):
    def test_last_inicia_vacio(self):
        dice = Dice()
        self.assertEqual(dice.last(), [])

    def test_roll_devuelve_lista_de_2_o_4(self):
        dice = Dice()
        roll = dice.roll()
        self.assertIn(len(roll), [2, 4])

    def test_valores_entre_1_y_6(self):
        dice = Dice()
        roll = dice.roll()
        for value in roll:
            self.assertGreaterEqual(value, 1)
            self.assertLessEqual(value, 6)

    def test_last_coincide_con_ultimo_roll(self):
        dice = Dice()
        roll = dice.roll()
        self.assertEqual(dice.last(), roll)

    def test_last_es_una_copia(self):
        dice = Dice()
        roll = dice.roll()
        copia = dice.last()
        self.assertIsNot(copia, roll)
        copia.append(99)
        self.assertNotEqual(dice.last(), copia)

    def test_eventualmente_hay_un_doble(self):
        dice = Dice()
        encontrado = False
        for _ in range(300):
            roll = dice.roll()
            if len(roll) == 4:
                encontrado = True
                break
        self.assertTrue(encontrado)

if __name__ == "__main__":
    unittest.main()
