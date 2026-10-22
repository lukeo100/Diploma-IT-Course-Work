# =====================================================================
#  CHAPTER 2: THE MANOR
#  ROOM 11: THE GREENHOUSE
# =====================================================================
#  A steamy glass greenhouse, overgrown with strange plants. A gardening
#  robot creaks:
#
#    "I only understand ONE-LINERS. Speak to me in comprehensions!"
#
#  WHAT TO DO
#  Finish the four functions below. Each one must use a COMPREHENSION
#  (no for loops with append!). Most can be a single return line.
#
#  Each plant is a dictionary like this:
#      {"name": "Fern", "height": 40, "colour": "green", "water": 70}
#
#  TOPICS: list, dict and set comprehensions, filtering with if
# =====================================================================

PLANTS = [
    {"name": "Fern", "height": 40, "colour": "green", "water": 70},
    {"name": "Cactus", "height": 15, "colour": "green", "water": 5},
    {"name": "Rose", "height": 60, "colour": "red", "water": 25},
    {"name": "Tulip", "height": 30, "colour": "red", "water": 50},
    {"name": "Snapjaw", "height": 120, "colour": "purple", "water": 10},
]


def squares(numbers):
    """Return a list of each number squared.

        squares([1, 2, 3]) -> [1, 4, 9]
    """
    # TODO: one line, like  return [... for n in numbers]
    pass


def thirsty(plants):
    """Return the NAMES of the plants whose water is below 30.

        thirsty(PLANTS) -> ["Cactus", "Rose", "Snapjaw"]
    """
    # TODO
    pass


def heights(plants):
    """Return a dictionary that maps each plant's name to its height.

        heights(PLANTS) -> {"Fern": 40, "Cactus": 15, ...}
    """
    # TODO
    pass


def colours(plants):
    """Return a SET of all the different colours.

        colours(PLANTS) -> {"green", "red", "purple"}
    """
    # TODO
    pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print(squares([1, 2, 3]))   # should print [1, 4, 9]
    print(thirsty(PLANTS))      # should print ['Cactus', 'Rose', 'Snapjaw']
    print(heights(PLANTS))
    print(colours(PLANTS))
