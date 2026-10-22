# =====================================================================
#  CHAPTER 2: THE MANOR
#  ROOM 12: THE SORTING OFFICE
# =====================================================================
#  Parcels are piled to the ceiling of the manor's old post room.
#  A brass sign reads:
#
#    "Deliver nothing until everything is in order."
#
#  WHAT TO DO
#  Finish the four functions below. Each parcel is a tuple:
#
#      (name, weight, city)      for example  ("Clock", 12, "Paris")
#
#  Don't change the list you are given: return a NEW list or dict.
#
#  TOPICS: sorted(), key=, lambda, reverse=True, grouping into a dict
# =====================================================================

PARCELS = [
    ("Clock", 12, "Paris"),
    ("Anvil", 50, "London"),
    ("Letter", 1, "Paris"),
    ("Teapot", 3, "Berlin"),
    ("Globe", 8, "London"),
]


def by_weight(parcels):
    """Return the parcels sorted from lightest to heaviest.

        by_weight(PARCELS)[0] -> ("Letter", 1, "Paris")

    Hint: sorted(parcels, key=lambda p: ...)
    """
    # TODO
    pass


def top_three(parcels):
    """Return the NAMES of the three heaviest parcels, heaviest first.

        top_three(PARCELS) -> ["Anvil", "Clock", "Globe"]
    """
    # TODO
    pass


def by_city_then_name(parcels):
    """Return the parcels sorted by city (A to Z). Parcels going to the
    same city are sorted by name (A to Z).

        by_city_then_name(PARCELS)[0] -> ("Teapot", 3, "Berlin")
    """
    # TODO
    pass


def group_by_city(parcels):
    """Return a dictionary mapping each city to a list of the names of
    the parcels going there, in their original order.

        group_by_city(PARCELS)["Paris"] -> ["Clock", "Letter"]
    """
    groups = {}
    # TODO
    return groups


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print(by_weight(PARCELS))
    print(top_three(PARCELS))          # should print ['Anvil', 'Clock', 'Globe']
    print(by_city_then_name(PARCELS))
    print(group_by_city(PARCELS))
