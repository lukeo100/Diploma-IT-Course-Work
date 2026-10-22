from escape.testkit import Fail, check_call, expect, need_attr, need_class


def subclass(s, name):
    cls = need_class(s, name)
    engine = need_class(s, "Engine")
    if not issubclass(cls, engine) or cls is engine:
        raise Fail("`{0}` should inherit from Engine: start it with `class {0}(Engine):`.".format(name))
    for inherited in ("start", "describe"):
        if inherited in vars(cls):
            raise Fail("`{}` has its own `{}` method. Delete it: the one in Engine is inherited for free.".format(
                name, inherited))
    return cls


def check_engine(s, name, arg, kind, power):
    cls = subclass(s, name)
    engine = cls("Test", arg)
    shown = '{}("Test", {})'.format(name, arg)
    expect(need_attr(engine, "name", "Engine's __init__ (call `super().__init__(name)`)"), "Test", shown + ".name")
    expect(need_attr(engine, "running", "Engine's __init__ (call `super().__init__(name)`)"), False, shown + ".running")
    expect(engine.kind(), kind, shown + ".kind()", verb="should return")
    expect(engine.describe(), "Test ({})".format(kind), shown + ".describe()", verb="should return")
    expect(engine.power(), 0, shown + ".power() before start()", verb="should return")
    engine.start()
    expect(engine.power(), power, shown + ".power() after start()", verb="should return")


def test_steam_engine(s):
    """SteamEngine inherits from Engine and makes steam power"""
    check_engine(s, "SteamEngine", 40, "steam", 80)


def test_electric_engine(s):
    """ElectricEngine inherits from Engine and makes electric power"""
    check_engine(s, "ElectricEngine", 6, "electric", 30)


def test_total_power(s):
    """total_power works for any mix of engines"""
    steam = subclass(s, "SteamEngine")("Boiler", 40)
    electric = subclass(s, "ElectricEngine")("Dynamo", 6)
    idle = subclass(s, "SteamEngine")("Spare", 100)
    plain = need_class(s, "Engine")("Old")
    steam.start()
    electric.start()
    plain.start()
    check_call(s, "total_power", ([steam, electric, idle, plain],), 110)
    check_call(s, "total_power", ([],), 0)
