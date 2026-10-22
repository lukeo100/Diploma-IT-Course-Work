# =====================================================================
#  ROOM 5: THE LABORATORY
# =====================================================================
#  A laboratory full of bubbling vials. A robot arm lowers a tray:
#
#    "Sort my shelves and find the missing test tube, and the exit
#     hatch will open."
#
#  WHAT TO DO
#  Finish the three functions below so they RETURN the right answers.
#  Save the file and the game will test them.
#
#  TOPICS: lists, indexing, len(), .append(), sum()
# =====================================================================


def middle_item(shelf):
    """Return the item in the exact middle of the shelf. The shelf is a
    list with an odd number of items.

        middle_item(["red", "green", "blue"]) -> "green"

    Hint: len() and // will help you find the index.
    """
    # TODO
    pass


def remove_broken(vials):
    """Return a NEW list with every "broken" vial taken out. Keep the
    other vials in the same order, and don't change the original list.

        remove_broken(["red", "broken", "blue"]) -> ["red", "blue"]

    Hint: start with an empty list and .append() the good vials.
    """
    good = []
    # TODO
    return good


def find_missing(numbers):
    """The test tubes are numbered from 1, and there should be ONE MORE
    tube than the list holds. One tube is missing. numbers holds the tubes
    that are left, in any order. Return the number of the missing tube.

        find_missing([1, 2, 4, 5]) -> 3
        find_missing([2, 3, 1])    -> 4    (tubes 1 to 4, so 4 is missing)
    """
    # TODO
    pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print(middle_item(["red", "green", "blue"]))     # should print green
    print(remove_broken(["red", "broken", "blue"]))  # should print ['red', 'blue']
    print(find_missing([1, 2, 4, 5]))                # should print 3
