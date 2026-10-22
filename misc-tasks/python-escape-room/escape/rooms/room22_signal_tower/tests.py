from escape.testkit import Fail, expect, need_attr, need_class


def signal_class(s):
    return need_class(s, "Signal")


def test_class_attributes(s):
    """Signal has class attributes count and MAX_STRENGTH"""
    Signal = signal_class(s)
    for name in ("count", "MAX_STRENGTH"):
        if name not in vars(Signal):
            raise Fail("Signal needs a class attribute called `{}`. Write it inside the class, "
                       "but outside every method.".format(name))
    expect(Signal.MAX_STRENGTH, 10, "Signal.MAX_STRENGTH")


def test_init(s):
    """Signal stores its code and strength"""
    signal = signal_class(s)("SOS", 7)
    expect(need_attr(signal, "code"), "SOS", 'Signal("SOS", 7).code')
    expect(need_attr(signal, "strength"), 7, 'Signal("SOS", 7).strength')


def test_max_strength(s):
    """Strength is capped at MAX_STRENGTH"""
    signal = signal_class(s)("SOS", 50)
    expect(need_attr(signal, "strength"), 10, 'Signal("SOS", 50).strength')


def test_count(s):
    """Signal.count goes up for every new signal"""
    Signal = signal_class(s)
    if "count" not in vars(Signal):
        raise Fail("Add the class attribute `count = 0` first.")
    before = Signal.count
    one = Signal("ONE", 1)
    Signal("TWO", 2)
    if "count" in vars(one):
        raise Fail("Each signal got its own `count`. Use `Signal.count += 1`, not `self.count += 1`.")
    expect(Signal.count, before + 2, "Signal.count after making 2 more signals")


def test_is_valid_code(s):
    """is_valid_code is a static method that checks codes"""
    Signal = signal_class(s)
    if not isinstance(vars(Signal).get("is_valid_code"), staticmethod):
        raise Fail("Put `@staticmethod` on the line above `def is_valid_code(code):`.")
    for code, wanted in [("SOS", True), ("HLP", True), ("sos", False), ("SO", False), ("SOSS", False), ("S0S", False)]:
        expect(Signal.is_valid_code(code), wanted, "Signal.is_valid_code({!r})".format(code), verb="should return")


def test_from_string(s):
    """from_string is a class method that reads "CODE:strength" """
    Signal = signal_class(s)
    if not isinstance(vars(Signal).get("from_string"), classmethod):
        raise Fail("Put `@classmethod` on the line above `def from_string(cls, text):`.")
    signal = Signal.from_string("SOS:7")
    if not isinstance(signal, Signal):
        raise Fail('Signal.from_string("SOS:7") should return a Signal, but it returned {!r}.'.format(signal))
    expect(signal.code, "SOS", 'Signal.from_string("SOS:7").code')
    expect(signal.strength, 7, 'Signal.from_string("SOS:7").strength')
    expect(Signal.from_string("HLP:50").strength, 10, 'Signal.from_string("HLP:50").strength')


def test_from_string_uses_cls(s):
    """from_string works for subclasses too (it uses cls)"""
    Signal = signal_class(s)
    Flare = type("Flare", (Signal,), {})
    flare = Flare.from_string("SOS:3")
    if type(flare) is not Flare:
        raise Fail("`Flare.from_string(...)` made a {} instead of a Flare. Build the object with "
                   "`cls(...)` instead of `Signal(...)`.".format(type(flare).__name__))
