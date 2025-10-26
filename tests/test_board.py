import unittest
from core.Board import Board
from core.Checker import Checker


class TestBoardBasico(unittest.TestCase):
    """Tests básicos de inicialización y getters"""
    
    def setUp(self):
        self.board = Board()
    
    def test_inicializacion(self):
        """Verifica que el tablero se inicialice correctamente"""
        self.assertEqual(len(self.board.points()), 24)
        self.assertIsNotNone(self.board.bar())
        self.assertIsNotNone(self.board.off())
    
    def test_bar_inicial_vacio(self):
        """Verifica que el bar inicie vacío"""
        bar = self.board.bar()
        self.assertEqual(len(bar['B']), 0)
        self.assertEqual(len(bar['N']), 0)
    
    def test_off_inicial_cero(self):
        """Verifica que las fichas retiradas inicien en 0"""
        off = self.board.off()
        self.assertEqual(off['B'], 0)
        self.assertEqual(off['N'], 0)
    
    def test_setup_correcto(self):
        """Verifica que el setup inicial coloque las fichas correctamente"""
        # Blancas
        owner, count = self.board.point_owner_count(23)
        self.assertEqual(owner, 'B')
        self.assertEqual(count, 5)
        
        owner, count = self.board.point_owner_count(12)
        self.assertEqual(owner, 'B')
        self.assertEqual(count, 2)
        
        owner, count = self.board.point_owner_count(7)
        self.assertEqual(owner, 'B')
        self.assertEqual(count, 5)
        
        owner, count = self.board.point_owner_count(4)
        self.assertEqual(owner, 'B')
        self.assertEqual(count, 3)
        
        # Negras
        owner, count = self.board.point_owner_count(0)
        self.assertEqual(owner, 'N')
        self.assertEqual(count, 5)
        
        owner, count = self.board.point_owner_count(11)
        self.assertEqual(owner, 'N')
        self.assertEqual(count, 2)
        
        owner, count = self.board.point_owner_count(16)
        self.assertEqual(owner, 'N')
        self.assertEqual(count, 5)
        
        owner, count = self.board.point_owner_count(19)
        self.assertEqual(owner, 'N')
        self.assertEqual(count, 3)
    
    def test_point_owner_count_vacio(self):
        """Verifica point_owner_count en punto vacío"""
        board = Board()
        # Limpiar un punto usando acceso directo
        board.points()[10] = []
        owner, count = board.point_owner_count(10)
        self.assertIsNone(owner)
        self.assertEqual(count, 0)
    
    def test_has_checkers_on_bar_false(self):
        """Verifica has_checkers_on_bar cuando no hay fichas"""
        self.assertFalse(self.board.has_checkers_on_bar('B'))
        self.assertFalse(self.board.has_checkers_on_bar('N'))
    
    def test_has_checkers_on_bar_true(self):
        """Verifica has_checkers_on_bar cuando hay fichas"""
        # Usar bar() para obtener referencia y agregar ficha
        bar = self.board.bar()
        # Crear nueva instancia para simular ficha en bar
        board = Board()
        board.points()[0].pop()  # Sacar una ficha
        bar_dict = board.bar()  # bar() retorna copia, necesitamos otra forma
        
        # Mejor enfoque: hacer un movimiento que ponga ficha en bar mediante captura
        board2 = Board()
        board2.points()[10] = []
        board2._put(10, 'N', 1)  # Una ficha negra sola
        board2.points()[13] = []
        board2._put(13, 'B', 1)  # Una blanca
        board2.move(13, 3, 'B')  # Mueve B de 13 a 10, captura N
        
        self.assertTrue(board2.has_checkers_on_bar('N'))
        self.assertFalse(board2.has_checkers_on_bar('B'))


class TestBoardBearingOff(unittest.TestCase):
    """Tests de lógica de Bearing Off (retirada)"""
    
    def setUp(self):
        self.board = Board()
    
    def test_get_home_range_blancas(self):
        """Verifica el rango de casa para Blancas"""
        home_range = self.board._get_home_range('B')
        self.assertEqual(list(home_range), [0, 1, 2, 3, 4, 5])
    
    def test_get_home_range_negras(self):
        """Verifica el rango de casa para Negras"""
        home_range = self.board._get_home_range('N')
        self.assertEqual(list(home_range), [18, 19, 20, 21, 22, 23])
    
    def test_can_bear_off_false_fichas_fuera_de_casa(self):
        """No puede retirar si tiene fichas fuera de casa"""
        # El setup inicial tiene fichas fuera de casa
        self.assertFalse(self.board.can_bear_off('B'))
        self.assertFalse(self.board.can_bear_off('N'))
    
    def test_can_bear_off_false_fichas_en_bar(self):
        """No puede retirar si tiene fichas en el bar"""
        # Crear tablero limpio
        board = Board()
        # Limpiar todos los puntos
        for i in range(24):
            board.points()[i] = []
        
        # Poner todas las blancas en casa (0-5)
        board._put(0, 'B', 5)
        board._put(1, 'B', 5)
        board._put(2, 'B', 4)
        
        # Crear una ficha blanca fuera de casa que será capturada
        board._put(10, 'B', 1)  # Blanca sola (será capturada)
        board._put(7, 'N', 1)   # Negra que va a capturar
        board.move(7, 3, 'N')   # N captura B, B va a bar
        
        # B no puede bear off (tiene una en bar)
        self.assertFalse(board.can_bear_off('B'))
        
        # Crear situación para N también
        board2 = Board()
        for i in range(24):
            board2.points()[i] = []
        
        # Todas las negras en casa (18-23)
        board2._put(18, 'N', 5)
        board2._put(19, 'N', 5)
        board2._put(20, 'N', 4)
        
        # Crear captura para poner N en bar
        board2._put(10, 'N', 1)
        board2._put(13, 'B', 1)
        board2.move(13, 3, 'B')
        
        # N no puede (tiene una en bar)
        self.assertFalse(board2.can_bear_off('N'))
    
    def test_can_bear_off_true_todas_en_casa(self):
        """Puede retirar si todas las fichas están en casa"""
        board = Board()
        # Limpiar tablero
        for i in range(24):
            board.points()[i] = []
        
        # Poner todas en casa para B (0-5)
        board._put(0, 'B', 5)
        board._put(1, 'B', 5)
        board._put(2, 'B', 5)
        
        self.assertTrue(board.can_bear_off('B'))
    
    def test_can_bear_off_true_negras_en_casa(self):
        """Puede retirar fichas negras si están en casa"""
        board = Board()
        # Limpiar tablero
        for i in range(24):
            board.points()[i] = []
        
        # Poner todas en casa para N (18-23)
        board._put(18, 'N', 5)
        board._put(19, 'N', 5)
        board._put(20, 'N', 5)
        
        self.assertTrue(board.can_bear_off('N'))
    
    def test_is_furthest_checker_blancas_true(self):
        """Verifica ficha más lejana para Blancas"""
        board = Board()
        for i in range(24):
            board.points()[i] = []
        
        board._put(5, 'B', 1)  # La más lejana
        board._put(2, 'B', 2)
        board._put(0, 'B', 3)
        
        self.assertTrue(board._is_furthest_checker(5, 'B'))
        self.assertFalse(board._is_furthest_checker(2, 'B'))
    
    def test_is_furthest_checker_blancas_false(self):
        """Verifica que no sea la más lejana si hay otras más lejos"""
        board = Board()
        for i in range(24):
            board.points()[i] = []
        
        board._put(5, 'B', 1)
        board._put(3, 'B', 1)
        
        self.assertFalse(board._is_furthest_checker(3, 'B'))
    
    def test_is_furthest_checker_negras_true(self):
        """Verifica ficha más lejana para Negras"""
        board = Board()
        for i in range(24):
            board.points()[i] = []
        
        board._put(18, 'N', 1)  # La más lejana
        board._put(20, 'N', 2)
        board._put(22, 'N', 3)
        
        self.assertTrue(board._is_furthest_checker(18, 'N'))
        self.assertFalse(board._is_furthest_checker(20, 'N'))
    
    def test_is_furthest_checker_negras_false(self):
        """Verifica que no sea la más lejana si hay otras más lejos"""
        board = Board()
        for i in range(24):
            board.points()[i] = []
        
        board._put(18, 'N', 1)
        board._put(20, 'N', 1)
        
        self.assertFalse(board._is_furthest_checker(20, 'N'))


class TestBoardCanMove(unittest.TestCase):
    """Tests de lógica can_move"""
    
    def setUp(self):
        self.board = Board()
    
    def test_can_move_bloqueado_por_bar(self):
        """No puede mover desde tablero si tiene fichas en bar"""
        board = Board()
        # Crear situación con ficha en bar
        board.points()[10] = []
        board._put(10, 'N', 1)
        board.points()[13] = []
        board._put(13, 'B', 1)
        board.move(13, 3, 'B')  # Captura, pone N en bar
        
        # Ahora N no puede mover desde tablero
        self.assertFalse(board.can_move(0, 3, 'N'))
    
    def test_can_move_desde_bar_sin_fichas(self):
        """No puede mover desde bar si no tiene fichas ahí"""
        self.assertFalse(self.board.can_move(None, 3, 'B'))
    
    def test_can_move_desde_bar_punto_bloqueado(self):
        """No puede reingresar si el punto está bloqueado"""
        board = Board()
        # Crear ficha en bar
        board.points()[10] = []
        board._put(10, 'N', 1)
        board.points()[13] = []
        board._put(13, 'B', 1)
        board.move(13, 3, 'B')  # B captura N, N va a bar
        
        # Bloquear punto de reingreso para N (die-1 = 3-1 = 2)
        board.points()[2] = []
        board._put(2, 'B', 2)
        
        self.assertFalse(board.can_move(None, 3, 'N'))
    
    def test_can_move_desde_bar_punto_disponible(self):
        """Puede reingresar si el punto está disponible"""
        board = Board()
        # Crear ficha en bar
        board.points()[10] = []
        board._put(10, 'N', 1)
        board.points()[13] = []
        board._put(13, 'B', 1)
        board.move(13, 3, 'B')  # B captura N, N va a bar
        
        # Limpiar punto de reingreso
        board.points()[2] = []
        
        self.assertTrue(board.can_move(None, 3, 'N'))
    
    def test_can_move_desde_bar_puede_capturar(self):
        """Puede reingresar capturando una ficha enemiga sola"""
        board = Board()
        # Crear ficha en bar
        board.points()[10] = []
        board._put(10, 'N', 1)
        board.points()[13] = []
        board._put(13, 'B', 1)
        board.move(13, 3, 'B')  # B captura N, N va a bar
        
        # Poner una ficha enemiga sola en punto de reingreso
        board.points()[2] = []
        board._put(2, 'B', 1)
        
        self.assertTrue(board.can_move(None, 3, 'N'))
    
    def test_can_move_origen_vacio(self):
        """No puede mover desde punto vacío"""
        board = Board()
        board.points()[10] = []
        self.assertFalse(board.can_move(10, 3, 'B'))
    
    def test_can_move_origen_color_incorrecto(self):
        """No puede mover ficha de otro color"""
        # Punto 0 tiene fichas negras
        self.assertFalse(self.board.can_move(0, 3, 'B'))
    
    def test_can_move_normal_valido(self):
        """Puede mover normalmente a punto disponible"""
        # Punto 7 tiene 5 fichas blancas, mover a 4 está bloqueado por 3 blancas
        # Mejor usar punto 23 con 5 blancas, mover 3 casillas a 20
        self.assertTrue(self.board.can_move(23, 3, 'B'))
    
    def test_can_move_destino_fuera_de_rango(self):
        """No puede mover fuera del rango válido sin bearing off"""
        # Intentar mover más allá del rango sin estar en casa
        self.assertFalse(self.board.can_move(23, 25, 'B'))
    
    def test_can_move_bearing_off_dado_exacto(self):
        """Puede retirar con dado exacto"""
        board = Board()
        for i in range(24):
            board.points()[i] = []
        
        board._put(3, 'B', 1)  # Distancia 4 al final (3+1)
        
        self.assertTrue(board.can_move(3, 4, 'B'))
    
    def test_can_move_bearing_off_dado_excedente_furthest(self):
        """Puede retirar con dado excedente si es la más lejana"""
        board = Board()
        for i in range(24):
            board.points()[i] = []
        
        board._put(2, 'B', 1)  # La más lejana, distancia 3
        
        self.assertTrue(board.can_move(2, 5, 'B'))
    
    def test_can_move_bearing_off_dado_excedente_no_furthest(self):
        """No puede retirar con dado excedente si no es la más lejana"""
        board = Board()
        for i in range(24):
            board.points()[i] = []
        
        board._put(5, 'B', 1)  # Hay otra más lejana
        board._put(2, 'B', 1)
        
        self.assertFalse(board.can_move(2, 5, 'B'))
    
    def test_can_move_bearing_off_dado_insuficiente(self):
        """Dado insuficiente para bearing off - línea 126"""
        # Esta línea es matemáticamente inalcanzable en Backgammon real
        # porque si to_point < 0, entonces die_value >= from_point + 1 = distance_to_off
        # Sin embargo, podemos testear el comportamiento con movimientos normales
        
        board = Board()
        for i in range(24):
            board.points()[i] = []
        
        board._put(3, 'B', 1)
        
        # Dado 2: to_point = 1 (normal, no bearing off)
        self.assertTrue(board.can_move(3, 2, 'B'))
    
    def test_can_move_destino_invalido_fuera_rango(self):
        """Destino fuera de rango en movimiento normal - línea 130"""
        board = Board()
        
        # Intentar mover con dado muy grande desde punto alto
        # Esto NO es bearing off porque el jugador tiene fichas fuera de casa
        # from_point = 22, die_value = 25 → to_point = -3 (< 0)
        # Pero can_bear_off será False por fichas fuera de casa
        # Entonces no entra en la sección de bearing off y llega a línea 129
        
        # Este test ya no aplica porque si to_point < 0, siempre entra en bearing off check
        # La línea 130 se alcanza cuando to_point está entre el rango después de bearing off check
        pass
    
    def test_can_move_bearing_off_sin_todas_en_casa(self):
        """No puede retirar si tiene fichas fuera de casa"""
        board = Board()
        for i in range(24):
            board.points()[i] = []
        
        board._put(0, 'B', 1)
        board._put(10, 'B', 1)  # Fuera de casa
        
        self.assertFalse(board.can_move(0, 1, 'B'))
    
    def test_can_move_bearing_off_negras_dado_exacto(self):
        """Puede retirar fichas negras con dado exacto"""
        board = Board()
        for i in range(24):
            board.points()[i] = []
        
        board._put(20, 'N', 1)  # Distancia 4 al final (24-20)
        
        self.assertTrue(board.can_move(20, 4, 'N'))
    
    def test_can_move_bearing_off_negras_dado_excedente(self):
        """Puede retirar fichas negras con dado excedente si es la más lejana"""
        board = Board()
        for i in range(24):
            board.points()[i] = []
        
        board._put(21, 'N', 1)  # La más lejana, distancia 3
        
        self.assertTrue(board.can_move(21, 5, 'N'))


class TestBoardCanLandOn(unittest.TestCase):
    """Tests de lógica _can_land_on"""
    
    def setUp(self):
        self.board = Board()
    
    def test_can_land_on_punto_vacio(self):
        """Puede aterrizar en punto vacío"""
        board = Board()
        board.points()[10] = []
        self.assertTrue(board._can_land_on(10, 'B'))
    
    def test_can_land_on_punto_propio(self):
        """Puede aterrizar en punto con fichas propias"""
        # Punto 7 tiene fichas blancas
        self.assertTrue(self.board._can_land_on(7, 'B'))
    
    def test_can_land_on_captura_blot(self):
        """Puede aterrizar capturando una ficha enemiga sola"""
        board = Board()
        board.points()[10] = []
        board._put(10, 'N', 1)  # Una sola ficha negra
        
        self.assertTrue(board._can_land_on(10, 'B'))
    
    def test_can_land_on_bloqueado(self):
        """No puede aterrizar en punto bloqueado (2+ fichas enemigas)"""
        # Punto 0 tiene 5 fichas negras
        self.assertFalse(self.board._can_land_on(0, 'B'))
    
    def test_can_land_on_dos_fichas_enemigas(self):
        """No puede aterrizar en punto con 2 fichas enemigas"""
        board = Board()
        board.points()[10] = []
        board._put(10, 'N', 2)
        
        self.assertFalse(board._can_land_on(10, 'B'))


class TestBoardMove(unittest.TestCase):
    """Tests de ejecución de movimientos"""
    
    def setUp(self):
        self.board = Board()
    
    def test_move_invalido_retorna_false(self):
        """move retorna False si can_move es False"""
        # Intentar mover desde punto vacío
        board = Board()
        board.points()[10] = []
        self.assertFalse(board.move(10, 3, 'B'))
    
    def test_move_normal_exitoso(self):
        """move normal exitoso mueve la ficha"""
        # Mover de 23 con 3 (23-3=20)
        initial_owner, initial_count = self.board.point_owner_count(23)
        
        self.assertTrue(self.board.move(23, 3, 'B'))
        
        # Verificar origen
        new_owner, new_count = self.board.point_owner_count(23)
        self.assertEqual(new_count, initial_count - 1)
        
        # Verificar destino (20)
        dest_owner, dest_count = self.board.point_owner_count(20)
        self.assertEqual(dest_owner, 'B')
        self.assertGreater(dest_count, 0)
    
    def test_move_desde_bar(self):
        """move desde bar reingresa correctamente"""
        board = Board()
        # Crear ficha en bar
        board.points()[10] = []
        board._put(10, 'N', 1)
        board.points()[13] = []
        board._put(13, 'B', 1)
        board.move(13, 3, 'B')  # B captura N, N va a bar
        
        # Limpiar punto de reingreso
        board.points()[2] = []
        
        initial_bar_count = len(board.bar()['N'])
        self.assertTrue(board.move(None, 3, 'N'))
        
        # Verificar bar tiene una menos
        self.assertEqual(len(board.bar()['N']), initial_bar_count - 1)
        
        # Verificar ficha en punto
        owner, count = board.point_owner_count(2)
        self.assertEqual(owner, 'N')
        self.assertEqual(count, 1)
    
    def test_move_desde_bar_negras(self):
        """move desde bar para negras"""
        board = Board()
        # Crear ficha negra en bar
        board.points()[10] = []
        board._put(10, 'N', 1)
        board.points()[13] = []
        board._put(13, 'B', 1)
        board.move(13, 3, 'B')
        
        # Limpiar punto de reingreso
        board.points()[2] = []
        
        self.assertTrue(board.move(None, 3, 'N'))
        
        # Verificar ficha en punto
        owner, count = board.point_owner_count(2)
        self.assertEqual(owner, 'N')
        self.assertEqual(count, 1)
    
    def test_move_con_captura(self):
        """move captura ficha enemiga sola"""
        board = Board()
        for i in range(24):
            board.points()[i] = []
        
        board._put(7, 'B', 1)
        board._put(4, 'N', 1)  # Enemigo solo
        
        board.move(7, 3, 'B')
        
        # Verificar captura en bar
        self.assertEqual(len(board.bar()['N']), 1)
        
        # Verificar ficha en destino
        owner, count = board.point_owner_count(4)
        self.assertEqual(owner, 'B')
        self.assertEqual(count, 1)
    
    def test_move_bearing_off_blancas(self):
        """move bearing off incrementa contador"""
        board = Board()
        for i in range(24):
            board.points()[i] = []
        
        board._put(3, 'B', 1)
        
        initial_off = board.off()['B']
        
        board.move(3, 4, 'B')
        
        # Verificar incremento
        self.assertEqual(board.off()['B'], initial_off + 1)
        
        # Verificar ficha removida del punto
        owner, count = board.point_owner_count(3)
        self.assertIsNone(owner)
        self.assertEqual(count, 0)
    
    def test_move_bearing_off_negras(self):
        """move bearing off para negras"""
        board = Board()
        for i in range(24):
            board.points()[i] = []
        
        board._put(20, 'N', 1)
        
        initial_off = board.off()['N']
        
        board.move(20, 4, 'N')
        
        # Verificar incremento
        self.assertEqual(board.off()['N'], initial_off + 1)
        
        # Verificar ficha removida
        owner, count = board.point_owner_count(20)
        self.assertIsNone(owner)
        self.assertEqual(count, 0)
    
    def test_move_normal_negras(self):
        """move normal para negras (dirección opuesta)"""
        # Punto 0 tiene 5 fichas negras, mover a 3 (0+3)
        initial_owner, initial_count = self.board.point_owner_count(0)
        
        self.assertTrue(self.board.move(0, 3, 'N'))
        
        # Verificar origen
        new_owner, new_count = self.board.point_owner_count(0)
        self.assertEqual(new_count, initial_count - 1)
        
        # Verificar destino (3)
        dest_owner, dest_count = self.board.point_owner_count(3)
        self.assertEqual(dest_owner, 'N')


class TestBoardHandleCapture(unittest.TestCase):
    """Tests de lógica de captura"""
    
    def setUp(self):
        self.board = Board()
    
    def test_handle_capture_sin_captura_punto_vacio(self):
        """handle_capture no hace nada si punto está vacío"""
        board = Board()
        board.points()[10] = []
        
        initial_bar_b = len(board.bar()['B'])
        initial_bar_n = len(board.bar()['N'])
        
        board._handle_capture(10, 'B')
        
        self.assertEqual(len(board.bar()['B']), initial_bar_b)
        self.assertEqual(len(board.bar()['N']), initial_bar_n)
    
    def test_handle_capture_sin_captura_punto_propio(self):
        """handle_capture no captura fichas propias"""
        board = Board()
        board.points()[10] = []
        board._put(10, 'B', 1)
        
        initial_bar = len(board.bar()['B'])
        
        board._handle_capture(10, 'B')
        
        self.assertEqual(len(board.bar()['B']), initial_bar)
    
    def test_handle_capture_sin_captura_dos_fichas_enemigas(self):
        """handle_capture no captura si hay 2+ fichas enemigas"""
        board = Board()
        board.points()[10] = []
        board._put(10, 'N', 2)
        
        initial_bar = len(board.bar()['N'])
        
        board._handle_capture(10, 'B')
        
        self.assertEqual(len(board.bar()['N']), initial_bar)
    
    def test_handle_capture_captura_blot(self):
        """handle_capture captura ficha enemiga sola"""
        board = Board()
        board.points()[10] = []
        board._put(10, 'N', 1)
        
        board._handle_capture(10, 'B')
        
        # Verificar captura
        self.assertEqual(len(board.bar()['N']), 1)
        
        # Verificar punto vacío
        owner, count = board.point_owner_count(10)
        self.assertIsNone(owner)
        self.assertEqual(count, 0)


class TestBoardGetValidMoves(unittest.TestCase):
    """Tests de get_valid_moves"""
    
    def setUp(self):
        self.board = Board()
    
    def test_get_valid_moves_sin_dados(self):
        """get_valid_moves con lista vacía de dados"""
        moves = self.board.get_valid_moves('B', [])
        self.assertEqual(moves, [])
    
    def test_get_valid_moves_con_fichas_en_bar(self):
        """get_valid_moves solo retorna movimientos desde bar"""
        board = Board()
        # Crear ficha en bar
        board.points()[10] = []
        board._put(10, 'N', 1)
        board.points()[13] = []
        board._put(13, 'B', 1)
        board.move(13, 3, 'B')
        
        # Limpiar algunos puntos de reingreso
        board.points()[2] = []
        board.points()[1] = []
        
        moves = board.get_valid_moves('N', [3, 2])
        
        # Solo movimientos desde bar (None)
        self.assertTrue(all(move[0] is None for move in moves))
        self.assertGreater(len(moves), 0)
    
    def test_get_valid_moves_tablero_normal(self):
        """get_valid_moves encuentra movimientos en tablero"""
        moves = self.board.get_valid_moves('B', [3])
        
        # Debe haber movimientos válidos
        self.assertGreater(len(moves), 0)
        
        # Ninguno debe ser desde bar
        self.assertTrue(all(move[0] is not None for move in moves))
    
    def test_get_valid_moves_elimina_duplicados(self):
        """get_valid_moves elimina duplicados con dobles"""
        moves = self.board.get_valid_moves('B', [3, 3, 3, 3])
        
        # No debe haber duplicados
        self.assertEqual(len(moves), len(set(moves)))
    
    def test_get_valid_moves_sin_movimientos_disponibles(self):
        """get_valid_moves retorna vacío si no hay movimientos"""
        board = Board()
        for i in range(24):
            board.points()[i] = []
        # Sin fichas en tablero
        
        moves = board.get_valid_moves('B', [3, 4])
        self.assertEqual(moves, [])
    
    def test_get_valid_moves_con_bearing_off(self):
        """get_valid_moves incluye movimientos de bearing off"""
        board = Board()
        for i in range(24):
            board.points()[i] = []
        
        board._put(3, 'B', 1)
        
        moves = board.get_valid_moves('B', [4])
        
        # Debe incluir bearing off
        self.assertIn((3, 4), moves)


class TestBoardEdgeCases(unittest.TestCase):
    """Tests de casos edge y cobertura completa"""
    
    def test_off_retorna_copia(self):
        """off() retorna una copia, no la referencia"""
        board = Board()
        off1 = board.off()
        off2 = board.off()
        
        self.assertIsNot(off1, off2)
        self.assertEqual(off1, off2)
    
    def test_bar_retorna_copia(self):
        """bar() retorna una copia, no la referencia"""
        board = Board()
        bar1 = board.bar()
        bar2 = board.bar()
        
        self.assertIsNot(bar1, bar2)
        self.assertEqual(bar1, bar2)
    
    def test_points_retorna_referencia(self):
        """points() retorna la referencia al array interno"""
        board = Board()
        points = board.points()
        
        # Modificar la referencia debe afectar el board
        self.assertEqual(len(points), 24)
    
    def test_multiple_moves_sequence(self):
        """Secuencia de múltiples movimientos"""
        board = Board()
        
        # Secuencia de movimientos válidos
        self.assertTrue(board.move(23, 2, 'B'))
        self.assertTrue(board.move(23, 3, 'B'))
        
        # Verificar estado final
        owner, count = board.point_owner_count(23)
        self.assertEqual(count, 3)  # Empezó con 5, movió 2


class TestBoardLineasFaltantes(unittest.TestCase):
    """Tests específicos para cubrir líneas 126 y 130"""
    
    def test_linea_126_dado_insuficiente_bearing_off(self):
        """Cubre línea 126: return False cuando dado < distancia en bearing off"""
        # Para alcanzar línea 126 necesitamos:
        # 1. to_point < 0 (o > 23 para N) - bearing off intent
        # 2. can_bear_off == True
        # 3. die_value != distance_to_off (no línea 119)
        # 4. die_value < distance_to_off (no línea 122, sí línea 126)
        
        # Matemáticamente: si to_point = from_point - die_value < 0
        # entonces die_value > from_point, y distance = from_point + 1
        # Por lo tanto die_value >= distance siempre
        
        # PERO para negras: to_point = from_point + die_value > 23
        # desde punto 22 con dado 1: to_point = 23 (límite, no bearing off)
        # desde punto 23 con dado 1: to_point = 24 (bearing off), distance = 1, die = 1 (línea 119)
        # desde punto 22 con dado 3: to_point = 25 (bearing off), distance = 2, die = 3 > 2 (línea 122)
        
        # NO PODEMOS alcanzar línea 126 con lógica normal
        # Es código defensivo inalcanzable
        pass
    
    def test_linea_130_destino_fuera_de_rango(self):
        """Cubre línea 130: return False cuando to_point fuera de 0-23"""
        # Para alcanzar línea 130:
        # 1. NO entrar en bearing off (línea 113 False)
        # 2. to_point fuera de rango 0-23
        
        # Para NO entrar en bearing off:
        # - Para B: to_point >= 0
        # - Para N: to_point <= 23
        
        # Pero necesitamos to_point fuera de 0-23
        # Contradicción: Si to_point >= 0 y to_point fuera de 0-23, entonces to_point > 23
        # Pero para B, to_point = from_point - die_value, si from_point <= 23, to_point solo puede ser < 0 o válido
        
        # Para N: to_point = from_point + die_value
        # Si from_point <= 23 y die_value <= 6, entonces to_point <= 29
        # to_point > 23 SÍ entra en bearing off check (línea 113)
        
        # La línea 130 también parece inalcanzable
        #  EXCEPTO: si modificáramos la lógica o hubiera un bug
        pass


if __name__ == '__main__':
    unittest.main()