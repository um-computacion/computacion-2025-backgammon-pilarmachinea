from core import BackgammonGame

OWNER_ICON = {"B": "B", "N": "N", None: "."}

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
    print("Comandos:\nshow, help, quit")

def main():
    game = BackgammonGame(player1="Blancas", player2="Negras")
    print(render_board_ascii(game))
    while True:
        try:
            cmd = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nChau!"); break
        if cmd in ("quit", "exit"): print("Chau!"); break
        if cmd == "help": print_help(); continue
        if cmd == "show": print(render_board_ascii(game)); continue
        if cmd == "roll":
            rolled = game.roll()
            print(f"Tiraste: {rolled}")
            print(render_board_ascii(game)); continue

        print("Comandos:\nshow, help, roll, quit")

if __name__ == "__main__":
    main()
