from escape.testkit import Fail, expect, expect_raises, need_attr, need_class, need_method


def navigation_error(s):
    error = need_class(s, "NavigationError")
    if not issubclass(error, Exception) or error is Exception:
        raise Fail("NavigationError should be its own class that inherits from Exception: "
                   "`class NavigationError(Exception):`.")
    return error


def port_class(s):
    Port = need_class(s, "Port")
    if not issubclass(Port, need_class(s, "Waypoint")):
        raise Fail("Port should inherit from Waypoint: `class Port(Waypoint):`.")
    return Port


def sample_route(s):
    Waypoint, Port = need_class(s, "Waypoint"), port_class(s)
    route = need_class(s, "Route")()
    add = need_method(route, "add")
    add(Port("Tower", 0, 0))
    add(Waypoint("Cloud", 3, 4))
    add(Port("Mast", 3, 10, False))
    add(Port("Home", 9, 18))
    return route


def test_navigation_error(s):
    """NavigationError is a custom exception"""
    navigation_error(s)


def test_waypoint(s):
    """Waypoint stores its position and measures distance"""
    Waypoint = need_class(s, "Waypoint")
    a, b = Waypoint("A", 0, 0), Waypoint("B", 3, 4)
    expect(need_attr(a, "name"), "A", 'Waypoint("A", 0, 0).name')
    expect(need_attr(b, "x"), 3, 'Waypoint("B", 3, 4).x')
    expect(need_method(a, "distance_to")(b), 5.0, "a.distance_to(b)", verb="should return")
    expect(b.distance_to(a), 5.0, "b.distance_to(a)", verb="should return")


def test_waypoint_str(s):
    """str() of a Waypoint"""
    expect(str(need_class(s, "Waypoint")("Home", 1, 2)), "Home (1, 2)", 'str(Waypoint("Home", 1, 2))')


def test_port(s):
    """Port is a Waypoint that may have fuel"""
    Port = port_class(s)
    dock = Port("Dock", 0, 0)
    expect(need_attr(dock, "name", "Waypoint's __init__ (call `super().__init__(name, x, y)`)"), "Dock", "dock.name")
    expect(need_attr(dock, "has_fuel"), True, 'Port("Dock", 0, 0).has_fuel')
    expect(str(dock), "Dock (0, 0) [fuel]", 'str(Port("Dock", 0, 0))')
    expect(str(Port("Dock", 0, 0, False)), "Dock (0, 0)", 'str(Port("Dock", 0, 0, False))')


def test_route_add(s):
    """A Route holds waypoints, and len() counts them"""
    route = sample_route(s)
    try:
        size = len(route)
    except TypeError:
        raise Fail("len(route) doesn't work yet. Write `__len__`.")
    expect(size, 4, "len(route) after adding 4 waypoints")
    expect(len(need_class(s, "Route")()), 0, "len(Route())")


def test_route_duplicate(s):
    """add() refuses a duplicate name with NavigationError"""
    error = navigation_error(s)
    route = sample_route(s)
    expect_raises(lambda: route.add(need_class(s, "Waypoint")("Cloud", 50, 50)), error, 'route.add(Waypoint("Cloud", ...)) again')


def test_total_distance(s):
    """total_distance adds up every leg"""
    route = sample_route(s)
    expect(need_method(route, "total_distance")(), 21.0, "route.total_distance()", verb="should return")
    empty = need_class(s, "Route")()
    if empty.total_distance() != 0:
        raise Fail("An empty route's total_distance() should be 0, not {!r}.".format(empty.total_distance()))


def test_check_range(s):
    """check_range raises NavigationError for a leg that's too long"""
    error = navigation_error(s)
    route = sample_route(s)
    expect(need_method(route, "check_range")(10), True, "route.check_range(10)", verb="should return")
    expect_raises(lambda: route.check_range(9.9), error, "route.check_range(9.9) (the last leg is 10)")
    expect_raises(lambda: route.check_range(4), error, "route.check_range(4)")


def test_fuel_stops(s):
    """fuel_stops lists the Ports that have fuel"""
    route = sample_route(s)
    expect(need_method(route, "fuel_stops")(), ["Tower", "Home"], "route.fuel_stops()", verb="should return")
