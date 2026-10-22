from escape.testkit import Fail, expect, expect_raises, need_attr, need_class, need_method


def full_crew(s):
    Crew, Member = need_class(s, "Crew"), need_class(s, "CrewMember")
    crew = Crew("The Albatross")
    add = need_method(crew, "add")
    add(Member("Ada", "pilot", 9))
    add(Member("Bo", "cook", 4))
    add(Member("Cy", "engineer", 7))
    add(Member("Di", "pilot", 6))
    return crew, Member


def test_init(s):
    """A new crew has its ship name and no members"""
    crew = need_class(s, "Crew")("The Albatross")
    expect(need_attr(crew, "ship_name"), "The Albatross", "crew.ship_name")
    expect(need_attr(crew, "members"), [], "crew.members")


def test_add(s):
    """add() puts members in the crew"""
    crew, _ = full_crew(s)
    names = [m.name for m in crew.members]
    expect(names, ["Ada", "Bo", "Cy", "Di"], "the names in crew.members")


def test_add_duplicate(s):
    """add() refuses a second member with the same name"""
    crew, Member = full_crew(s)
    expect_raises(lambda: crew.add(Member("Ada", "cook", 2)), ValueError, 'add(CrewMember("Ada", ...)) again')
    expect(len(crew.members), 4, "the number of members after a refused add")


def test_find(s):
    """find() returns the right member object"""
    crew, _ = full_crew(s)
    found = need_method(crew, "find")("Cy")
    if found is None or getattr(found, "name", None) != "Cy":
        raise Fail('find("Cy") should return the CrewMember object called Cy, but it returned {!r}.'.format(found))
    expect(crew.find("Zed"), None, 'find("Zed")', verb="should return", none_tip=None)


def test_by_role(s):
    """by_role() lists names for a role"""
    crew, _ = full_crew(s)
    expect(need_method(crew, "by_role")("pilot"), ["Ada", "Di"], 'by_role("pilot")', verb="should return")
    expect(crew.by_role("captain"), [], 'by_role("captain")', verb="should return")


def test_average_skill(s):
    """average_skill() averages the crew's skill"""
    crew, _ = full_crew(s)
    expect(need_method(crew, "average_skill")(), 6.5, "average_skill()", verb="should return")
    empty = need_class(s, "Crew")("Empty Ship")
    expect(empty.average_skill(), 0.0, "average_skill() for an empty crew", verb="should return")


def test_len(s):
    """len() gives the number of members"""
    crew, _ = full_crew(s)
    try:
        size = len(crew)
    except TypeError:
        raise Fail("len(crew) doesn't work yet. Write `__len__` and make it return a number.")
    expect(size, 4, "len(crew)")
