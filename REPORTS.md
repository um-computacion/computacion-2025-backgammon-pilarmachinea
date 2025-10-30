# Automated Reports

## Coverage Report
```text
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
cli/CLI.py                 169      1    99%   216
core/BackgammonGame.py     103     13    87%   22, 29, 84, 91, 120, 129, 135-138, 146-148, 154, 156
core/Board.py              109     14    87%   34, 56, 69, 78-89, 127, 138
core/Checker.py              5      0   100%
core/Dice.py                13      0   100%
core/Player.py              16      0   100%
------------------------------------------------------
TOTAL                      415     28    93%

```

## Pylint Report
```text
************* Module computacion-2025-backgammon-pilarmachinea.core.BackgammonGame
core/BackgammonGame.py:120:15: E1101: Instance of 'Board' has no 'get_valid_moves' member (no-member)
************* Module computacion-2025-backgammon-pilarmachinea.core.Board
core/Board.py:68:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
core/Board.py:95:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
core/Board.py:113:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
core/Board.py:137:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
************* Module computacion-2025-backgammon-pilarmachinea.core.Checker
core/Checker.py:1:0: R0903: Too few public methods (1/2) (too-few-public-methods)

------------------------------------------------------------------
Your code has been rated at 9.74/10 (previous run: 9.74/10, +0.00)


```
