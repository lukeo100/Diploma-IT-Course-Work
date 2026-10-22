from escape.testkit import Fail, expect, expect_raises, need_class, need_method


def balloon_class(s):
    Balloon = need_class(s, "Balloon")
    prop = vars(Balloon).get("altitude")
    if not isinstance(prop, property):
        raise Fail("`altitude` should be a property. Put `@property` above `def altitude(self):`.")
    return Balloon


def test_property(s):
    """altitude is a property backed by _altitude"""
    balloon = balloon_class(s)("Hope", 1500)
    expect(balloon.altitude, 1500, 'Balloon("Hope", 1500).altitude')
    if getattr(balloon, "_altitude", None) != 1500:
        raise Fail("Keep the real value in `self._altitude` (with the underscore).")
    expect(balloon_class(s)("Hope").altitude, 0, 'Balloon("Hope").altitude')


def test_setter(s):
    """altitude can be changed to safe values"""
    Balloon = balloon_class(s)
    if vars(Balloon)["altitude"].fset is None:
        raise Fail("`altitude` needs a setter: put `@altitude.setter` above a second `def altitude(self, value):`.")
    balloon = Balloon("Hope")
    balloon.altitude = 2500
    expect(balloon.altitude, 2500, "altitude after setting it to 2500")
    balloon.altitude = 10000
    expect(balloon.altitude, 10000, "altitude after setting it to 10000")


def test_setter_refuses(s):
    """The setter refuses unsafe altitudes"""
    balloon = balloon_class(s)("Hope", 300)

    def set_to(value):
        balloon.altitude = value

    expect_raises(lambda: set_to(-1), ValueError, "balloon.altitude = -1")
    expect_raises(lambda: set_to(10001), ValueError, "balloon.altitude = 10001")
    expect(balloon.altitude, 300, "altitude after refused changes")


def test_init_checks(s):
    """Making a balloon at an unsafe altitude is refused"""
    Balloon = balloon_class(s)
    expect_raises(lambda: Balloon("Mole", -50), ValueError, 'Balloon("Mole", -50)')


def test_altitude_km(s):
    """altitude_km is a read-only property"""
    Balloon = balloon_class(s)
    prop = vars(Balloon).get("altitude_km")
    if not isinstance(prop, property):
        raise Fail("`altitude_km` should be a property. Put `@property` above `def altitude_km(self):`.")
    if prop.fset is not None:
        raise Fail("`altitude_km` should be read-only, so don't give it a setter.")
    expect(Balloon("Hope", 1500).altitude_km, 1.5, 'Balloon("Hope", 1500).altitude_km')


def test_climb(s):
    """climb() goes up, but not too high"""
    balloon = balloon_class(s)("Hope", 9000)
    need_method(balloon, "climb")(500)
    expect(balloon.altitude, 9500, "altitude after climb(500) from 9000")
    expect_raises(lambda: balloon.climb(1000), ValueError, "climb(1000) from 9500")
    expect(balloon.altitude, 9500, "altitude after a refused climb")
