from core import BackgammonGame

def print_help():
    print(
        "Comandos:\n"
        "  show   -> muestra tablero\n"
        "  help   -> esta ayuda\n"
        "  quit   -> salir\n"
    )

def main():
    game = BackgammonGame(player1="Blancas", player2="Negras")
    print("Backgammon CLI iniciado. Escribí 'help' para ver comandos.")

    while True:
        try:
            cmd = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nAdios!"); break

        if cmd in ("quit", "exit"):
            print("Adios!"); break
        if cmd == "help":
            print_help(); continue
        if cmd == "show":
            print("nose todavia .............."); continue

        print("Comando no reconocido. Escribí 'help'.")

if __name__ == "__main__":
    main()