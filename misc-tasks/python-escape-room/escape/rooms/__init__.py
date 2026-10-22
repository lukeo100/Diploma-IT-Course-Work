"""The rooms, grouped into chapters, in the order students play them.

To add a room: make a folder here named after its id containing
  starter.py  the code students start with (copied into solutions/)
  tests.py    test_... functions that check it (see escape/testkit.py)
  files/      optional data files, copied into solutions/ next to the starter
then add an entry to a chapter's room list. Use `backticks` in hints for code.
"""
from pathlib import Path

from .manor import MANOR_ROOMS
from .airship import AIRSHIP_ROOMS

ROOMS_DIR = Path(__file__).resolve().parent

PRISON_ROOMS = [
    {
        "id": "room01_cell",
        "title": "The Cell",
        "concept": "Variables, data types, print and f-strings",
        "story": (
            "You wake on a cold stone floor in a locked cell. Scratched into the wall is a note "
            "from the last prisoner: “The door only listens to Python. Tell it who you are "
            "and where you are, and it will let you out.”"
        ),
        "objectives": [
            "Store values in variables with the right type: str, int, float and bool",
            "Calculate a value with +",
            "Build a message with an f-string",
            "print() the message",
        ],
        "hints": [
            "Text (a str) goes inside quotes: `prisoner_name = \"Alex\"`. Numbers don't: `cell_number = 13`.",
            "A float has a decimal point, like `0.25`. A bool is `True` or `False`, with a capital letter and no quotes.",
            "Put an f before the quote and variables inside curly braces: "
            "`f\"Prisoner {prisoner_name} is in cell {cell_number}\"`. Then `print(door_message)`.",
        ],
        "digit": 4,
    },
    {
        "id": "room02_keypad",
        "title": "The Keypad",
        "concept": "Arithmetic operators and if / elif / else",
        "story": (
            "The cell door creaks open into a corridor. At the far end is a steel door with a "
            "glowing keypad. A screen above it flickers: “ANSWER MY THREE QUESTIONS.”"
        ),
        "objectives": [
            "Use // and % to split seconds into minutes and seconds",
            "Use if / elif / else to compare a guess with the PIN",
            "Pick an answer based on a range of numbers",
            "return your answers (don't just print them)",
        ],
        "hints": [
            "`125 // 60` is `2` (whole minutes). `125 % 60` is `5` (the seconds left over).",
            "Check for the correct PIN first with `==`. Then `elif guess < 4321:` means too low. "
            "Anything else must be too high.",
            "For alarm_level: `if wrong_guesses == 0:` return `\"green\"`, `elif wrong_guesses <= 2:` "
            "return `\"amber\"`, `else:` return `\"red\"`.",
        ],
        "digit": 7,
    },
    {
        "id": "room03_lever_hall",
        "title": "The Lever Hall",
        "concept": "for loops, while loops and range()",
        "story": (
            "Beyond the keypad door is a long hall lined with rusty levers. A sign reads: "
            "“Only those who can count without tiring may pass.”"
        ),
        "objectives": [
            "Add up numbers with a for loop and range()",
            "Repeat with a while loop until a condition is met",
            "Count matches inside a loop using %",
        ],
        "hints": [
            "`range(1, n + 1)` gives 1, 2, …, n. Inside the loop add each number: `total += number`.",
            "`while weight > 0:` then halve it with `weight = weight // 2` and add 1 to `pulls`.",
            "Loop over `range(start, stop + 1)` and count the numbers where `number % k == 0`.",
        ],
        "digit": 1,
    },
    {
        "id": "room04_library",
        "title": "The Library",
        "concept": "Strings: slicing, split, upper and lower",
        "story": (
            "You stumble into a dusty library. Every title on the book spines is backwards, and a "
            "ghostly librarian blocks the exit: “Read my books properly and I'll let you leave.”"
        ),
        "objectives": [
            "Reverse a string with slicing",
            "Split a sentence into words and build a new string",
            "Clean up text with .lower() and .replace() before comparing it",
        ],
        "hints": [
            "`text[::-1]` is a slice that steps backwards through the whole string.",
            "Loop over `sentence.split()`. `word[0]` is the first letter of a word. Add it to a result "
            "string, then `return result.upper()`.",
            "Clean the phrase first: `cleaned = phrase.lower().replace(\" \", \"\")`. "
            "Then return `cleaned == cleaned[::-1]`.",
        ],
        "digit": 9,
    },
    {
        "id": "room05_laboratory",
        "title": "The Laboratory",
        "concept": "Lists: indexing, len, append and sum",
        "story": (
            "A laboratory full of bubbling vials. A robot arm lowers a tray: “Sort my shelves "
            "and find the missing test tube, and the exit hatch will open.”"
        ),
        "objectives": [
            "Use len() and an index to find the middle item",
            "Build a new list with a loop and .append()",
            "Find a missing number using sum() or a loop",
        ],
        "hints": [
            "For a list of 5 items the middle index is 2, which is `len(shelf) // 2`. Return `shelf[middle]`.",
            "Start with `good = []`. Loop over `vials` and `good.append(vial)` when `vial != \"broken\"`. "
            "Don't use .remove() on the original list!",
            "The tubes should be 1 to `len(numbers) + 1`, which add up to `sum(range(1, len(numbers) + 2))`. "
            "The missing tube is that total minus `sum(numbers)`.",
        ],
        "digit": 3,
    },
    {
        "id": "room06_vault",
        "title": "The Vault",
        "concept": "Dictionaries: keys, values, .get() and .items()",
        "story": (
            "The hatch drops you into a bank vault stacked with treasure. A voice booms from the "
            "darkness: “Count my treasure correctly, or stay here forever.”"
        ),
        "objectives": [
            "Count things using a dictionary",
            "Look up values safely with .get() and a default",
            "Loop over a dictionary's keys and values with .items()",
        ],
        "hints": [
            "Start with `counts = {}`. For each item: `counts[item] = counts.get(item, 0) + 1`.",
            "`for item, quantity in inventory.items():` then add `quantity * prices.get(item, 0)` to a total.",
            "Keep the best name and best price so far while you loop over `prices.items()`. "
            "Start with `best_name = None` so an empty dict returns None.",
        ],
        "digit": 8,
    },
    {
        "id": "room07_clock_tower",
        "title": "The Clock Tower",
        "concept": "Writing functions: parameters, return values and defaults",
        "story": (
            "A spiral staircase leads up into the clock tower. Giant gears grind overhead. The tower "
            "door opens only when the clock is set and the bell rings at the right hour."
        ),
        "objectives": [
            "Write functions that take parameters and return results",
            "Use % to wrap numbers around a clock",
            "Write a whole function yourself, including a default parameter value",
        ],
        "hints": [
            "12 is the special case: 12 AM is `0` and 12 PM is `12`. For any other hour, PM adds 12.",
            "Turn everything into minutes: `total = hour * 60 + minute + extra`. "
            "Then `(total // 60) % 24` is the hour and `total % 60` is the minute.",
            "Start with `def chime(hour, sound=\"BONG\"):`. `strikes = hour % 12`, but if that's 0 it should be 12. "
            "`\" \".join([sound] * strikes)` builds the answer.",
        ],
        "digit": 2,
    },
    {
        "id": "room08_final_door",
        "title": "The Final Door",
        "concept": "Putting it together: strings, loops, functions and try / except",
        "story": (
            "The last door. It's covered in scrambled letters and has a dial you can turn. An "
            "inscription reads: “Only a true Pythonista can decode my message. Turn the dial "
            "wisely: a bad dial must never break you.”"
        ),
        "objectives": [
            "Shift letters along the alphabet with ord(), chr() and %",
            "Loop over a string to build a new one",
            "Handle bad input with try / except instead of crashing",
            "Combine your functions to unlock the door",
        ],
        "hints": [
            "For a lowercase letter: `position = ord(letter) - ord(\"a\")`, then "
            "`chr(ord(\"a\") + (position + shift) % 26)`. Do the same with `\"A\"` when `letter.isupper()`.",
            "In read_dial: `try:` `return int(value)` `except ValueError:` `return None`.",
            "In unlock: `shift = read_dial(dial)`. If `shift is None` return `\"DIAL ERROR\"`, "
            "otherwise return `caesar(message, -shift)`.",
        ],
        "digit": 6,
    },
]

CHAPTERS = [
    {
        "id": "prison",
        "title": "The Prison",
        "topics": "Python fundamentals",
        "rooms": PRISON_ROOMS,
    },
    {
        "id": "manor",
        "title": "The Manor",
        "topics": "Files, comprehensions, sorting, recursion, debugging and testing",
        "rooms": MANOR_ROOMS,
    },
    {
        "id": "airship",
        "title": "The Airship",
        "topics": "Classes and object-oriented programming",
        "rooms": AIRSHIP_ROOMS,
    },
]

for _chapter in CHAPTERS:
    for _room in _chapter["rooms"]:
        _room["chapter"] = _chapter["id"]

ROOMS = [room for chapter in CHAPTERS for room in chapter["rooms"]]
ROOM_IDS = [room["id"] for room in ROOMS]


def starter_path(rid):
    return ROOMS_DIR / rid / "starter.py"


def data_files(rid):
    """The data files that go into solutions/ along with a room's starter."""
    folder = ROOMS_DIR / rid / "files"
    return sorted(p for p in folder.iterdir() if p.is_file()) if folder.is_dir() else []
