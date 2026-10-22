from escape.testkit import Fail, check_call, check_raises, data_file, need_function, write_file


def star(name, constellation, magnitude, distance):
    return {"name": name, "constellation": constellation, "magnitude": magnitude, "distance": distance}


SAMPLE = [
    star("Rigel", "Orion", 0.13, 860.0),
    star("Vega", "Lyra", 0.03, 25.0),
    star("Bellatrix", "Orion", 1.64, 250.0),
    star("Sirius", "Canis Major", -1.46, 8.6),
    star("Betelgeuse", "Orion", 0.5, 548.0),
]


def test_parse_row(s):
    """parse_row turns a line into a star dict"""
    check_call(s, "parse_row", "Vega,Lyra,0.03,25", star("Vega", "Lyra", 0.03, 25.0))
    check_call(s, "parse_row", " Mintaka , Orion , 2.23 , 1200 ", star("Mintaka", "Orion", 2.23, 1200.0))


def test_parse_row_bad_numbers(s):
    """parse_row raises ValueError when a number isn't a number"""
    check_raises(s, "parse_row", "Mystery Star,Unknown,bright,999", ValueError)
    check_raises(s, "parse_row", "Nova,Cygnus,1.0,far", ValueError)


def test_parse_row_wrong_parts(s):
    """parse_row raises ValueError for the wrong number of parts"""
    check_raises(s, "parse_row", "Half a row,Orion", ValueError)
    check_raises(s, "parse_row", "A,B,1,2,3", ValueError)


def test_load_stars(s):
    """load_stars loads the good stars and counts the bad rows"""
    func = need_function(s, "load_stars")
    result = func(data_file("stars.csv"))
    if not isinstance(result, tuple) or len(result) != 2:
        raise Fail("load_stars should return a tuple: (stars, skipped). It returned {!r}.".format(result))
    stars, skipped = result
    names = [x.get("name") if isinstance(x, dict) else x for x in stars]
    wanted = ["Sirius", "Canopus", "Arcturus", "Vega", "Capella", "Rigel", "Procyon",
              "Betelgeuse", "Polaris", "Bellatrix", "Mintaka", "Alcor"]
    if names != wanted:
        raise Fail("load_stars should load these stars, in order:\n{}\nbut it loaded:\n{}".format(wanted, names))
    if skipped != 2:
        raise Fail("load_stars should skip 2 broken rows, but it says it skipped {!r}.".format(skipped))


def test_load_stars_other_file(s):
    """load_stars works on another file"""
    path = write_file("tiny.csv", "# tiny\nDeneb,Cygnus,1.25,2600\n\nbroken\n")
    check_call(s, "load_stars", path, ([star("Deneb", "Cygnus", 1.25, 2600.0)], 1))


def test_brightest(s):
    """brightest names the brightest stars (lowest magnitude first)"""
    check_call(s, "brightest", (SAMPLE, 3), ["Sirius", "Vega", "Rigel"])
    check_call(s, "brightest", (SAMPLE, 1), ["Sirius"])
    check_call(s, "brightest", ([], 2), [])


def test_stars_in(s):
    """stars_in lists a constellation's stars, closest first"""
    check_call(s, "stars_in", (SAMPLE, "Orion"), ["Bellatrix", "Betelgeuse", "Rigel"])
    check_call(s, "stars_in", (SAMPLE, "Lyra"), ["Vega"])
    check_call(s, "stars_in", (SAMPLE, "Draco"), [])
