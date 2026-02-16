# JUSTIFICACION.md

## 1. Resumen del diseño general

El proyecto implementa el juego **Backgammon** separando claramente la **lógica de juego** de las **interfaces**.  
El código está estructurado en módulos independientes, lo que facilita el mantenimiento, el testing y la posibilidad de agregar nuevas interfaces sin modificar la base.

- **`core/`** → Lógica pura del juego (tablero, dados, movimientos, validaciones, turnos).  
- **`pygame_ui/`** → Interfaz gráfica construida con Pygame.  
- **`cli/`** → Contiene la versión por consola (CLI.py) con comandos interactivos.
- **`main.py`** → Archivo principal en la raíz del proyecto que lanza una versión simplificada por terminal (sin comandos).
- **`tests/`** → Conjunto de pruebas unitarias para cada clase principal.

El objetivo fue lograr una estructura **modular**, **probada** y **fácil de extender**, donde las reglas del juego se ejecuten correctamente sin importar si se usa interfaz visual o consola.

---

## 2. Justificación de clases y responsabilidades

### `core/Board`
- **Qué modela:** El estado completo del tablero (24 puntos, barra y área de retiro).  
- **Por qué existe:** Para encapsular todas las reglas que dependen del estado del tablero, como si un movimiento es válido o si una ficha puede salir del tablero.  
- **Responsabilidades principales:**
  - Mantener las listas de puntos (`points`), barra (`bar`) y off (`off`).
  - Determinar si un movimiento es válido (`can_move`).
  - Ejecutar los movimientos (`move`).
  - Verificar si se puede realizar el bear-off (`can_bear_off`).
  - Calcular movimientos válidos (`get_valid_moves`).

### `core/BackgammonGame`
- **Qué modela:** El flujo del juego: turnos, tiradas de dados, jugadores y condiciones de victoria.  
- **Por qué existe:** Para coordinar el tablero, los jugadores y los dados sin depender de la interfaz.  
- **Responsabilidades principales:**
  - Administrar los turnos.
  - Tirar y registrar los dados (`roll`, `dice`, `available_dice`).
  - Validar y ejecutar movimientos (`can_move`, `move`).
  - Finalizar el turno (`end_turn`).
  - Detectar el fin de partida y al ganador (`is_game_over`, `winner`).

### `core/Checker`
- **Qué modela:** Cada ficha del juego.  
- **Por qué existe:** Para representar de forma simple y clara el color de cada ficha.  
- **Responsabilidades principales:**
  - Guardar su color (`B` o `N`).
  - Devolverlo cuando se consulta (`color()`).

### `core/Dice`
- **Qué modela:** La tirada de los dados en cada turno.  
- **Por qué existe:** Para manejar de forma centralizada la generación de números aleatorios y la regla de los dobles.  
- **Responsabilidades principales:**
  - Generar tiradas (`roll`).
  - Guardar la última tirada (`last`).
  - En caso de dobles, devolver cuatro valores iguales (regla estándar del backgammon).

### `core/Player`
- **Qué modela:** A cada jugador del juego.  
- **Por qué existe:** Para manejar nombre y color, validando los valores permitidos.  
- **Responsabilidades principales:**
  - Validar el color (“blanco” o “negro”).
  - Exponer métodos como `es_blanco()`, `es_negro()` y `nombre()`.

### `pygame_ui/BackgammonUI`
- **Qué modela:** Toda la interfaz visual del juego.  
- **Por qué existe:** Para manejar la experiencia del jugador, la interacción con el ratón y el renderizado del tablero.  
- **Responsabilidades principales:**
  - Dibujar tablero, fichas, barra, off, dados y mensajes.
  - Interpretar clics del usuario y enviar las acciones al `BackgammonGame`.
  - Mostrar mensajes de ayuda, bloqueos o fin de turno.

### `CLI.py`
**Qué modela:** La versión interactiva del juego en consola, útil para pruebas y defensa oral.
**Responsabilidades principales:**
  - Mostrar el tablero en texto.
  - Pedir y procesar los comandos (`roll`, `move`, `ver`, `terminar`, etc.).
  - Permitir jugar sin interfaz gráfica, con reglas y turnos idénticos a la versión Pygame.

### `main.py`
**Qué modela:** Un lanzador simplificado del juego desde la terminal.
**Por qué existe:** Para ejecutar partidas rápidas sin comandos complejos.
**Responsabilidades principales:**
  - Mostrar el tablero básico en consola.
  - Pedir los nombres de los jugadores
  - Correr una partida completa con turnos y tiradas de dados.

---

## 3. Justificación de atributos elegidos

- **`Board`**
  - `points`: lista de 24 listas de fichas (`Checker`), refleja directamente la estructura del tablero.  
  - `bar`: diccionario con listas de fichas capturadas por color.  
  - `off`: diccionario con conteo de fichas retiradas, simplifica el chequeo de victoria.

- **`BackgammonGame`**
  - `players`: contiene ambos jugadores.  
  - `turn`: mantiene de forma simple el color del turno actual (`'B'` o `'N'`).  
  - `dice`: objeto separado para centralizar la lógica de tiradas.  
  - `board`: composición que contiene el estado del tablero.

- **`Dice`**
  - `_last`: guarda la tirada anterior para consulta sin repetir la tirada.

- **`Player`**
  - `_color` y `_nombre`: encapsulan identidad y validación de color.

- **`BackgammonUI`**
  - Atributos visuales (`info_message`, `punto_seleccionado`, `dado_seleccionado`) y constantes de tablero para centralizar toda la configuración visual.

---

## 4. Decisiones de diseño relevantes

- **Regla de bear-off exacta:** Se decidió que solo se puede retirar una ficha del tablero si el valor del dado coincide exactamente con la cantidad de casillas restantes.  
- **Entrada desde el bar:** Si hay fichas en el bar, deben salir primero antes de mover otras fichas.  
- **Visualización de fichas:**  
  - Fichas apoyadas en la base del triángulo.  
  - Máximo de 5 fichas visibles; si hay más, se muestra “+n”.  
  - Fichas retiradas (off) representadas como tiritas apiladas.  
- **Separación total entre lógica y presentación:**  
  - La lógica (core) no tiene dependencias con Pygame.  
  - La UI solo usa métodos públicos (`can_move`, `move`, `roll`, `end_turn`).  
- **Ejecutar con `python -m`** para mantener imports limpios y estables.  
- **Mensajes informativos** para el usuario cuando no hay movimientos válidos.

---

## 5. Excepciones y manejo de errores

- **Validaciones en `Player`:**  
  Si el color no es “blanco” o “negro”, se lanza `ValueError`.  
  Esto evita crear jugadores inválidos.

- **Lógica de juego (`Board` y `Game`):**  
  Los movimientos inválidos no lanzan excepciones, sino que devuelven `False`.  
  Solo los errores inesperados levantan excepciones.

- **En la interfaz (Pygame):**  
  Se usa `try/except` para capturar errores y mostrarlos visualmente sin romper el juego.  
  Además, se muestran mensajes como “Sin movimientos válidos. Se pasa el turno…”.

- **En la CLI:**  
  Se validan entradas numéricas y se informa si el comando o formato es incorrecto.

---

## 6. Estrategia de testing y cobertura

- **Framework utilizado:** `unittest` (nativo de Python).  
- **Archivos de prueba:** uno por clase (`test_dice.py`, `test_board.py`, `test_player.py`, etc.).  

### Qué se prueba
- **`Dice`** → Valores válidos (1–6), dobles → 4 tiradas iguales, comportamiento de `last()`.  
- **`Checker`** → Color correcto.  
- **`Player`** → Validaciones de color, mayúsculas, nulos y errores esperados.  
- **`Board`** →  
  - Movimientos válidos e inválidos.  
  - Reingreso desde el bar.  
  - Bear-off correcto (solo con valor exacto).  
  - Capturas y bloqueos de puntos.  
  - Generación de movimientos válidos (`get_valid_moves`).  

### Cobertura
Se usa el módulo **`coverage`**:
```bash
coverage run -m unittest discover
coverage report -m
```
Y opcionalmente:
```bash
coverage html && xdg-open htmlcov/index.html
```
El objetivo es cubrir principalmente la **lógica de juego**, ya que la interfaz gráfica se prueba manualmente.

---

## 7. Principios SOLID aplicados

- **S - Single Responsibility:**  
  Cada clase tiene una sola responsabilidad (por ejemplo, `Board` solo maneja el tablero).  

- **O - Open/Closed:**  
  El sistema puede extenderse (por ejemplo, agregar una IA o nuevas UIs) sin modificar la lógica principal.  

- **L - Liskov Substitution:**  
  Las clases respetan los contratos: los métodos devuelven los mismos tipos esperados (`bool`, `list`, etc.).  

- **I - Interface Segregation:**  
  Cada clase expone solo los métodos que necesita; la UI no conoce internamente el `Board`.  

- **D - Dependency Inversion:**  
  La interfaz depende de las abstracciones del `Game` y no de sus detalles internos.

---

## 8. Anexo: Guía para diagrama UML

**Relaciones principales (texto guía para el dibujo):**

- `BackgammonGame`
  - **compone** → `Board` y `Dice`
  - **usa** → `Player` x2
- `Board`
  - **contiene** → `Checker` en `points` y `bar`
- `BackgammonUI`
  - **usa** → `BackgammonGame`

**Clases y atributos clave:**
- `BackgammonGame`: `board`, `dice`, `players`, `turn`  
- `Board`: `points`, `bar`, `off`  
- `Checker`: `color`  
- `Dice`: `_last`  
- `Player`: `_color`, `_nombre`  
- `BackgammonUI`: `info_message`, `punto_seleccionado`, `dado_seleccionado`, `game`

---

## 9. Trabajo futuro

- Guardar y cargar partidas.  
- Añadir **sonidos y animaciones** en Pygame.  
- Tests de integración para partidas completas.  
- Excepciones específicas para errores de movimiento.  
- Agregar poder jugar contra el ordenador o una IA

---

## 10. Versionado y evolución del proyecto

Durante el desarrollo se fueron ajustando aspectos clave:
- Estructura de paquetes y ejecución con `-m`.  
- Implementación de la regla del **bear-off exacto**.  
- Bloqueo de movimientos hasta liberar el **bar**.  
- Mensajes visuales de “sin movimientos válidos”.  
- Mejora visual de fichas (base del triángulo, `+n`, off en tiras).  
- Incorporación de pruebas unitarias y medición de cobertura.  

---

## 11. Cómo ejecutar y probar el proyecto

```bash
# Ejecutar interfaz gráfica
python -m pygame_ui.game_pygame

# Ejecutar versión CLI simple
python main.py

# Ejecutar versión CLI con comandos
python CLI.py

# Ejecutar pruebas con coverage
coverage run -m unittest discover
coverage report -m
```