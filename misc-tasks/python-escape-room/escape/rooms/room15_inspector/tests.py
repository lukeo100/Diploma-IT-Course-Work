from escape.testkit import Fail, explain, need_function, try_call


def real(code):
    return len(code) == 6 and code[:2].isalpha() and code[:2].isupper() and code[2:].isdigit()


def no_length_check(code):
    return code[:2].isalpha() and code[:2].isupper() and code[2:].isdigit()


def allows_lowercase(code):
    return len(code) == 6 and code[:2].isalpha() and code[2:].isdigit()


def checks_three_digits(code):
    return len(code) == 6 and code[:2].isalpha() and code[:2].isupper() and code[2:5].isdigit()


def rejects_everything(code):
    return False


def must_catch(s, broken, description):
    test = need_function(s, "test_is_valid_code")
    if try_call(test, real) is not None:
        raise Fail("First make your test pass for the real is_valid_code (see the check above).")
    if try_call(test, broken) is None:
        raise Fail("A broken version that {} got past your test. Add an assert that it would get wrong.".format(
            description))


def test_passes_real(s):
    """Your test passes for the real is_valid_code"""
    test = need_function(s, "test_is_valid_code")
    error = try_call(test, real)
    if error is not None:
        raise Fail("Your test fails for the CORRECT is_valid_code ({}). That assert expects the wrong "
                   "answer.".format(explain(error, s)))


def test_catches_no_length_check(s):
    """Your test catches a version that doesn't check the length"""
    must_catch(s, no_length_check, "doesn't check the length")


def test_catches_lowercase(s):
    """Your test catches a version that allows lowercase letters"""
    must_catch(s, allows_lowercase, "allows lowercase letters")


def test_catches_three_digits(s):
    """Your test catches a version that only checks three digits"""
    must_catch(s, checks_three_digits, "only checks the first three digits")


def test_catches_rejects_everything(s):
    """Your test catches a version that rejects every code"""
    must_catch(s, rejects_everything, "rejects every code, even valid ones,")
