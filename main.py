"""
Script principal para probar el juego de Backgammon
Ejecutar desde la raíz del proyecto: python main.py
"""
from core import BackgammonGame

def mostrar_tablero(game):
    """Muestra el estado actual del tablero de forma simple"""
    print("\n" + "="*60)
    print(f"Turno de: {game.current_player().nombre()} ({game.turno()})")
    print("="*60)
    
    board = game.board()
    
    # Mostrar bar
    bar = board.bar()
    if bar['B'] or bar['N']:
        print(f"BAR -> B: {len(bar['B'])}, N: {len(bar['N'])}")
    
    # Mostrar puntos (mitad superior)
    print("\nPuntos 12-23:")
    for i in range(12, 24):
        owner, count = board.point_owner_count(i)
        if count > 0:
            print(f"  Punto {i:2d}: {owner} x{count}")
    
    print("\nPuntos 0-11:")
    for i in range(0, 12):
        owner, count = board.point_owner_count(i)
        if count > 0:
            print(f"  Punto {i:2d}: {owner} x{count}")
    
    print("="*60 + "\n")

def probar_movimientos():
    """Función de prueba para los movimientos básicos"""
    print("PROBANDO BACKGAMMON - MOVIMIENTOS\n")
    
    game = BackgammonGame("Jugador 1", "Jugador 2")
    
    print("TABLERO INICIAL:")
    mostrar_tablero(game)
    
    print("Blancas tiran los dados...")
    dados = game.roll()
    print(f"   Dados: {dados}")
    print(f"   Dados disponibles: {game.available_dice()}")
    
    movimientos = game.get_valid_moves()
    print(f"\nMovimientos válidos disponibles: {len(movimientos)}")
    if movimientos:
        print("   Primeros 5 movimientos:")
        for mov in movimientos[:5]:
            from_point, die = mov
            if from_point is None:
                print(f"     - Desde BAR usando dado {die}")
            else:
                print(f"     - Desde punto {from_point} usando dado {die}")
    
    if dados:
        print(f"\nIntentando mover desde punto 23 con dado {dados[0]}...")
        if game.move(23, dados[0]):
            print("Movimiento exitoso!")
        else:
            print("Movimiento inválido")
        
        mostrar_tablero(game)
        print(f"   Dados restantes: {game.available_dice()}")
    
    dados_disponibles = game.available_dice()
    if dados_disponibles:
        print(f"\nIntentando mover desde punto 12 con dado {dados_disponibles[0]}...")
        if game.move(12, dados_disponibles[0]):
            print("Movimiento exitoso!")
        else:
            print("Movimiento inválido")
        
        mostrar_tablero(game)
        print(f"   Dados restantes: {game.available_dice()}")
    
    print("\nIntentando terminar turno...")
    if game.can_end_turn():
        game.end_turn()
        print("Turno terminado!")
    else:
        print("Aún hay movimientos disponibles, no se puede terminar")
    
    print("\n" + "="*60)
    print("Negras tiran los dados...")
    dados = game.roll()
    print(f"   Dados: {dados}")
    
    movimientos = game.get_valid_moves()
    print(f"\nMovimientos válidos disponibles: {len(movimientos)}")
    
    mostrar_tablero(game)
    
    print("\nPrueba completada")

def probar_captura():
    """Función para probar la captura de fichas"""
    print("\n\nPROBANDO CAPTURA DE FICHAS\n")
    
    game = BackgammonGame()
    board = game.board()
    
    print("⚙️  Configurando escenario de captura...")
    print("   (Esto es solo para pruebas, normalmente no harías esto)\n")
    
    board.points()[15] = []
    from core.Checker import Checker
    board.points()[15].append(Checker('N'))
    
    print(f"✓ Punto 15 tiene 1 ficha Negra (blot)")
    
    board.points()[18] = []
    board.points()[18].append(Checker('B'))
    board.points()[18].append(Checker('B'))
    
    print(f"✓ Punto 18 tiene 2 fichas Blancas")
    
    mostrar_tablero(game)
    
    game._BackgammonGame__dice_cache__ = [3, 5]
    print(f"Dados simulados: [3, 5]")
    print(f"\nMoviendo desde punto 18 con dado 3 (debería capturar en punto 15)...")
    
    if game.move(18, 3):
        print("Movimiento y captura exitosos!")
        mostrar_tablero(game)
        
        bar = board.bar()
        print(f"Fichas en el BAR: B={len(bar['B'])}, N={len(bar['N'])}")
        
        if len(bar['N']) > 0:
            print("¡Ficha negra capturada correctamente!")
        else:
            print("ERROR: No se capturó la ficha")
    else:
        print("Movimiento falló")
    
    print("\nPrueba de captura completada!")

if __name__ == "__main__":
    try:
        probar_movimientos()
        probar_captura()
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()