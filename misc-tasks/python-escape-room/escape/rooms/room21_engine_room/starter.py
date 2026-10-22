# =====================================================================
#  CHAPTER 3: THE AIRSHIP
#  ROOM 21: THE ENGINE ROOM
# =====================================================================
#  The engine room roars with heat. Two engines are dead: a steam
#  engine and an electric one. The chief engineer's notes say both are
#  kinds of Engine, if only someone would write them.
#
#  WHAT TO DO
#  The Engine class is done for you. Write two SUBCLASSES of Engine:
#
#    class SteamEngine(Engine):      <- the (Engine) means "inherits from"
#
#  A subclass gets every method of its parent for free (start and
#  describe), and can OVERRIDE methods to behave differently (kind and
#  power). Don't copy start or describe into your subclasses!
#
#  TOPICS: inheritance, super().__init__(), overriding, polymorphism
# =====================================================================


class Engine:
    def __init__(self, name):
        self.name = name
        self.running = False

    def start(self):
        self.running = True

    def kind(self):
        return "engine"

    def power(self):
        return 0

    def describe(self):
        return f"{self.name} ({self.kind()})"


# TODO: Write class SteamEngine, which inherits from Engine.
#   __init__(self, name, pressure)
#       call super().__init__(name), then store pressure
#   kind()  returns "steam"
#   power() returns pressure * 2 when running, otherwise 0
#
#       boiler = SteamEngine("Boiler", 40)
#       boiler.describe()  -> "Boiler (steam)"
#       boiler.start()
#       boiler.power()     -> 80


# TODO: Write class ElectricEngine, which inherits from Engine.
#   __init__(self, name, cells)
#       call super().__init__(name), then store cells
#   kind()  returns "electric"
#   power() returns cells * 5 when running, otherwise 0


def total_power(engines):
    """Return the total power of a list of engines (any kind!).

        total_power([boiler, dynamo]) -> boiler.power() + dynamo.power()
    """
    # TODO
    pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    boiler = SteamEngine("Boiler", 40)
    print(boiler.describe())   # should print Boiler (steam)
    boiler.start()
    print(boiler.power())      # should print 80
