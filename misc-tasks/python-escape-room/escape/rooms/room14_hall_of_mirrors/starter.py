# =====================================================================
#  CHAPTER 2: THE MANOR
#  ROOM 14: THE HALL OF MIRRORS
# =====================================================================
#  A hall where every mirror reflects another mirror, forever. A voice
#  whispers from every direction:
#
#    "To leave, a function must call itself... and know when to stop."
#
#  WHAT TO DO
#  Finish the four functions below using RECURSION: each function must
#  call itself. No for or while loops are needed (except in flatten).
#
#  Every recursive function has two parts:
#    1. a BASE CASE: a simple input where you know the answer straight away
#    2. a RECURSIVE CASE: solve a smaller version of the problem by
#       calling the function again, then use that answer
#
#  TOPICS: recursion, base cases, recursive cases
# =====================================================================


def countdown(n):
    """Return a list counting down from n to 1.

        countdown(3) -> [3, 2, 1]
        countdown(0) -> []
    """
    # TODO: base case: n is 0
    # TODO: recursive case: [n] followed by countdown(n - 1)
    pass


def sum_digits(n):
    """Return the sum of the digits of a whole number (0 or more).

        sum_digits(1234) -> 10      because 1 + 2 + 3 + 4 = 10
        sum_digits(0)    -> 0

    Hint: n % 10 is the last digit, and n // 10 is the rest of the number.
    """
    # TODO
    pass


def flatten(items):
    """items is a list that can contain lists, which can contain lists...
    Return one flat list of all the values, in order.

        flatten([1, [2, [3, 4]], 5]) -> [1, 2, 3, 4, 5]

    Hint: isinstance(item, list) tells you if item is a list.
    """
    result = []
    # TODO
    return result


def count_paths(rows, cols):
    """A grid has rows x cols squares. Starting in the top-left square,
    you may only move RIGHT or DOWN. Return how many different paths lead
    to the bottom-right square.

        count_paths(2, 2) -> 2      (right then down, or down then right)
        count_paths(3, 3) -> 6
        count_paths(1, 5) -> 1      (a single row: only one way)
    """
    # TODO
    pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print(countdown(3))                    # should print [3, 2, 1]
    print(sum_digits(1234))                # should print 10
    print(flatten([1, [2, [3, 4]], 5]))    # should print [1, 2, 3, 4, 5]
    print(count_paths(3, 3))               # should print 6
