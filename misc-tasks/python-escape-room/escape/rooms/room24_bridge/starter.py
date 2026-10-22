# =====================================================================
#  CHAPTER 3: THE AIRSHIP
#  ROOM 24: THE BRIDGE                               (final room!)
# =====================================================================
#  The bridge, at last. The captain's chair is empty and home is on the
#  horizon. Plot a safe route, and don't let the airship try a leg it
#  can't fly.
#
#  WHAT TO DO
#  Write everything below. This room uses everything from this chapter:
#  classes, inheritance, special methods and your own exception.
#
#  TOPICS: custom exceptions, inheritance, composition, special methods
# =====================================================================
import math


# TODO: Write a custom exception class called NavigationError that
#       inherits from Exception. (The body can just be: pass)


class Waypoint:
    def __init__(self, name, x, y):
        """Store name, x and y."""
        # TODO
        pass

    def distance_to(self, other):
        """Return the straight-line distance to another waypoint, as a float.

            Waypoint("A", 0, 0).distance_to(Waypoint("B", 3, 4)) -> 5.0

        Hint: math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        """
        # TODO
        pass

    def __str__(self):
        """Like: Home (1, 2)"""
        # TODO
        pass


# TODO: Write class Port, a subclass of Waypoint.
#   __init__(self, name, x, y, has_fuel=True)
#       use super().__init__ for name, x and y, then store has_fuel
#   __str__ is the same as a Waypoint's, plus " [fuel]" if it has fuel:
#       str(Port("Dock", 0, 0))         -> "Dock (0, 0) [fuel]"
#       str(Port("Dock", 0, 0, False))  -> "Dock (0, 0)"


class Route:
    def __init__(self):
        """Start with an empty list called waypoints."""
        # TODO
        pass

    def add(self, waypoint):
        """Add a waypoint (or Port) to the end of the route. If a waypoint
        with the same NAME is already on the route, raise NavigationError."""
        # TODO
        pass

    def __len__(self):
        """len(route) is the number of waypoints."""
        # TODO
        pass

    def total_distance(self):
        """Add up the distance of every leg (from each waypoint to the
        next). A route with fewer than 2 waypoints has distance 0."""
        # TODO
        pass

    def check_range(self, max_leg):
        """If any leg is longer than max_leg, raise NavigationError with a
        message naming the two waypoints. Otherwise return True."""
        # TODO
        pass

    def fuel_stops(self):
        """Return the NAMES of the Ports on the route that have fuel.
        (Plain Waypoints never have fuel.) Hint: isinstance()"""
        # TODO
        pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    route = Route()
    route.add(Port("Tower", 0, 0))
    route.add(Waypoint("Cloud", 3, 4))
    route.add(Port("Home", 3, 10))
    print(len(route))                # should print 3
    print(route.total_distance())    # should print 11.0
    print(route.fuel_stops())        # should print ['Tower', 'Home']
    try:
        route.check_range(5.5)
    except NavigationError as error:
        print("Unsafe:", error)
