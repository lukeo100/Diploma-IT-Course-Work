# =====================================================================
#  ROOM 3: THE LEVER HALL
# =====================================================================
#  Beyond the keypad door is a long hall lined with rusty levers.
#  A sign reads:
#
#    "Only those who can count without tiring may pass."
#
#  WHAT TO DO
#  Finish the three functions below so they RETURN the right answers.
#  Save the file and the game will test them.
#
#  TOPICS: for loops, while loops, range()
# =====================================================================


def sum_levers(n):
    """Levers are numbered 1, 2, 3 ... n. Each lever weighs its number in kg.
    Return the total weight of all n levers.

        sum_levers(4) -> 10     because 1 + 2 + 3 + 4 = 10
        sum_levers(0) -> 0

    Use a for loop with range().
    """
    total = 0
    # TODO
    return total


def pulls_needed(weight):
    """Every pull of the big lever halves the counterweight, using whole
    numbers only (so use //). Return how many pulls it takes to get the
    weight down to 0.

        pulls_needed(8) -> 4    because 8 -> 4 -> 2 -> 1 -> 0
        pulls_needed(0) -> 0

    Use a while loop.
    """
    pulls = 0
    # TODO
    return pulls


def count_multiples(start, stop, k):
    """Only the levers whose number is a multiple of k are real. Count the
    real levers numbered from start to stop (INCLUDING stop).

        count_multiples(1, 10, 3) -> 3     (levers 3, 6 and 9)
    """
    # TODO
    pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print(sum_levers(4))              # should print 10
    print(pulls_needed(8))            # should print 4
    print(count_multiples(1, 10, 3))  # should print 3
