# =====================================================================
#  CHAPTER 2: THE MANOR
#  ROOM 10: THE WORKSHOP                     ** FIX THE BUGS **
# =====================================================================
#  A workshop full of half-built clockwork. The previous owner left
#  four machines that ALMOST work. They run without crashing, but they
#  give the wrong answers.
#
#  WHAT TO DO
#  Every function below has exactly ONE bug. Find it and fix it.
#  Don't rewrite the functions from scratch: a real programmer's job is
#  usually to fix the code that's already there, with small changes.
#
#  Tip: run this file yourself (see the bottom) and compare what each
#  function returns with what its docstring says it should return.
#
#  TOPICS: debugging, loops, return, default arguments, conditions
# =====================================================================


def average(scores):
    """Return the average (mean) of a list of numbers.

        average([10, 20, 30]) -> 20.0
    """
    total = 0
    for i in range(1, len(scores)):
        total += scores[i]
    return total / len(scores)


def all_doors_locked(doors):
    """doors is a list like ["locked", "open", "locked"].
    Return True only if EVERY door is "locked".

        all_doors_locked(["locked", "locked"]) -> True
        all_doors_locked(["locked", "open"])   -> False
    """
    for door in doors:
        if door == "open":
            return False
        else:
            return True
    return True


def add_tool(tool, toolbox=[]):
    """Add tool to the toolbox and return the toolbox.
    If no toolbox is given, start a NEW empty one.

        add_tool("hammer")          -> ["hammer"]
        add_tool("saw")             -> ["saw"]
        add_tool("glue", ["tape"])  -> ["tape", "glue"]
    """
    toolbox.append(tool)
    return toolbox


def is_weekend(day):
    """Return True if day is "Saturday" or "Sunday", otherwise False.

        is_weekend("Sunday") -> True
        is_weekend("Monday") -> False
    """
    if day == "Saturday" or "Sunday":
        return True
    return False


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print(average([10, 20, 30]))                # should print 20.0
    print(all_doors_locked(["locked", "open"]))  # should print False
    print(add_tool("hammer"))                   # should print ['hammer']
    print(add_tool("saw"))                      # should print ['saw']
    print(is_weekend("Monday"))                 # should print False
