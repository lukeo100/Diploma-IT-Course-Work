# =====================================================================
#  ROOM 6: THE VAULT
# =====================================================================
#  The hatch drops you into a bank vault stacked with treasure.
#  A voice booms from the darkness:
#
#    "Count my treasure correctly, or stay here forever."
#
#  WHAT TO DO
#  Finish the three functions below so they RETURN the right answers.
#  Save the file and the game will test them.
#
#  TOPICS: dictionaries, keys and values, .get(), .items()
# =====================================================================


def count_items(items):
    """Count how many of each item is in the list. Return a dictionary
    that maps each item to its count.

        count_items(["gold", "ruby", "gold"]) -> {"gold": 2, "ruby": 1}
    """
    counts = {}
    # TODO
    return counts


def total_value(inventory, prices):
    """inventory maps each item to HOW MANY you have.
    prices maps each item to the price of ONE.
    Return the total value of the inventory. Items with no price are
    worth 0.

        total_value({"gold": 2, "rock": 5}, {"gold": 100}) -> 200

    Hint: dict.get(key, default)
    """
    # TODO
    pass


def most_valuable(prices):
    """Return the NAME of the item with the highest price.
    If prices is empty, return None.

        most_valuable({"gold": 100, "ruby": 250}) -> "ruby"
    """
    # TODO
    pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print(count_items(["gold", "ruby", "gold"]))               # {'gold': 2, 'ruby': 1}
    print(total_value({"gold": 2, "rock": 5}, {"gold": 100}))  # 200
    print(most_valuable({"gold": 100, "ruby": 250}))           # ruby
