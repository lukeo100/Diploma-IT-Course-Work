# =====================================================================
#  CHAPTER 2: THE MANOR
#  ROOM 16: THE OBSERVATORY                       (chapter finale)
# =====================================================================
#  At the top of the manor's tower is an observatory. The star
#  catalogue is a mess, but the exit is written in the stars. Clean the
#  data, find the brightest stars, and the dome will open to the sky.
#
#  The catalogue is stars.csv, in the same folder as this file. Each row:
#
#      name,constellation,magnitude,distance
#
#  Some rows are broken! Lower magnitude means BRIGHTER (Sirius, at
#  -1.46, is the brightest star in the night sky).
#
#  WHAT TO DO
#  Finish the four functions below. Each star is a dictionary:
#      {"name": "Vega", "constellation": "Lyra", "magnitude": 0.03, "distance": 25.0}
#
#  TOPICS: everything so far: files, strings, raise / try / except,
#          dicts, sorting with key=, comprehensions
# =====================================================================


def parse_row(line):
    """Turn one line of the catalogue into a star dictionary.
      - remove extra spaces around each part
      - magnitude and distance are floats
      - if the line doesn't have exactly 4 parts, raise ValueError
      - if magnitude or distance isn't a number, raise ValueError
        (float() already does that for you!)

        parse_row("Vega,Lyra,0.03,25")
          -> {"name": "Vega", "constellation": "Lyra", "magnitude": 0.03, "distance": 25.0}
    """
    # TODO
    pass


def load_stars(filename):
    """Read every star in the file. Skip blank lines and # lines.
    Rows that make parse_row raise ValueError are skipped and counted.
    Return a tuple: (list of star dicts, number of rows skipped).

        stars, skipped = load_stars("stars.csv")   ->  12 stars, 2 skipped
    """
    stars = []
    skipped = 0
    # TODO
    return stars, skipped


def brightest(stars, n):
    """Return the NAMES of the n brightest stars (lowest magnitude),
    brightest first.

        brightest(stars, 3) -> ["Sirius", "Canopus", "Arcturus"]
    """
    # TODO
    pass


def stars_in(stars, constellation):
    """Return the NAMES of the stars in constellation, closest first.

        stars_in(stars, "Orion") -> ["Bellatrix", "Betelgeuse", "Rigel", "Mintaka"]
    """
    # TODO
    pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    import os

    here = os.path.dirname(os.path.abspath(__file__))
    stars, skipped = load_stars(os.path.join(here, "stars.csv"))
    print(len(stars), "stars loaded,", skipped, "rows skipped")
    print(brightest(stars, 3))
    print(stars_in(stars, "Orion"))
