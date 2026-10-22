from escape.testkit import check_call


def test_shift_letter(s):
    """shift_letter shifts lowercase and capital letters"""
    check_call(s, "shift_letter", ("a", 1), "b")
    check_call(s, "shift_letter", ("m", 13), "z")
    check_call(s, "shift_letter", ("H", 3), "K")


def test_shift_letter_wraps(s):
    """shift_letter wraps around the alphabet both ways"""
    check_call(s, "shift_letter", ("Z", 1), "A")
    check_call(s, "shift_letter", ("y", 28), "a")
    check_call(s, "shift_letter", ("c", -3), "z")
    check_call(s, "shift_letter", ("A", 26), "A")


def test_shift_letter_other(s):
    """shift_letter leaves non-letters alone"""
    check_call(s, "shift_letter", ("!", 5), "!")
    check_call(s, "shift_letter", (" ", 5), " ")
    check_call(s, "shift_letter", ("7", 5), "7")


def test_caesar(s):
    """caesar shifts a whole message"""
    check_call(s, "caesar", ("Hello, World!", 3), "Khoor, Zruog!")
    check_call(s, "caesar", ("abc xyz", 2), "cde zab")
    check_call(s, "caesar", ("", 5), "")


def test_read_dial(s):
    """read_dial turns text into a whole number"""
    check_call(s, "read_dial", "7", 7)
    check_call(s, "read_dial", " 12 ", 12)
    check_call(s, "read_dial", "-3", -3)


def test_read_dial_bad(s):
    """read_dial returns None for a broken dial instead of crashing"""
    check_call(s, "read_dial", "seven", None)
    check_call(s, "read_dial", "", None)
    check_call(s, "read_dial", "4.5", None)


def test_unlock(s):
    """unlock decodes the door's message"""
    check_call(s, "unlock", ("Khoor", "3"), "Hello")
    check_call(s, "unlock", ("Uryyb", "13"), "Hello")
    check_call(s, "unlock", ("Fvb lzjhwlk!", "7"), "You escaped!")


def test_unlock_bad_dial(s):
    """unlock reports a broken dial"""
    check_call(s, "unlock", ("Khoor", "abc"), "DIAL ERROR")
    check_call(s, "unlock", ("Khoor", ""), "DIAL ERROR")
