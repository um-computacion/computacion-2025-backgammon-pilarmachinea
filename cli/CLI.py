from core import BackgammonGame

OWNER_ICON = {"B": "B", "N": "N", None: "."}

def index_from_human(n):
    if not 1 <= n <= 24:
        raise ValueError("El punto debe estar entre 1 y 24.")
    return n - 1

def distance_for_move(src_idx, dst_idx, player):
    return (src_idx - dst_idx) if player == "B" else (dst_idx - src_idx)

def consume_die(dice, dist):
    try:
        i = dice.index(dist)
        dice.pop(i)
        return True
    except ValueError:
        return False

def do_hit_if_single(board, dst_idx, player):
    owner, count = board.point_owner_count(dst_idx)
    if owner is not None and owner != player and count == 1:
        board.points()[dst_idx].pop()

def render_board_ascii(game):
    b = game.board()
    top = list(range(23, 11, -1))   # 24..13
    bottom = list(range(0, 12, 1))  # 1..12

    def point_owner_count(idx):
        return b.point_owner_count(idx)

    def human(idx): return idx + 1
    def cell(idx):
        owner, count = point_owner_count(idx)
        return " . " if owner is None else f" {OWNER_ICON[owner]}{count}"

    line = "+" + ("----" * 12) + "+"
    top_hdr = " ".join(f"{human(i):>2}" for i in top)
    bot_hdr = " ".join(f"{human(i):>2}" for i in bottom)
    top_row = " ".join(cell(i) for i in top)
    bot_row = " ".join(cell(i) for i in bottom)

    turno = game.turno()
    dice = game.dice()
    dice_str = " ".join(str(d) for d in dice) if dice else "(sin tirar)"
    return (
        f"\nTurno: {turno} | Dados: {dice_str}\n"
        f"{line}\n  {top_hdr}\n{line}\n"
        f"| {top_row} |\n{line}\n"
        f"| {bot_row} |\n{line}\n"
        f"  {bot_hdr}\n{line}\n"
    )

def print_help():
    print("Comandos:\nshow, roll, move <src> <dst>, help, quit")

def main():
    game = BackgammonGame(player1="Blancas", player2="Negras")
    print(render_board_ascii(game))
    while True:
        try:
            cmd = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n¡Chau!"); break

        if cmd in ("quit", "exit"):
            print("¡Chau!"); break
        if cmd == "help":
            print_help(); continue
        if cmd == "show":
            print(render_board_ascii(game)); continue
        if cmd == "roll":
            rolled = game.roll()
            print(f"Tiraste: {rolled}")
            print(render_board_ascii(game)); continue

        if cmd.startswith("move"):
            parts = cmd.split()
            if len(parts) != 3 or not parts[1].isdigit() or not parts[2].isdigit():
                print("Uso: move <src> <dst> (1..24)"); continue

            src_h, dst_h = int(parts[1]), int(parts[2])
            dice = game.dice()
            if not dice:
                print("Primero tirá los dados con 'roll'."); continue

            src, dst = index_from_human(src_h), index_from_human(dst_h)
            board = game.board()
            pts = board.points()
            if not pts[src]:
                print(f"No hay fichas en {src_h}."); continue

            turn = game.turno()  
            if pts[src][0].color() != turn:
                print(f"Esa ficha no es tuya. Turno de {turn}."); continue

            dist = distance_for_move(src, dst, turn)
            if dist <= 0:
                print("Dirección inválida para tu color."); continue

            owner_dst, count_dst = board.point_owner_count(dst)
            if owner_dst is not None and owner_dst != turn and count_dst >= 2:
                print("Destino bloqueado (2 o más del rival)."); continue

            if not consume_die(dice, dist):
                print(f"No tenés el valor {dist} disponible en los dados."); continue
            do_hit_if_single(board, dst, turn)


            checker = pts[src].pop()
            pts[dst].append(checker)
            print(f"Movida OK: {src_h} -> {dst_h} (usaste {dist}).")
            print(render_board_ascii(game)); continue

        print("Comando no reconocido. Escribí 'help'.")

if __name__ == "__main__":
    main()
