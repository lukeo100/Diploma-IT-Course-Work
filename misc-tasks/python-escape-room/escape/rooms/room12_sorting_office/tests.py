from escape.testkit import Fail, check_call, need_function

PARCELS = [
    ("Clock", 12, "Paris"),
    ("Anvil", 50, "London"),
    ("Letter", 1, "Paris"),
    ("Teapot", 3, "Berlin"),
    ("Globe", 8, "London"),
]


def test_by_weight(s):
    """by_weight sorts lightest first"""
    check_call(s, "by_weight", (PARCELS,), [
        ("Letter", 1, "Paris"), ("Teapot", 3, "Berlin"), ("Globe", 8, "London"),
        ("Clock", 12, "Paris"), ("Anvil", 50, "London")])
    check_call(s, "by_weight", ([],), [])


def test_by_weight_keeps_original(s):
    """by_weight doesn't change the original list"""
    func = need_function(s, "by_weight")
    parcels = list(PARCELS)
    func(parcels)
    if parcels != PARCELS:
        raise Fail("by_weight changed the list it was given. Use `sorted(...)`, which makes a new list, "
                   "instead of `.sort()`, which changes the original.")


def test_top_three(s):
    """top_three names the three heaviest, heaviest first"""
    check_call(s, "top_three", (PARCELS,), ["Anvil", "Clock", "Globe"])
    check_call(s, "top_three", ([("Feather", 0, "Rome"), ("Brick", 2, "Oslo")],), ["Brick", "Feather"])


def test_by_city_then_name(s):
    """by_city_then_name sorts by city, then by name"""
    check_call(s, "by_city_then_name", (PARCELS,), [
        ("Teapot", 3, "Berlin"), ("Anvil", 50, "London"), ("Globe", 8, "London"),
        ("Clock", 12, "Paris"), ("Letter", 1, "Paris")])


def test_group_by_city(s):
    """group_by_city collects the names for each city"""
    check_call(s, "group_by_city", (PARCELS,), {
        "Paris": ["Clock", "Letter"], "London": ["Anvil", "Globe"], "Berlin": ["Teapot"]})
    check_call(s, "group_by_city", ([],), {})
