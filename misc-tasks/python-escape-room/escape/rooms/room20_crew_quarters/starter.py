# =====================================================================
#  CHAPTER 3: THE AIRSHIP
#  ROOM 20: THE CREW QUARTERS
# =====================================================================
#  Hammocks swing in the crew quarters. The ship's log is missing its
#  crew list, and the airship won't take orders from a crew it doesn't
#  know.
#
#  WHAT TO DO
#  CrewMember is done for you. Finish the Crew class: a Crew object
#  holds a LIST of CrewMember objects. One object containing others is
#  called "composition".
#
#  TOPICS: objects inside objects, searching a list of objects, __len__
# =====================================================================


class CrewMember:
    def __init__(self, name, role, skill):
        self.name = name
        self.role = role      # like "pilot", "engineer" or "cook"
        self.skill = skill    # a number from 1 to 10


class Crew:
    def __init__(self, ship_name):
        """Store ship_name, and start with an empty list called members."""
        # TODO
        pass

    def add(self, member):
        """Add a CrewMember to the crew. If someone with the same NAME is
        already in the crew, raise ValueError instead."""
        # TODO
        pass

    def find(self, name):
        """Return the CrewMember with this name, or None if there isn't one."""
        # TODO
        pass

    def by_role(self, role):
        """Return a list of the NAMES of the members with this role,
        in the order they were added."""
        # TODO
        pass

    def average_skill(self):
        """Return the average skill of the crew as a float.
        Return 0.0 if the crew is empty."""
        # TODO
        pass

    def __len__(self):
        """len(crew) should give the number of members."""
        # TODO
        pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    crew = Crew("The Albatross")
    crew.add(CrewMember("Ada", "pilot", 9))
    crew.add(CrewMember("Bo", "cook", 4))
    print(len(crew))                 # should print 2
    print(crew.find("Ada").role)     # should print pilot
    print(crew.by_role("cook"))      # should print ['Bo']
    print(crew.average_skill())      # should print 6.5
