from escape.testkit import check_call


def test_count_items(s):
    """count_items counts each item"""
    check_call(s, "count_items", (["gold", "ruby", "gold"],), {"gold": 2, "ruby": 1})
    check_call(s, "count_items", (["coin"] * 5 + ["crown"],), {"coin": 5, "crown": 1})


def test_count_items_empty(s):
    """count_items gives an empty dict for an empty list"""
    check_call(s, "count_items", ([],), {})


def test_total_value(s):
    """total_value multiplies quantities by prices"""
    check_call(s, "total_value", ({"gold": 2, "ruby": 3}, {"gold": 100, "ruby": 250}), 950)
    check_call(s, "total_value", ({"gold": 2, "rock": 5}, {"gold": 100}), 200)


def test_total_value_empty(s):
    """total_value is 0 for an empty inventory"""
    check_call(s, "total_value", ({}, {"gold": 100}), 0)


def test_most_valuable(s):
    """most_valuable names the priciest item"""
    check_call(s, "most_valuable", ({"gold": 100, "ruby": 250},), "ruby")
    check_call(s, "most_valuable", ({"crown": 900, "coin": 1, "ring": 300},), "crown")
    check_call(s, "most_valuable", ({"dust": 0},), "dust")


def test_most_valuable_empty(s):
    """most_valuable returns None for an empty vault"""
    check_call(s, "most_valuable", ({},), None)
