# =====================================================================
#  CHAPTER 2: THE MANOR
#  ROOM 15: THE INSPECTOR'S OFFICE            ** WRITE THE TESTS **
# =====================================================================
#  A stern inspector sits behind a desk piled with forms:
#
#    "Anyone can write code. Prove you can TEST it. I have four broken
#     copies of this function. Catch them all."
#
#  WHAT TO DO
#  is_valid_code (below) is already written, and it is correct.
#  Your job is to finish test_is_valid_code with asserts that check it.
#
#  The inspector will run your test function against:
#    - the real is_valid_code: your test must PASS (no assert fails)
#    - 4 broken versions: your test must FAIL for every one of them
#
#  So you need asserts for codes that should be accepted AND for codes
#  that should be rejected. Think about the ways the rules could break!
#
#  TOPICS: testing, assert, edge cases
# =====================================================================


def is_valid_code(code):
    """A door code is valid when:
      - it is exactly 6 characters long
      - the first 2 characters are CAPITAL letters
      - the last 4 characters are digits

        is_valid_code("AB1234") -> True
        is_valid_code("AB12")   -> False
    """
    return (
        len(code) == 6
        and code[:2].isalpha()
        and code[:2].isupper()
        and code[2:].isdigit()
    )


def test_is_valid_code(is_valid_code):
    """The inspector passes in a version of is_valid_code (real or broken)
    as the parameter, so your asserts below test whichever one it is.
    """
    assert is_valid_code("AB1234") == True
    # TODO: add more asserts. Which codes should be rejected?


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    test_is_valid_code(is_valid_code)   # no output means every assert passed
    print("Your test passes for the real is_valid_code.")
