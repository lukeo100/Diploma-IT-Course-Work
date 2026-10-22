from escape.testkit import Fail, expect, expect_type, need_variable, printed


def test_prisoner_name(s):
    """prisoner_name holds your name as a str"""
    name = need_variable(s, "prisoner_name")
    expect_type(name, str, "prisoner_name")
    if not name.strip():
        raise Fail("`prisoner_name` is empty. Put your name between the quotes.")


def test_cell_number(s):
    """cell_number is 13, stored as an int"""
    number = need_variable(s, "cell_number")
    expect_type(number, int, "cell_number")
    expect(number, 13, "cell_number")


def test_escape_chance(s):
    """escape_chance is 0.25, stored as a float"""
    chance = need_variable(s, "escape_chance")
    expect_type(chance, float, "escape_chance")
    expect(chance, 0.25, "escape_chance")


def test_door_open(s):
    """door_open is False, stored as a bool"""
    door = need_variable(s, "door_open")
    expect_type(door, bool, "door_open")
    expect(door, False, "door_open")


def test_total_watchers(s):
    """total_watchers is guards + dogs"""
    total = need_variable(s, "total_watchers")
    expect(total, need_variable(s, "guards") + need_variable(s, "dogs"), "total_watchers")


def test_door_message(s):
    """door_message is built from your variables with an f-string"""
    message = need_variable(s, "door_message")
    name = need_variable(s, "prisoner_name")
    number = need_variable(s, "cell_number")
    if name is None or number is None:
        raise Fail("Finish `prisoner_name` and `cell_number` first. door_message is built from them.")
    expect(message, "Prisoner {} is in cell {}".format(name, number), "door_message")


def test_message_printed(s):
    """door_message is printed"""
    message = getattr(s, "door_message", None)
    if not isinstance(message, str) or message not in printed(s):
        raise Fail("door_message wasn't printed. Add `print(door_message)` at the bottom of your file.")
