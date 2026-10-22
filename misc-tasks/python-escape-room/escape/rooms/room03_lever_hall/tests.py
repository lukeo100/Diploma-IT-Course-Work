from escape.testkit import check_call


def test_sum_levers_small(s):
    """sum_levers adds up small numbers of levers"""
    check_call(s, "sum_levers", 4, 10)
    check_call(s, "sum_levers", 1, 1)
    check_call(s, "sum_levers", 0, 0)


def test_sum_levers_big(s):
    """sum_levers works for lots of levers"""
    check_call(s, "sum_levers", 10, 55)
    check_call(s, "sum_levers", 100, 5050)


def test_pulls_needed(s):
    """pulls_needed counts the halvings down to 0"""
    check_call(s, "pulls_needed", 8, 4)
    check_call(s, "pulls_needed", 1, 1)
    check_call(s, "pulls_needed", 0, 0)


def test_pulls_needed_odd(s):
    """pulls_needed works for weights that aren't powers of 2"""
    check_call(s, "pulls_needed", 100, 7)
    check_call(s, "pulls_needed", 1000, 10)


def test_count_multiples(s):
    """count_multiples counts the real levers"""
    check_call(s, "count_multiples", (1, 10, 3), 3)
    check_call(s, "count_multiples", (1, 10, 1), 10)
    check_call(s, "count_multiples", (1, 2, 5), 0)


def test_count_multiples_includes_stop(s):
    """count_multiples includes the stop lever"""
    check_call(s, "count_multiples", (10, 20, 4), 3)
    check_call(s, "count_multiples", (5, 5, 5), 1)
