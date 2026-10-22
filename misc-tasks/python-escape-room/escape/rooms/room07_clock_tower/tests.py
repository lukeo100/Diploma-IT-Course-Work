from escape.testkit import check_call


def test_to_24_hour(s):
    """to_24_hour converts ordinary AM and PM times"""
    check_call(s, "to_24_hour", (3, "PM"), 15)
    check_call(s, "to_24_hour", (9, "AM"), 9)
    check_call(s, "to_24_hour", (11, "PM"), 23)
    check_call(s, "to_24_hour", (1, "AM"), 1)


def test_to_24_hour_twelve(s):
    """to_24_hour gets midnight and midday right"""
    check_call(s, "to_24_hour", (12, "AM"), 0)
    check_call(s, "to_24_hour", (12, "PM"), 12)


def test_add_minutes(s):
    """add_minutes moves the clock forward"""
    check_call(s, "add_minutes", (10, 30, 45), (11, 15))
    check_call(s, "add_minutes", (0, 0, 0), (0, 0))


def test_add_minutes_wraps(s):
    """add_minutes wraps past midnight"""
    check_call(s, "add_minutes", (23, 50, 20), (0, 10))
    check_call(s, "add_minutes", (22, 15, 150), (0, 45))
    check_call(s, "add_minutes", (5, 0, 1440), (5, 0))


def test_chime_default(s):
    """chime uses "BONG" when no sound is given"""
    check_call(s, "chime", 3, "BONG BONG BONG")
    check_call(s, "chime", 13, "BONG")


def test_chime_sound(s):
    """chime uses the sound it is given"""
    check_call(s, "chime", (14, "DING"), "DING DING")
    check_call(s, "chime", 1, "TICK", kwargs={"sound": "TICK"})


def test_chime_twelve(s):
    """chime strikes 12 times at midnight and midday"""
    check_call(s, "chime", 0, " ".join(["BONG"] * 12))
    check_call(s, "chime", 12, " ".join(["BONG"] * 12))
