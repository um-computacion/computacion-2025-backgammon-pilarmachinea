import unittest
from core.Dice import Dice


class TestDice(unittest.TestCase):    
    def test_crear_dice(self):
        dice = Dice()
        self.assertIsNotNone(dice)
        self.assertEqual(dice.last(), [])
    
    def test_roll_retorna_lista(self):
        dice = Dice()
        resultado = dice.roll()
        self.assertIsInstance(resultado, list)
    
    def test_roll_valores_validos(self):
        dice = Dice()
        for _ in range(50):
            resultado = dice.roll()
            for valor in resultado:
                self.assertGreaterEqual(valor, 1)
                self.assertLessEqual(valor, 6)
    
    def test_roll_dos_valores_diferentes(self):
        dice = Dice()
        dados_diferentes = False
        for _ in range(50):
            resultado = dice.roll()
            if len(resultado) == 2 and resultado[0] != resultado[1]:
                dados_diferentes = True
                break
        self.assertTrue(dados_diferentes)
    
    def test_roll_dobles_cuatro_valores(self):
        dice = Dice()
        encontro_dobles = False
        for _ in range(100):
            resultado = dice.roll()
            if len(resultado) == 4:
                self.assertEqual(resultado[0], resultado[1])
                self.assertEqual(resultado[1], resultado[2])
                self.assertEqual(resultado[2], resultado[3])
                encontro_dobles = True
                break
        self.assertTrue(encontro_dobles)
    
    def test_last_retorna_ultima_tirada(self):
        dice = Dice()
        resultado_roll = dice.roll()
        resultado_last = dice.last()
        self.assertEqual(resultado_roll, resultado_last)
    
    def test_last_no_modifica_original(self):
        dice = Dice()
        dice.roll()
        resultado1 = dice.last()
        resultado1.append(99)
        resultado2 = dice.last()
        self.assertNotIn(99, resultado2)
    
    def test_multiples_rolls_independientes(self):
        dice = Dice()
        resultados = []
        for _ in range(10):
            resultados.append(tuple(dice.roll()))
        
        # Verificar que hay variación (improbable que sean todos iguales)
        self.assertGreater(len(set(resultados)), 1)
    
    def test_last_actualiza_con_nuevo_roll(self):
        dice = Dice()
        dice.roll()
        primer_last = dice.last()
        dice.roll()
        segundo_last = dice.last()
        self.assertIsInstance(segundo_last, list)


if __name__ == '__main__':
    unittest.main()
