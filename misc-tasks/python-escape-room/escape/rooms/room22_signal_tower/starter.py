# =====================================================================
#  CHAPTER 3: THE AIRSHIP
#  ROOM 22: THE SIGNAL TOWER
# =====================================================================
#  High on the mast is the signal tower. To call for help you need to
#  send signals, but the machine also keeps count of every signal ever
#  made, and it only reads them in one format.
#
#  WHAT TO DO
#  Finish the Signal class. It uses three new ideas:
#
#    CLASS ATTRIBUTES   belong to the class, shared by every object.
#                       Written inside the class but outside any method.
#    @staticmethod      a method that needs neither self nor the class:
#                       just a helper function that lives in the class.
#    @classmethod       a method that gets the CLASS (cls) instead of an
#                       object. Often used as another way to make objects.
#
#  TOPICS: class attributes, @staticmethod, @classmethod
# =====================================================================


class Signal:
    # TODO: class attribute  count = 0         (how many Signals were ever made)
    # TODO: class attribute  MAX_STRENGTH = 10

    def __init__(self, code, strength):
        """Store code and strength, but strength can never be more than
        Signal.MAX_STRENGTH. Also add 1 to Signal.count.

        Careful: self.count += 1 would NOT change the shared count!
        """
        # TODO
        pass

    # TODO: make this a static method (add a decorator on the line above)
    def is_valid_code(code):
        """Return True if code is exactly 3 capital letters, like "SOS"."""
        # TODO
        pass

    # TODO: make this a class method (add a decorator on the line above)
    def from_string(cls, text):
        """Make a new signal from text like "SOS:7" (code:strength).
        Use cls(...) to make the object, not Signal(...).

            Signal.from_string("SOS:7")  -> a Signal with code "SOS", strength 7
        """
        # TODO
        pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    first = Signal("SOS", 5)
    second = Signal.from_string("HLP:50")
    print(second.code, second.strength)     # should print HLP 10
    print(Signal.count)                     # should print 2
    print(Signal.is_valid_code("SOS"))      # should print True
