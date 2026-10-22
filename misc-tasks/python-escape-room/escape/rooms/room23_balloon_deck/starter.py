# =====================================================================
#  CHAPTER 3: THE AIRSHIP
#  ROOM 23: THE BALLOON DECK
# =====================================================================
#  Up on the balloon deck, the altitude controls are dangerously loose.
#  Anyone could set the airship to fly underground! Lock them down so
#  only safe values get through.
#
#  WHAT TO DO
#  Finish the Balloon class. A PROPERTY looks like a normal attribute
#  from outside (balloon.altitude = 500), but runs your method behind
#  the scenes, so you can check the value first:
#
#      @property                   runs when you READ balloon.altitude
#      def altitude(self): ...
#
#      @altitude.setter            runs when you SET balloon.altitude = ...
#      def altitude(self, value): ...
#
#  The real value is kept in self._altitude. The underscore means
#  "private: don't touch this from outside the class".
#
#  TOPICS: @property, setters, private attributes, read-only properties
# =====================================================================


class Balloon:
    def __init__(self, name, altitude=0):
        self.name = name
        # TODO: set self.altitude = altitude, so the setter checks it too

    # TODO: an altitude property that returns self._altitude

    # TODO: an altitude setter. If value is below 0 or above 10000,
    #       raise ValueError. Otherwise store it in self._altitude.

    # TODO: a read-only property called altitude_km that returns the
    #       altitude in kilometres (altitude / 1000). No setter!

    def climb(self, metres):
        """Go up by metres. Going too high must raise ValueError
        (and leave the altitude as it was)."""
        # TODO: use self.altitude, so the setter does the checking
        pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    balloon = Balloon("Hope", 1500)
    print(balloon.altitude)      # should print 1500
    print(balloon.altitude_km)   # should print 1.5
    balloon.climb(500)
    print(balloon.altitude)      # should print 2000
    try:
        balloon.altitude = -10
    except ValueError:
        print("Refused! Still at", balloon.altitude)
