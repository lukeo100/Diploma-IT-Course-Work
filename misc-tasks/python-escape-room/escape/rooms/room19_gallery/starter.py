# =====================================================================
#  CHAPTER 3: THE AIRSHIP
#  ROOM 19: THE GALLERY
# =====================================================================
#  The captain's private gallery. The paintings are all jumbled up, and
#  a parrot squawks:
#
#    "Name them! Compare them! SORT THEM!"
#
#  WHAT TO DO
#  Special methods (the ones with double underscores, "dunder" methods)
#  let your objects work with Python's built-in features:
#
#      print(p)        uses  __str__
#      p  (in shell)   uses  __repr__
#      p1 == p2        uses  __eq__
#      p1 < p2         uses  __lt__     (and sorted() uses <)
#
#  __init__ is done for you. Finish the four special methods.
#
#  TOPICS: __str__, __repr__, __eq__, __lt__
# =====================================================================


class Painting:
    def __init__(self, title, artist, year):
        self.title = title
        self.artist = artist
        self.year = year

    def __str__(self):
        """Return a friendly description, like:
            The Starry Night by Van Gogh (1889)
        """
        # TODO
        pass

    def __repr__(self):
        """Return code that would make this painting, like:
            Painting('The Starry Night', 'Van Gogh', 1889)
        """
        # TODO
        pass

    def __eq__(self, other):
        """Two paintings are equal if they have the same title AND artist."""
        # TODO
        pass

    def __lt__(self, other):
        """A painting is "less than" another if it is OLDER (smaller year).
        This is what lets sorted() put paintings in order."""
        # TODO
        pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    starry = Painting("The Starry Night", "Van Gogh", 1889)
    mona = Painting("Mona Lisa", "Leonardo da Vinci", 1503)
    print(starry)                     # The Starry Night by Van Gogh (1889)
    print(repr(starry))               # Painting('The Starry Night', 'Van Gogh', 1889)
    print(mona < starry)              # True
    print(sorted([starry, mona]))     # oldest first
