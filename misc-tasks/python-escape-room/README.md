# Python Escape Room

A Python revision game. Students are locked in a series of rooms, and each
door opens only when their code passes its checks. The game runs in the
browser, and students write their code in ordinary `.py` files in any editor.

## Playing (students)

1. Install Python 3.8 or newer. Nothing else is needed.
2. Open a terminal in this folder and run:

   ```
   python play.py
   ```

   (On some Macs, use `python3 play.py`.) The game opens in your browser.
3. Open the file shown on the page (for example `solutions/room01_cell.py`)
   in VS Code, IDLE, Thonny, PyCharm or any other editor.
4. Complete the TODOs and **save**. The page checks your code every time you
   save and shows what passed, what failed and why.
5. Pass every check to open the door. You'll get a digit of the escape code,
   and the next room's file appears in `solutions/`.

A hint unlocks after every 2 saves that don't pass yet. Keep the terminal
window open while you play, and press Ctrl+C to save and quit.

### Saving and moving your game

Everything is saved **inside this folder**:

- `solutions/`: your code, one file per room
- `solutions/backups/`: your old code whenever you use "Reset room"
- `progress.json`: rooms solved, attempts, hints and time

To carry on at home or on another computer, copy the whole folder.

## The rooms

The game has three chapters of 8 rooms. Each chapter has its own escape code
and victory screen, and finishing a chapter unlocks the next one.

**Chapter 1: The Prison** (fundamentals)

| # | Room | Topic |
|---|------|-------|
| 1 | The Cell | variables, data types, print, f-strings |
| 2 | The Keypad | arithmetic operators, if / elif / else |
| 3 | The Lever Hall | for and while loops, range() |
| 4 | The Library | strings: slicing, split, upper, lower |
| 5 | The Laboratory | lists: indexing, len, append, sum |
| 6 | The Vault | dictionaries: .get(), .items() |
| 7 | The Clock Tower | writing functions, parameters, defaults |
| 8 | The Final Door | Caesar cipher with try / except |

**Chapter 2: The Manor** (intermediate skills)

| # | Room | Topic |
|---|------|-------|
| 9 | The Archive | reading and writing files |
| 10 | The Workshop | **fix the bugs**: four planted bugs in working-looking code |
| 11 | The Greenhouse | list, dict and set comprehensions (loops not allowed) |
| 12 | The Sorting Office | sorted(), key=, lambda, grouping |
| 13 | The Maze | 2D grids, nested loops, enumerate() |
| 14 | The Hall of Mirrors | recursion (checked: the function must call itself) |
| 15 | The Inspector's Office | **write the tests**: asserts must catch 4 broken versions |
| 16 | The Observatory | finale: files, raise / except, sorting, comprehensions |

**Chapter 3: The Airship** (classes and object-oriented programming)

| # | Room | Topic |
|---|------|-------|
| 17 | The Hangar | first class: __init__, attributes, methods |
| 18 | The Crew Lockers | object state, raising ValueError |
| 19 | The Gallery | __str__, __repr__, __eq__, __lt__ |
| 20 | The Crew Quarters | composition: objects holding objects, __len__ |
| 21 | The Engine Room | inheritance, super(), overriding, polymorphism |
| 22 | The Signal Tower | class attributes, @staticmethod, @classmethod |
| 23 | The Balloon Deck | @property, setters, private attributes |
| 24 | The Bridge | finale: custom exceptions, inheritance, composition |
