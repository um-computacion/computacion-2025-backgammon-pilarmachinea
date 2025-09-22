# Justificación
## Resumen del diseño general
El proyecto implementa una versión simplificada del juego Backgammon utilizando **Programación Orientada a Objetos (POO)** en Python.  
El diseño se basa en separar las responsabilidades en clases individuales, manteniendo la lógica del juego modular, testeable y fácil de extender.  

## Justificación de las clases elegidas
- Board: Representa el tablero. Su responsabilidad es administrar las posiciones, fichas y movimientos válidos.  
- Checker: Modela las fichas individuales. Se decidió separarlas para poder manipularlas de manera independiente y reutilizable.  
- Dice: Encapsula la lógica de lanzar los dados. Esto facilita pruebas y evita duplicar lógica aleatoria en otras partes del código.  
- Player: Contiene los datos de cada jugador (nombre, fichas asignadas, color). Se justifica su existencia para desacoplar la lógica del tablero de la información de los jugadores.  
- BackgammonGame: Clase principal que coordina la interacción entre jugadores, tablero y dados. Administra turnos y estado general de la partida.

## Justificación de atributos
- `Board.positions`: lista/estructura que representa los puntos del tablero → necesaria para validar y actualizar jugadas.  
- `Checker.color` / `Checker.owner`: permiten distinguir las fichas por jugador → soporte directo a las reglas del juego.  
- `Dice.values`: guarda los valores del último lanzamiento → usado para verificar jugadas válidas.  
- `Player.name` y `Player.checkers`: mantienen la identidad del jugador y las fichas que controla.  
Se priorizó la simplicidad, manteniendo únicamente los atributos mínimos necesarios para cumplir los requisitos.

## Decisiones de diseño relevantes
- Separación de responsabilidades en múltiples clases (principio de Single Responsibility).  
- Uso de una clase central (`BackgammonGame`) para aplicar el patrón Mediator, coordinando entidades sin que se acoplen directamente.  
- Organización del proyecto en carpetas `core/` y `tests/` para mantener escalabilidad.  
- Uso de `.gitignore` para evitar archivos innecesarios en el repo.  

## Excepciones y manejo de errores
- Se definieron excepciones personalizadas como `InvalidMoveError` (movimientos inválidos) y `NotYourTurnError` (jugador intenta mover fuera de turno).  
- Esto mejora la claridad de la lógica y facilita testing de casos de error.  
- Se eligió usar excepciones personalizadas en lugar de `ValueError` o `RuntimeError` genéricas, para tener mensajes claros y diferenciados.

## Estrategias de testing y cobertura
- Se implementaron tests unitarios con **pytest** que cubren:  
  - Creación de tablero y jugadores.  
  - Lanzamiento de dados y validación de valores.  
  - Reglas básicas de movimiento.  
- Estrategia: pruebas de **unidad** para cada clase y pruebas de **integración** para la clase `BackgammonGame`.  
- El objetivo fue alcanzar **>90% de cobertura**, garantizando robustez del diseño y cumplimiento de requisitos.

## Referencias a requisitos SOLID
- Single Responsibility: cada clase tiene una única responsabilidad clara.  
- Open/Closed: el diseño permite extender nuevas reglas de movimiento sin modificar las clases base.  
- Liskov Substitution: las clases son sustituibles y cumplen contratos de comportamiento (ej. `Checker` siempre se puede usar como ficha sin romper el tablero).  
- Interface Segregation: se evitó recargar clases con métodos innecesarios, cada una expone solo lo necesario.  
- Dependency Inversion: la clase principal `BackgammonGame` depende de abstracciones (métodos públicos de `Board`, `Player`, `Dice`), no de implementaciones internas.
