import random

from escape.testkit import Fail, check_call, need_function


def test_middle_item(s):
    """middle_item finds the middle of the shelf"""
    check_call(s, "middle_item", (["red", "green", "blue"],), "green")
    check_call(s, "middle_item", ([1, 2, 3, 4, 5],), 3)
    check_call(s, "middle_item", (["only"],), "only")


def test_remove_broken(s):
    """remove_broken keeps the good vials in order"""
    check_call(s, "remove_broken", (["red", "broken", "blue"],), ["red", "blue"])
    check_call(s, "remove_broken", (["broken", "green", "broken", "broken", "gold"],), ["green", "gold"])


def test_remove_broken_edges(s):
    """remove_broken handles all-broken and empty shelves"""
    check_call(s, "remove_broken", (["broken", "broken"],), [])
    check_call(s, "remove_broken", ([],), [])


def test_remove_broken_new_list(s):
    """remove_broken doesn't change the original list"""
    func = need_function(s, "remove_broken")
    vials = ["red", "broken", "blue"]
    func(vials)
    if vials != ["red", "broken", "blue"]:
        raise Fail(
            "remove_broken changed the list it was given (it's now {!r}). "
            "Build a new list with .append() instead of removing items.".format(vials))


def test_find_missing(s):
    """find_missing finds the missing tube"""
    check_call(s, "find_missing", ([1, 2, 4, 5],), 3)
    check_call(s, "find_missing", ([5, 3, 1, 2],), 4)


def test_find_missing_ends(s):
    """find_missing works when the first or last tube is missing"""
    check_call(s, "find_missing", ([2, 3, 1],), 4)
    check_call(s, "find_missing", ([2],), 1)
    check_call(s, "find_missing", ([],), 1)


def test_find_missing_big(s):
    """find_missing works on a big rack of 1000 tubes"""
    tubes = [n for n in range(1, 1001) if n != 618]
    random.Random(5).shuffle(tubes)
    check_call(s, "find_missing", (tubes,), 618)
