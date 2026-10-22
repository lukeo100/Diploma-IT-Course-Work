from escape.testkit import Fail, expect, need_class


def paintings(s):
    Painting = need_class(s, "Painting")
    return (
        Painting("The Starry Night", "Van Gogh", 1889),
        Painting("Mona Lisa", "Leonardo da Vinci", 1503),
        Painting("The Great Wave", "Hokusai", 1831),
    )


def call_text_method(name, obj):
    """str() and repr() crash if the method returns None, so explain that kindly."""
    try:
        return str(obj) if name == "__str__" else repr(obj)
    except TypeError:
        raise Fail("`{}` must RETURN a string, but it returned something else (probably None).".format(name))


def test_str(s):
    """__str__ gives a friendly description"""
    starry, mona, _ = paintings(s)
    expect(call_text_method("__str__", starry), "The Starry Night by Van Gogh (1889)", "str(starry)")
    expect(call_text_method("__str__", mona), "Mona Lisa by Leonardo da Vinci (1503)", "str(mona)")


def test_repr(s):
    """__repr__ shows how to make the painting"""
    starry, _, _ = paintings(s)
    expect(call_text_method("__repr__", starry), "Painting('The Starry Night', 'Van Gogh', 1889)", "repr(starry)")


def test_eq(s):
    """== compares title and artist"""
    Painting = need_class(s, "Painting")
    a = Painting("Sunflowers", "Van Gogh", 1888)
    expect(a == Painting("Sunflowers", "Van Gogh", 1888), True, "two identical paintings with ==")
    expect(a == Painting("Sunflowers", "Van Gogh", 1889), True, "same title and artist, different year, with ==")
    expect(a == Painting("Sunflowers", "Monet", 1888), False, "same title, different artist, with ==")
    expect(a == Painting("Irises", "Van Gogh", 1888), False, "different title, same artist, with ==")


def test_in_list(s):
    """`in` can find a painting in a list (it uses __eq__)"""
    Painting = need_class(s, "Painting")
    wall = list(paintings(s))
    expect(Painting("Mona Lisa", "Leonardo da Vinci", 1503) in wall, True, "a copy of the Mona Lisa `in` the wall list")


def test_lt(s):
    """< compares years"""
    starry, mona, wave = paintings(s)
    expect(mona < starry, True, "mona < starry")
    expect(starry < mona, False, "starry < mona")
    expect(wave < starry, True, "wave < starry")


def test_sorted(s):
    """sorted() puts paintings oldest first"""
    starry, mona, wave = paintings(s)
    try:
        result = sorted([starry, mona, wave])
    except TypeError:
        raise Fail("sorted() couldn't compare the paintings. Write `__lt__` and make it return True or False.")
    titles = [p.title for p in result]
    expect(titles, ["Mona Lisa", "The Great Wave", "The Starry Night"], "the titles after sorted()")
