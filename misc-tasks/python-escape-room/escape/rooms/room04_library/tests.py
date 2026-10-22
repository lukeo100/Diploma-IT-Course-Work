from escape.testkit import check_call


def test_reverse_text(s):
    """reverse_text reverses a word"""
    check_call(s, "reverse_text", "ROOD", "DOOR")
    check_call(s, "reverse_text", "stressed", "desserts")


def test_reverse_text_edges(s):
    """reverse_text works with spaces and empty text"""
    check_call(s, "reverse_text", "a b c", "c b a")
    check_call(s, "reverse_text", "", "")


def test_first_letters(s):
    """first_letters builds the hidden word"""
    check_call(s, "first_letters", "keep every yard", "KEY")
    check_call(s, "first_letters", "Exit", "E")


def test_first_letters_spacing(s):
    """first_letters copes with extra spaces and empty text"""
    check_call(s, "first_letters", "  open   the  door ", "OTD")
    check_call(s, "first_letters", "", "")


def test_is_palindrome_true(s):
    """is_palindrome spots palindromes, ignoring case and spaces"""
    check_call(s, "is_palindrome", "Race car", True)
    check_call(s, "is_palindrome", "A", True)
    check_call(s, "is_palindrome", "Was it a car or a cat I saw", True)


def test_is_palindrome_false(s):
    """is_palindrome rejects non-palindromes"""
    check_call(s, "is_palindrome", "Python", False)
    check_call(s, "is_palindrome", "ab", False)
