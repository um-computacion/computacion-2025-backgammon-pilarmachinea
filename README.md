# Backgammon - Computación 2025
Implementación del juego de Backgammon en Python con interfaces CLI y gráfica (Pygame)

## Estructura del Proyecto
```
backgammon/
├── core/                   # Lógica del juego
│   ├── __init__.py
│   ├── BackgammonGame.py  # Coordinador principal
│   ├── Board.py           # Tablero y movimientos
│   ├── Player.py          # Jugador
│   ├── Dice.py            # Dados
│   └── Checker.py         # Fichas
├── cli/                   # Interfaz de línea de comandos
│   └── main.py
├── pygame_ui/             # Interfaz gráfica
│   ├── PygameUI.py
│   └── game_pygame.py
├── tests/                 # Tests unitarios
│   ├── test_backgammongame.py
│   ├── test_board.py
│   ├── test_player.py
│   ├── test_dice.py
│   └── test_checker.py
│
├── requirements.txt
├── CHANGELOG.md
├── JUSTIFICACION.md
└── README.md
```

## Requisitos
- Python 3.12+
- Pygame 2.5.0+

## Instalación
### 1. Clonar el repositorio
```bash
git clone <url-repositorio>
cd backgammon
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## Ejecución
### Modo CLI (Línea de Comandos)
```bash
python cli/main.py
```

### Modo Gráfico (Pygame)
```bash
python pygame_ui/game_pygame.py
```

## Testing
### Ejecutar todos los tests
```bash
python -m pytest tests/ -v
```

### Ejecutar tests con cobertura
```bash
python -m pytest tests/ --cov=core --cov-report=html
```

### Ver reporte de cobertura
```bash
# El reporte HTML estará en htmlcov/index.html
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
```

## Docker (Próximamente)
### Modo Testing
```bash
docker build -t backgammon-test -f Dockerfile.test .
docker run backgammon-test
```

### Modo Juego
```bash
docker build -t backgammon-game .
docker run -it backgammon-game
```

## Reglas del Juego
El Backgammon es un juego de mesa para 2 jugadores donde cada uno tiene 15 fichas que deben mover alrededor del tablero según el resultado de los dados.

### Objetivo
Ser el primero en mover todas las fichas a tu zona home y sacarlas del tablero.

### Movimientos
- Se tiran 2 dados por turno
- Las fichas se mueven según el valor de los dados
- Si salen dobles, se juega 4 veces ese valor
- Las blancas se mueven de 23→0
- Las negras se mueven de 0→23

### Reglas Especiales
- **Captura**: Si aterrizas en un punto con solo 1 ficha enemiga, la capturas
- **Bar**: Las fichas capturadas van al bar y deben reentrar antes de mover otras
- **Bearing Off**: Cuando todas las fichas están en home (0-5 para blancas, 18-23 para negras), puedes sacarlas del tablero

## Controles

### CLI
- Comandos de texto para interactuar con el juego

### Pygame
- **ESPACIO**: Tirar dados
- **Click izquierdo**: Seleccionar punto/ficha
- **Click en dado**: Ejecutar movimiento
- **T**: Terminar turno
- **ESC**: Salir

## Arquitectura

El proyecto sigue los principios SOLID:
- **S**ingle Responsibility: Cada clase tiene una única responsabilidad
- **O**pen/Closed: Abierto a extensión, cerrado a modificación
- **L**iskov Substitution: Las subclases pueden sustituir a sus clases base
- **I**nterface Segregation: Interfaces específicas para cada cliente
- **D**ependency Inversion: Dependencia de abstracciones, no de concreciones

## Autores
- Pilar Machinea - Computación 2025

## Licencia
Proyecto educativo - Universidad