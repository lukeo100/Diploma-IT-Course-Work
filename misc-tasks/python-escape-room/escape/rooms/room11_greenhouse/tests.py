from escape.testkit import check_call, need_comprehension

PLANTS = [
    {"name": "Fern", "height": 40, "colour": "green", "water": 70},
    {"name": "Cactus", "height": 15, "colour": "green", "water": 5},
    {"name": "Rose", "height": 60, "colour": "red", "water": 25},
    {"name": "Tulip", "height": 30, "colour": "red", "water": 50},
    {"name": "Snapjaw", "height": 120, "colour": "purple", "water": 10},
]

OTHERS = [
    {"name": "Moss", "height": 2, "colour": "green", "water": 30},
    {"name": "Orchid", "height": 45, "colour": "white", "water": 29},
]


def test_squares(s):
    """squares squares every number, using a comprehension"""
    check_call(s, "squares", ([1, 2, 3],), [1, 4, 9])
    check_call(s, "squares", ([],), [])
    check_call(s, "squares", ([-4, 10],), [16, 100])
    need_comprehension(s, "squares")


def test_thirsty(s):
    """thirsty lists the dry plants, using a comprehension"""
    check_call(s, "thirsty", (PLANTS,), ["Cactus", "Rose", "Snapjaw"])
    check_call(s, "thirsty", (OTHERS,), ["Orchid"])
    need_comprehension(s, "thirsty")


def test_heights(s):
    """heights maps names to heights, using a dict comprehension"""
    check_call(s, "heights", (PLANTS,), {"Fern": 40, "Cactus": 15, "Rose": 60, "Tulip": 30, "Snapjaw": 120})
    check_call(s, "heights", ([],), {})
    need_comprehension(s, "heights")


def test_colours(s):
    """colours finds each different colour, using a set comprehension"""
    check_call(s, "colours", (PLANTS,), {"green", "red", "purple"})
    check_call(s, "colours", (OTHERS,), {"green", "white"})
    need_comprehension(s, "colours")
