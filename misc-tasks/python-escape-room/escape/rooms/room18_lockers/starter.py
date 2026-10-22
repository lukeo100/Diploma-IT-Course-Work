# =====================================================================
#  CHAPTER 3: THE AIRSHIP
#  ROOM 18: THE CREW LOCKERS
# =====================================================================
#  A corridor of brass crew lockers. Yours has a keypad and a coin
#  slot. A label warns:
#
#    "A good locker never lets anyone cheat, not even you."
#
#  WHAT TO DO
#  Finish the Locker class below. The locker protects its own coins:
#  nothing can go in or out while it's locked, and bad amounts are
#  refused with an error.
#
#  TOPICS: object state, methods that return True/False, raise ValueError
# =====================================================================


class Locker:
    def __init__(self, owner, pin):
        """A new locker belongs to owner, opens with pin, holds 0 coins
        and starts LOCKED. Store: owner, pin, coins, locked.
        """
        # TODO
        pass

    def unlock(self, pin):
        """If pin is right, unlock the locker and return True.
        Otherwise stay locked and return False."""
        # TODO
        pass

    def lock(self):
        """Lock the locker."""
        # TODO
        pass

    def deposit(self, amount):
        """If the locker is locked, return False and do nothing.
        If amount is 0 or less, raise ValueError.
        Otherwise add amount to coins and return True."""
        # TODO
        pass

    def withdraw(self, amount):
        """If the locker is locked, return False and do nothing.
        If amount is 0 or less, or more than the coins inside, raise ValueError.
        Otherwise take amount out of coins and return True."""
        # TODO
        pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    mine = Locker("Sam", 1234)
    print(mine.deposit(10))    # should print False (it's locked)
    print(mine.unlock(1234))   # should print True
    print(mine.deposit(10))    # should print True
    print(mine.coins)          # should print 10
    try:
        mine.withdraw(50)
    except ValueError as error:
        print("Refused:", error)
