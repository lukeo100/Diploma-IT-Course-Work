from escape.testkit import check_call


def test_minutes_seconds_basic(s):
    """to_minutes_seconds(125) gives (2, 5)"""
    check_call(s, "to_minutes_seconds", 125, (2, 5))


def test_minutes_seconds_edges(s):
    """to_minutes_seconds works for exact minutes and under a minute"""
    check_call(s, "to_minutes_seconds", 60, (1, 0))
    check_call(s, "to_minutes_seconds", 59, (0, 59))
    check_call(s, "to_minutes_seconds", 3600, (60, 0))
    check_call(s, "to_minutes_seconds", 0, (0, 0))


def test_check_pin_open(s):
    """check_pin opens for the right PIN"""
    check_call(s, "check_pin", 4321, "OPEN")


def test_check_pin_low_high(s):
    """check_pin says TOO LOW or TOO HIGH"""
    check_call(s, "check_pin", 1000, "TOO LOW")
    check_call(s, "check_pin", 4320, "TOO LOW")
    check_call(s, "check_pin", 9999, "TOO HIGH")
    check_call(s, "check_pin", 4322, "TOO HIGH")


def test_alarm_level(s):
    """alarm_level gives green, amber or red"""
    check_call(s, "alarm_level", 0, "green")
    check_call(s, "alarm_level", 1, "amber")
    check_call(s, "alarm_level", 2, "amber")
    check_call(s, "alarm_level", 3, "red")
    check_call(s, "alarm_level", 10, "red")
