"""Chapter 3: The Airship. Classes and object-oriented programming."""

AIRSHIP_ROOMS = [
    {
        "id": "room17_hangar",
        "title": "The Hangar",
        "concept": "Your first class: __init__, attributes and methods",
        "story": (
            "You climb out of the observatory dome and onto the deck of an airship moored to the "
            "tower. Before you can blink, it casts off. In the hangar, a pile of robot parts lies on "
            "the floor with a blueprint: “Build me, and I'll fly you home.”"
        ),
        "objectives": [
            "Write a class with an `__init__` method",
            "Store attributes on `self`, including a default value",
            "Write methods that use and change the object's attributes",
            "Make two objects that don't share their data",
        ],
        "hints": [
            "Inside `__init__`, store each value on self: `self.name = name`, `self.battery = battery`, "
            "`self.position = 0`.",
            "In move: `cost = steps * 10`. `if cost > self.battery: return False`. Otherwise change "
            "`self.position` and `self.battery`, then `return True`.",
            "In recharge: `self.battery = min(100, self.battery + amount)`. status() returns "
            "`f\"{self.name} is at {self.position} with {self.battery}% battery\"`.",
        ],
        "digit": 2,
    },
    {
        "id": "room18_lockers",
        "title": "The Crew Lockers",
        "concept": "Objects that protect their own state, and raising errors",
        "story": (
            "A corridor of brass crew lockers. Yours has a keypad and a coin slot. A label warns: "
            "“A good locker never lets anyone cheat, not even you.”"
        ),
        "objectives": [
            "Keep track of an object's state (locked or unlocked)",
            "Return True or False to show whether an action worked",
            "`raise ValueError` when a method gets bad input",
        ],
        "hints": [
            "Start with `self.coins = 0` and `self.locked = True` in `__init__`. unlock sets "
            "`self.locked = False` only when the pin matches.",
            "In deposit and withdraw, check `if self.locked: return False` first.",
            "Then check the amount: `if amount <= 0: raise ValueError(\"amount must be positive\")`. "
            "withdraw also needs `if amount > self.coins: raise ValueError(...)`.",
        ],
        "digit": 6,
    },
    {
        "id": "room19_gallery",
        "title": "The Gallery",
        "concept": "Special methods: __str__, __repr__, __eq__ and __lt__",
        "story": (
            "The captain's private gallery. The paintings are all jumbled up, and a parrot squawks: "
            "“Name them! Compare them! SORT THEM!”"
        ),
        "objectives": [
            "Control what `print()` shows with `__str__`",
            "Write a developer-friendly `__repr__`",
            "Decide when two objects are equal with `__eq__`",
            "Make objects sortable with `__lt__`",
        ],
        "hints": [
            "`__str__` and `__repr__` must RETURN a string. For repr, `{self.title!r}` adds the quotes for you.",
            "`__eq__(self, other)` returns `self.title == other.title and self.artist == other.artist`.",
            "`sorted()` uses `<`, which calls `__lt__(self, other)`. Return `self.year < other.year`.",
        ],
        "digit": 4,
    },
    {
        "id": "room20_crew_quarters",
        "title": "The Crew Quarters",
        "concept": "Composition: objects that contain other objects",
        "story": (
            "Hammocks swing in the crew quarters. The ship's log is missing its crew list, and the "
            "airship won't take orders from a crew it doesn't know."
        ),
        "objectives": [
            "Store a list of objects inside another object",
            "Search the list for an object by one of its attributes",
            "Calculate totals and averages across the objects",
            "Use `__len__` so `len()` works on your object",
        ],
        "hints": [
            "Crew's `__init__` sets `self.members = []`. add() appends a CrewMember, after checking that "
            "no existing member has the same name.",
            "find() loops over `self.members` and returns the member whose `.name` matches, or None at the end.",
            "average_skill: if there are no members return 0.0, otherwise "
            "`sum(m.skill for m in self.members) / len(self.members)`. `__len__` returns `len(self.members)`.",
        ],
        "digit": 0,
    },
    {
        "id": "room21_engine_room",
        "title": "The Engine Room",
        "concept": "Inheritance: subclasses, super() and overriding",
        "story": (
            "The engine room roars with heat. Two engines are dead: a steam engine and an electric "
            "one. The chief engineer's notes say both are kinds of Engine, if only someone would "
            "write them."
        ),
        "objectives": [
            "Write a subclass that inherits from another class",
            "Call the parent's `__init__` with `super().__init__(...)`",
            "Override methods to change behaviour",
            "Use polymorphism: one loop that works for every kind of engine",
        ],
        "hints": [
            "`class SteamEngine(Engine):` then in `__init__`: `super().__init__(name)` and "
            "`self.pressure = pressure`.",
            "Override `kind()` to return `\"steam\"` and `power()` to return `self.pressure * 2` if "
            "`self.running`, otherwise 0. describe() and start() are inherited for free.",
            "total_power just adds up `engine.power()` for every engine: it doesn't need to know which kind each one is.",
        ],
        "digit": 9,
    },
    {
        "id": "room22_signal_tower",
        "title": "The Signal Tower",
        "concept": "Class attributes, @classmethod and @staticmethod",
        "story": (
            "High on the mast is the signal tower. To call for help you need to send signals, but "
            "the machine also keeps count of every signal ever made, and it only reads them in one format."
        ),
        "objectives": [
            "Use a class attribute shared by every object",
            "Write a `@staticmethod` that doesn't need `self`",
            "Write a `@classmethod` that builds an object another way",
        ],
        "hints": [
            "`count = 0` and `MAX_STRENGTH = 10` go directly inside the class, not in `__init__`. "
            "In `__init__`, do `Signal.count += 1`.",
            "`@staticmethod` goes on the line above `def is_valid_code(code):`, with no self. Return "
            "`len(code) == 3 and code.isalpha() and code.isupper()`.",
            "`@classmethod` then `def from_string(cls, text):` then `code, strength = text.split(\":\")` and "
            "`return cls(code, int(strength))`.",
        ],
        "digit": 5,
    },
    {
        "id": "room23_balloon_deck",
        "title": "The Balloon Deck",
        "concept": "Properties: @property, setters and private attributes",
        "story": (
            "Up on the balloon deck, the altitude controls are dangerously loose. Anyone could set the "
            "airship to fly underground. Lock them down so only safe values get through."
        ),
        "objectives": [
            "Hide an attribute behind a leading underscore",
            "Read it through a `@property`",
            "Check new values in a `.setter` and raise ValueError",
            "Make a read-only calculated property",
        ],
        "hints": [
            "Store the real value in `self._altitude`. In `__init__`, write `self.altitude = altitude` "
            "so the setter checks the starting value too.",
            "`@property` above `def altitude(self): return self._altitude`, then "
            "`@altitude.setter` above `def altitude(self, value):`.",
            "In the setter: `if value < 0 or value > 10000: raise ValueError(...)`, then `self._altitude = value`. "
            "altitude_km is a property with no setter: `return self._altitude / 1000`.",
        ],
        "digit": 1,
    },
    {
        "id": "room24_bridge",
        "title": "The Bridge",
        "concept": "Putting it together: classes, inheritance, special methods and custom exceptions",
        "story": (
            "The bridge, at last. The captain's chair is empty and home is on the horizon. Plot a "
            "safe route, and don't let the airship try a leg it can't fly."
        ),
        "objectives": [
            "Write your own exception class",
            "Use inheritance to make a special kind of Waypoint",
            "Build a Route out of Waypoint objects",
            "Raise your custom exception when a route is unsafe",
        ],
        "hints": [
            "A custom exception is one line: `class NavigationError(Exception): pass`. distance_to uses "
            "`math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)`.",
            "Port's `__init__` calls `super().__init__(name, x, y)` and stores has_fuel. Its `__str__` can "
            "build on the parent's: `super().__str__() + \" [fuel]\"`.",
            "Loop over pairs of neighbouring waypoints with `for a, b in zip(self.waypoints, self.waypoints[1:]):`. "
            "Add up `a.distance_to(b)`, or `raise NavigationError(...)` if a leg is too long.",
        ],
        "digit": 3,
    },
]
