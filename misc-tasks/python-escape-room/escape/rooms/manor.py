"""Chapter 2: The Manor. Intermediate skills, plus fix-the-bug and write-the-tests rooms."""

MANOR_ROOMS = [
    {
        "id": "room09_archive",
        "title": "The Archive",
        "concept": "Files: open, read, strip, split and write",
        "story": (
            "You escaped the prison, straight into the grounds of a crumbling manor. The front door "
            "slams behind you. In the archive, a dusty ledger sits on a desk next to a note: “Balance "
            "my books and I'll show you the way out.”"
        ),
        "objectives": [
            "Open a file with `with open(...)` and read its lines",
            "Clean each line with .strip() and split it with .split(\",\")",
            "Skip blank lines and # comment lines",
            "Write a report to a new file",
        ],
        "hints": [
            "`with open(filename) as f:` then `for line in f:` gives you one line at a time. "
            "`len(f.readlines())` counts them.",
            "For each line: `line = line.strip()`, then `if not line or line.startswith(\"#\"): continue`. "
            "Then `date, item, amount = [part.strip() for part in line.split(\",\")]` and use `int(amount)`.",
            "Build a dict of totals, then `with open(report_filename, \"w\") as f:` and "
            "`for item in sorted(totals): f.write(f\"{item}: {totals[item]}\\n\")`.",
        ],
        "digit": 5,
    },
    {
        "id": "room10_workshop",
        "title": "The Workshop",
        "concept": "Debugging: find and fix the bugs",
        "story": (
            "A workshop full of half-built clockwork. The previous owner left four machines that "
            "almost work. They run without crashing, but they give the wrong answers. Fix them and "
            "the workshop door will open."
        ),
        "objectives": [
            "Read code carefully and work out what it actually does",
            "Fix an off-by-one error in a loop",
            "Fix a return in the wrong place",
            "Fix a mutable default argument and a broken `or` condition",
        ],
        "hints": [
            "Run each function yourself with the examples in the docstring and compare the answers. "
            "Add `print()` calls inside loops to see what's happening.",
            "`range(1, len(scores))` skips index 0. In all_doors_locked, the `else: return True` "
            "returns after looking at only the first door.",
            "`toolbox=[]` is created once and shared between calls: use `toolbox=None` and "
            "`if toolbox is None: toolbox = []`. And `day == \"Saturday\" or \"Sunday\"` is always "
            "true; write `day == \"Saturday\" or day == \"Sunday\"`.",
        ],
        "digit": 0,
    },
    {
        "id": "room11_greenhouse",
        "title": "The Greenhouse",
        "concept": "List, dict and set comprehensions",
        "story": (
            "A steamy glass greenhouse, overgrown with strange plants. A gardening robot creaks: "
            "“I only understand ONE-LINERS. Speak to me in comprehensions!”"
        ),
        "objectives": [
            "Build a list with a list comprehension",
            "Filter with `if` inside a comprehension",
            "Build a dict with a dict comprehension and a set with a set comprehension",
        ],
        "hints": [
            "A list comprehension: `[n * n for n in numbers]`. Each function body can be a single `return` line.",
            "Filter with if at the end: `[p[\"name\"] for p in plants if p[\"water\"] < 30]`.",
            "Dict: `{p[\"name\"]: p[\"height\"] for p in plants}`. Set: `{p[\"colour\"] for p in plants}`.",
        ],
        "digit": 3,
    },
    {
        "id": "room12_sorting_office",
        "title": "The Sorting Office",
        "concept": "sorted(), key=, lambda and grouping",
        "story": (
            "Parcels are piled to the ceiling of the manor's old post room. A brass sign reads: "
            "“Deliver nothing until everything is in order.”"
        ),
        "objectives": [
            "Sort with `sorted()` and a `key=lambda ...`",
            "Sort in reverse, and by two things at once",
            "Group items into a dict of lists",
            "Leave the original list unchanged",
        ],
        "hints": [
            "Each parcel is a tuple `(name, weight, city)`, so `p[1]` is the weight: "
            "`sorted(parcels, key=lambda p: p[1])`. `sorted` makes a new list; `.sort()` changes the original.",
            "`sorted(..., reverse=True)` puts the heaviest first; then take `[:3]`. To sort by city and "
            "then name, return a tuple from the key: `key=lambda p: (p[2], p[0])`.",
            "For grouping: `groups = {}`, then for each parcel `groups.setdefault(city, []).append(name)`.",
        ],
        "digit": 8,
    },
    {
        "id": "room13_maze",
        "title": "The Maze",
        "concept": "2D lists, nested loops and grid coordinates",
        "story": (
            "Behind the manor is a hedge maze. A gardener's map shows it as rows of characters: "
            "`#` is a hedge, `.` is a path, `S` is the start and `E` is the exit."
        ),
        "objectives": [
            "Loop over rows and columns with nested loops",
            "Use `enumerate()` to get row and column numbers",
            "Check grid boundaries before looking at a cell",
            "Build a new grid without changing the old one",
        ],
        "hints": [
            "`for row in grid:` then `for cell in row:` visits every cell. "
            "`grid[r][c]` is the cell in row r, column c.",
            "`for r, row in enumerate(grid):` and `for c, cell in enumerate(row):` give you the coordinates "
            "to return as `(r, c)`.",
            "For neighbours, check each of `(r - 1, c)`, `(r + 1, c)`, `(r, c - 1)`, `(r, c + 1)` in that order: "
            "keep it if `0 <= nr < len(grid)`, `0 <= nc < len(grid[nr])` and `grid[nr][nc] != \"#\"`.",
        ],
        "digit": 1,
    },
    {
        "id": "room14_hall_of_mirrors",
        "title": "The Hall of Mirrors",
        "concept": "Recursion: base cases and recursive cases",
        "story": (
            "A hall where every mirror reflects another mirror, forever. A voice whispers from every "
            "direction: “To leave, a function must call itself… and know when to stop.”"
        ),
        "objectives": [
            "Write a base case that stops the recursion",
            "Write a recursive case that calls the function on a smaller problem",
            "Recurse into nested lists",
            "Combine the results of two recursive calls",
        ],
        "hints": [
            "Every recursive function starts with the stopping case: `if n == 0: return []`. "
            "Then `return [n] + countdown(n - 1)`.",
            "`sum_digits(1234)` is `4 + sum_digits(123)`: use `n % 10` and `n // 10`. For flatten, loop over the "
            "items; if `isinstance(item, list)`, extend with `flatten(item)`, otherwise append item.",
            "count_paths: if `rows == 1 or cols == 1` there is only 1 path. Otherwise it's "
            "`count_paths(rows - 1, cols) + count_paths(rows, cols - 1)`.",
        ],
        "digit": 9,
    },
    {
        "id": "room15_inspector",
        "title": "The Inspector's Office",
        "concept": "Testing: writing asserts that catch bugs",
        "story": (
            "A stern inspector sits behind a desk piled with forms. “Anyone can write code. "
            "Prove you can TEST it. I have four broken copies of this function. Catch them all.”"
        ),
        "objectives": [
            "Write asserts that check a function's answers",
            "Test codes that should be accepted AND codes that should be rejected",
            "Think about edge cases: wrong length, lowercase, letters where digits should be",
        ],
        "hints": [
            "Use the `is_valid_code` passed into your test function, not one you write yourself. "
            "Each assert looks like `assert is_valid_code(\"AB1234\") == True`.",
            "One broken version rejects everything; another accepts codes of the wrong length. "
            "Try `\"AB12345\"` and `\"AB123\"`.",
            "The other two broken versions accept lowercase letters (`\"ab1234\"`) and only check the "
            "first three digits (`\"AB123X\"`).",
        ],
        "digit": 7,
    },
    {
        "id": "room16_observatory",
        "title": "The Observatory",
        "concept": "Putting it together: files, exceptions, comprehensions and sorting",
        "story": (
            "At the top of the manor's tower is an observatory. The star catalogue is a mess, but "
            "the exit is written in the stars. Clean the data, find the brightest stars, and the "
            "dome will open to the sky."
        ),
        "objectives": [
            "Turn a line of text into a dict",
            "`raise ValueError` for bad data, and catch it when loading",
            "Load a whole file, counting the rows you skip",
            "Use sorting and comprehensions to answer questions about the data",
        ],
        "hints": [
            "In parse_row: `parts = [p.strip() for p in line.split(\",\")]`. If `len(parts) != 4`, "
            "`raise ValueError(\"wrong number of fields\")`. `float(\"bright\")` raises ValueError by itself.",
            "In load_stars, wrap the call: `try: stars.append(parse_row(line))` "
            "`except ValueError: skipped += 1`. Return `stars, skipped`.",
            "Brightest means LOWEST magnitude: `sorted(stars, key=lambda s: s[\"magnitude\"])[:n]`. For "
            "stars_in, filter with a comprehension, then sort by `\"distance\"`.",
        ],
        "digit": 2,
    },
]
