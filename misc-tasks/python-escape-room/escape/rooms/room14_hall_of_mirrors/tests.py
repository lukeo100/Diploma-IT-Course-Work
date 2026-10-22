from escape.testkit import check_call, need_recursion


def test_countdown(s):
    """countdown counts down, using recursion"""
    check_call(s, "countdown", 3, [3, 2, 1])
    check_call(s, "countdown", 1, [1])
    check_call(s, "countdown", 0, [])
    check_call(s, "countdown", 10, [10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
    need_recursion(s, "countdown")


def test_sum_digits(s):
    """sum_digits adds up digits, using recursion"""
    check_call(s, "sum_digits", 1234, 10)
    check_call(s, "sum_digits", 0, 0)
    check_call(s, "sum_digits", 7, 7)
    check_call(s, "sum_digits", 99999, 45)
    need_recursion(s, "sum_digits")


def test_flatten(s):
    """flatten unpacks nested lists, using recursion"""
    check_call(s, "flatten", ([1, [2, [3, 4]], 5],), [1, 2, 3, 4, 5])
    check_call(s, "flatten", ([[["deep"]], "shallow"],), ["deep", "shallow"])
    need_recursion(s, "flatten")


def test_flatten_edges(s):
    """flatten handles empty and already-flat lists"""
    check_call(s, "flatten", ([],), [])
    check_call(s, "flatten", ([[], [[]]],), [])
    check_call(s, "flatten", ([1, 2, 3],), [1, 2, 3])


def test_count_paths(s):
    """count_paths counts the routes, using recursion"""
    check_call(s, "count_paths", (1, 1), 1)
    check_call(s, "count_paths", (1, 5), 1)
    check_call(s, "count_paths", (2, 2), 2)
    check_call(s, "count_paths", (3, 3), 6)
    check_call(s, "count_paths", (3, 4), 10)
    check_call(s, "count_paths", (6, 6), 252)
    need_recursion(s, "count_paths")
