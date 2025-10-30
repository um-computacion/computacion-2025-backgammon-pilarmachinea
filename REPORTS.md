# Automated Reports

## Coverage Report
```text
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
cli/__init__.py                    7      0   100%
core/BackgammonGame.py           103     13    87%   22, 29, 84, 91, 120, 129, 135-138, 146-148, 154, 156
core/Board.py                    109     14    87%   34, 56, 69, 78-89, 127, 138
core/Checker.py                    5      0   100%
core/Dice.py                      13      0   100%
core/Player.py                    16      0   100%
core/__init__.py                   0      0   100%
pygame_ui/PygameUI.py            448    405    10%   43-54, 66-92, 96-126, 130, 135, 140-160, 164-198, 204-316, 321-346, 350-408, 412-424, 428-467, 471-557, 561-671, 674-678, 682
pygame_ui/__init__.py              0      0   100%
tests/__init__.py                  0      0   100%
tests/test_backgammongame.py     163      4    98%   66, 147-148, 235
tests/test_board.py              162      1    99%   229
tests/test_checker.py              8      1    88%   10
tests/test_dice.py                36      1    97%   50
tests/test_player.py              49      1    98%   68
------------------------------------------------------------
TOTAL                           1119    440    61%

```

## Pylint Report
```text
************* Module computacion-2025-backgammon-pilarmachinea.main
main.py:19:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:23:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:28:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:36:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:46:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:49:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:59:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:73:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:75:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:86:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:90:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:92:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:100:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:116:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:121:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:123:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:133:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:139:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:148:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:159:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:164:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:167:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:169:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:174:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:176:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:181:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:189:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:193:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:197:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:208:0: C0303: Trailing whitespace (trailing-whitespace)
main.py:227:0: C0304: Final newline missing (missing-final-newline)
main.py:7:0: E0401: Unable to import 'core.BackgammonGame' (import-error)
main.py:12:4: C0415: Import outside toplevel (os) (import-outside-toplevel)
main.py:25:4: C0104: Disallowed name "bar" (disallowed-name)
main.py:141:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
main.py:178:11: R1714: Consider merging these comparisons with 'in' by using 'comando in ('q', 'quit')'. Use a set instead if elements are hashable. (consider-using-in)
main.py:182:13: R1714: Consider merging these comparisons with 'in' by using 'comando in ('r', 'roll')'. Use a set instead if elements are hashable. (consider-using-in)
main.py:194:13: R1714: Consider merging these comparisons with 'in' by using 'comando in ('v', 'ver')'. Use a set instead if elements are hashable. (consider-using-in)
main.py:198:13: R1714: Consider merging these comparisons with 'in' by using 'comando in ('t', 'terminar')'. Use a set instead if elements are hashable. (consider-using-in)
main.py:220:11: W0718: Catching too general exception Exception (broad-exception-caught)
main.py:222:8: C0415: Import outside toplevel (traceback) (import-outside-toplevel)

-----------------------------------
Your code has been rated at 6.90/10


```
