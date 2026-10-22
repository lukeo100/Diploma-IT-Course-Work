# =====================================================================
#  ROOM 2: THE KEYPAD
# =====================================================================
#  The cell door creaks open into a corridor. At the far end is a steel
#  door with a glowing keypad. A screen above it flickers:
#
#    "ANSWER MY THREE QUESTIONS."
#
#  WHAT TO DO
#  Finish the three functions below so they RETURN the right answers.
#  Save the file and the game will test them.
#
#  TOPICS: arithmetic (+ - * / // % **), comparisons, if / elif / else
# =====================================================================


def to_minutes_seconds(total_seconds):
    """The keypad's timer shows a number of seconds, like 125.
    Return it as minutes and seconds:

        to_minutes_seconds(125) -> (2, 5)

    Hint: // gives whole-number division, % gives the remainder.
    """
    minutes = None  # TODO
    seconds = None  # TODO
    return minutes, seconds


def check_pin(guess):
    """The real PIN is 4321. Return:
        "OPEN"     if guess is the PIN
        "TOO LOW"  if guess is smaller than the PIN
        "TOO HIGH" if guess is bigger than the PIN
    """
    # TODO: use if / elif / else
    pass


def alarm_level(wrong_guesses):
    """The alarm gets louder with every wrong guess. Return:
        "green" for 0 wrong guesses
        "amber" for 1 or 2 wrong guesses
        "red"   for 3 or more wrong guesses
    """
    # TODO
    pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
#  The game ignores it, so experiment as much as you like.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print(to_minutes_seconds(125))  # should print (2, 5)
    print(check_pin(1000))          # should print TOO LOW
    print(alarm_level(2))           # should print amber
