#!/usr/bin/env python3
"""
Backgammon - Juego de Mesa
Juego por turnos para 2 jugadores en la terminal
"""
from core.BackgammonGame import BackgammonGame

def limpiar_pantalla():
    """Limpia la pantalla (funciona en Linux/Mac/Windows)"""
    import os
    os.system('clear' if os.name == 'posix' else 'cls')

def mostrar_tablero(game):
    """Muestra el tablero de backgammon en la terminal"""
    board = game.board()
    print("\n" + "="*70)
    print(" "*25 + "BACKGAMMON")
    print("="*70)
    # Mostrar bar (fichas capturadas)
    bar = board.bar()
    if bar['B'] or bar['N']:
        print(f"\nBAR - Blancas: {len(bar['B'])} | Negras: {len(bar['N'])}")
    # Línea superior (puntos 12-23)
    print("\n" + "-"*70)
    print("PUNTOS: ", end="")
    for i in range(12, 24):
        print(f"{i:3}", end=" ")
    print()
    print("-"*70)
    # Mostrar fichas en puntos superiores (12-23)
    for i in range(12, 24):
        owner, count = board.point_owner_count(i)
        if count > 0:
            simbolo = "B" if owner == 'B' else "N"
            print(f"{simbolo}{count:2}", end=" ")
        else:
            print("  .", end=" ")
    print()
    print("\n" + " "*32 + "DADOS")
    print()
    # Mostrar fichas en puntos inferiores (11-0)
    for i in range(11, -1, -1):
        owner, count = board.point_owner_count(i)
        if count > 0:
            simbolo = "B" if owner == 'B' else "N"
            print(f"{simbolo}{count:2}", end=" ")
        else:
            print("  .", end=" ")
    print()
    # Línea inferior (puntos 0-11)
    print("-"*70)
    print("PUNTOS: ", end="")
    for i in range(11, -1, -1):
        print(f"{i:3}", end=" ")
    print()
    print("-"*70)

def mostrar_turno(game):
    """Muestra información del turno actual"""
    player = game.current_player()
    color_texto = "BLANCAS" if player.es_blanco() else "NEGRAS"
    print(f"\nTURNO: {color_texto} ({player.nombre()})")
    dados = game.available_dice()
    if dados:
        print(f"Dados disponibles: {dados}")
    else:
        print("No hay dados (presiona 'r' para tirar)")

def mostrar_movimientos_validos(game):
    """Muestra los movimientos válidos disponibles"""
    moves = game.get_valid_moves()
    if not moves:
        print("\n[X] No hay movimientos válidos disponibles")
        return
    print(f"\n[OK] Movimientos válidos disponibles ({len(moves)}):")
    # Agrupar por punto de origen
    moves_dict = {}
    for from_point, die in moves:
        origen = "BAR" if from_point is None else str(from_point)
        if origen not in moves_dict:
            moves_dict[origen] = []
        moves_dict[origen].append(die)
    for origen, dados in moves_dict.items():
        print(f"   Desde {origen}: dados {dados}")

def obtener_comando():
    """Solicita y procesa un comando del usuario"""
    print("\n" + "-"*70)
    print("Comandos: [r]oll | [m]over FROM DADO | [v]er movimientos | [t]erminar turno | [q]uit")
    comando = input(">>> ").strip().lower()
    return comando

def procesar_movimiento(game, comando):
    """Procesa un comando de movimiento"""
    partes = comando.split()
    if len(partes) != 3:
        print("[X] Formato: m FROM DADO (ejemplo: m 23 3)")
        print("Para mover desde el bar: m bar 3")
        return False
    _, from_str, die_str = partes
    try:
        # Parsear origen
        if from_str.lower() == 'bar':
            from_point = None
        else:
            from_point = int(from_str)
            if from_point < 0 or from_point > 23:
                print("[X] El punto debe estar entre 0 y 23")
                return False
        # Parsear dado
        die_value = int(die_str)
        if die_value < 1 or die_value > 6:
            print("[X] El dado debe estar entre 1 y 6")
            return False
        # Intentar el movimiento
        if game.move(from_point, die_value):
            origen = "BAR" if from_point is None else f"punto {from_point}"
            print(f"[OK] Movimiento exitoso desde {origen} con dado {die_value}")
            return True
        else:
            print("[X] Movimiento inválido")
            return False 
    except ValueError:
        print("[X] Formato inválido. Usa números.")
        return False

def jugar():
    """Función principal del juego"""
    print("\n" + "="*70)
    print(" "*25 + "BACKGAMMON")
    print("="*70)
    # Configurar jugadores
    print("\nNombres de los jugadores? (Enter para usar nombres por defecto)")
    nombre1 = input("Jugador Blancas: ").strip() or "Blancas"
    nombre2 = input("Jugador Negras: ").strip() or "Negras"
    # Crear juego
    game = BackgammonGame(nombre1, nombre2)
    jugando = True
    while jugando:
        limpiar_pantalla()
        mostrar_tablero(game)
        mostrar_turno(game)
        comando = obtener_comando()
        # Procesar comando
        if comando == 'q' or comando == 'quit':
            print("\nGracias por jugar!")
            jugando = False   
        elif comando == 'r' or comando == 'roll':
            if game.available_dice():
                print("[X] Ya tiraste los dados este turno")
            else:
                dados = game.roll()
                print(f"Tiraste: {dados}")
            input("\nPresiona Enter para continuar...")
        elif comando.startswith('m'):
            procesar_movimiento(game, comando)
            input("\nPresiona Enter para continuar...") 
        elif comando == 'v' or comando == 'ver':
            mostrar_movimientos_validos(game)
            input("\nPresiona Enter para continuar...")
        elif comando == 't' or comando == 'terminar':
            if not game.available_dice():
                print("[X] Debes tirar los dados primero")
            elif game.has_valid_moves():
                print("[X] Aún tienes movimientos válidos disponibles")
                print("Usa 'v' para verlos")
            else:
                game.end_turn()
                print("[OK] Turno terminado")
            input("\nPresiona Enter para continuar...")
        else:
            print("[X] Comando no reconocido")
            input("\nPresiona Enter para continuar...")

def main():
    """Punto de entrada del programa"""
    try:
        jugar()
    except KeyboardInterrupt:
        print("\n\nJuego interrumpido! Hasta luego.")
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()