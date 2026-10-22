# =====================================================================
#  CHAPTER 2: THE MANOR
#  ROOM 9: THE ARCHIVE
# =====================================================================
#  You escaped the prison, straight into the grounds of a crumbling
#  manor. In the archive, a dusty ledger sits on a desk with a note:
#
#    "Balance my books and I'll show you the way out."
#
#  The ledger is the file ledger.txt, in the same folder as this file.
#  Open it and have a look! Each entry is:   date,item,amount
#  Some lines are blank, some are # comments, and some have extra spaces.
#
#  WHAT TO DO
#  Finish the four functions below. Each one is given a FILENAME, so
#  open that file (don't just type "ledger.txt" inside the function).
#
#  TOPICS: with open(), reading lines, .strip(), .split(), writing files
# =====================================================================


def count_lines(filename):
    """Return how many lines are in the file, counting EVERY line
    (blank lines and comments too).

        count_lines("ledger.txt") -> 12
    """
    # TODO
    pass


def read_entries(filename):
    """Return a list of (date, item, amount) tuples, one for each entry.
      - skip blank lines and lines starting with #
      - remove extra spaces around each part
      - amount should be an int

        read_entries("ledger.txt")[0] -> ("1891-01-03", "candles", 12)
    """
    entries = []
    # TODO
    return entries


def total_spent(filename, item):
    """Return the total amount spent on item. 0 if it was never bought.

        total_spent("ledger.txt", "coal") -> 75

    Hint: use your read_entries function!
    """
    # TODO
    pass


def write_report(filename, report_filename):
    """Write a report to report_filename with one line per item, in
    alphabetical order, showing the total spent:

        bread: 16
        candles: 35
        coal: 75
        ink: 3
    """
    # TODO
    pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    import os

    # This finds ledger.txt next to this file, wherever you run it from.
    here = os.path.dirname(os.path.abspath(__file__))
    ledger = os.path.join(here, "ledger.txt")

    print(count_lines(ledger))           # should print 12
    print(read_entries(ledger)[:2])      # the first two entries
    print(total_spent(ledger, "coal"))   # should print 75
    write_report(ledger, os.path.join(here, "report.txt"))
