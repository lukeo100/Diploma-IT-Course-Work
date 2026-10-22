# =====================================================================
#  ROOM 8: THE FINAL DOOR
# =====================================================================
#  The last door. It's covered in scrambled letters and has a dial you
#  can turn. An inscription reads:
#
#    "Only a true Pythonista can decode my message. Turn the dial
#     wisely: a bad dial must never break you."
#
#  WHAT TO DO
#  Finish the four functions below. Each one builds on the one before.
#  Save the file and the game will test them.
#
#  TOPICS: strings, ord() and chr(), loops, functions, try / except
# =====================================================================


def shift_letter(letter, shift):
    """Shift ONE letter along the alphabet by shift places, wrapping
    around from z back to a. Capitals stay capitals and lowercase stays
    lowercase. Anything that isn't a letter (spaces, digits, !) comes
    back unchanged.

        shift_letter("a", 1)  -> "b"
        shift_letter("Z", 1)  -> "A"
        shift_letter("c", -3) -> "z"
        shift_letter("!", 5)  -> "!"

    Hint: ord("a") is 97 and chr(97) is "a". % handles the wrapping.
    """
    # TODO
    pass


def caesar(text, shift):
    """Shift every character in text using shift_letter.

        caesar("Hello, World!", 3) -> "Khoor, Zruog!"
    """
    # TODO
    pass


def read_dial(value):
    """The dial gives you TEXT, like "7" or " 12 " or "seven".
    Turn it into an int. If it isn't a whole number, return None.

        read_dial("7")     -> 7
        read_dial("seven") -> None

    Use try / except ValueError. Don't let the program crash!
    """
    # TODO
    pass


def unlock(message, dial):
    """Put it all together:
      1. read the dial with read_dial()
      2. if the dial is broken (None), return "DIAL ERROR"
      3. otherwise DECODE the message by shifting it BACKWARDS by the
         dial amount, and return it.

        unlock("Khoor", "3")   -> "Hello"
        unlock("Khoor", "abc") -> "DIAL ERROR"
    """
    # TODO
    pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print(shift_letter("a", 1))            # should print b
    print(caesar("Hello, World!", 3))      # should print Khoor, Zruog!
    print(read_dial("seven"))              # should print None
    print(unlock("Fvb lzjhwlk!", "7"))     # what does the door say?
