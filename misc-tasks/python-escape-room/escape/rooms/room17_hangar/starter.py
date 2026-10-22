# =====================================================================
#  CHAPTER 3: THE AIRSHIP
#  ROOM 17: THE HANGAR
# =====================================================================
#  You climb out of the observatory dome onto the deck of an airship
#  moored to the tower. Before you can blink, it casts off! In the
#  hangar, robot parts lie on the floor next to a blueprint:
#
#    "Build me, and I'll fly you home."
#
#  WHAT TO DO
#  Finish the Robot class below. A class is a blueprint: every Robot
#  object made from it gets its own name, battery and position.
#
#      r2 = Robot("R2")       # calls __init__ to set up a new robot
#      r2.move(3)             # calls the move method on that robot
#      print(r2.battery)      # reads one of its attributes
#
#  TOPICS: class, __init__, self, attributes, methods
# =====================================================================


class Robot:
    def __init__(self, name, battery=100):
        """Set up a new robot. Store three attributes on self:
            name      the name given
            battery   the battery given (100 if none is given)
            position  always starts at 0
        """
        # TODO: self.name = name   ...and the other two
        pass

    def move(self, steps):
        """Each step forward uses 10 battery.
        If there is enough battery for ALL the steps: add steps to the
        position, use the battery and return True.
        Otherwise don't move at all, and return False.
        """
        # TODO
        pass

    def recharge(self, amount):
        """Add amount to the battery, but it can never go above 100."""
        # TODO
        pass

    def status(self):
        """Return a string like:  "R2 is at 3 with 70% battery" """
        # TODO
        pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    r2 = Robot("R2")
    print(r2.move(3))      # should print True
    print(r2.status())     # should print R2 is at 3 with 70% battery
    print(r2.move(8))      # should print False (not enough battery)
    r2.recharge(50)
    print(r2.battery)      # should print 100
