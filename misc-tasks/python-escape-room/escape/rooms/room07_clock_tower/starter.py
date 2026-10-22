# =====================================================================
#  ROOM 7: THE CLOCK TOWER
# =====================================================================
#  A spiral staircase leads up into the clock tower. Giant gears grind
#  overhead. The tower door opens only when the clock is set and the
#  bell rings at the right hour.
#
#  WHAT TO DO
#  Finish to_24_hour and add_minutes, then write the chime function
#  YOURSELF from scratch. Save the file and the game will test them.
#
#  TOPICS: functions, parameters, return values, default parameters, %
# =====================================================================


def to_24_hour(hour, period):
    """Convert a 12-hour clock time to 24-hour time.
    period is "AM" or "PM".

        to_24_hour(3, "PM")  -> 15
        to_24_hour(9, "AM")  -> 9
        to_24_hour(12, "AM") -> 0     (midnight)
        to_24_hour(12, "PM") -> 12    (midday)
    """
    # TODO
    pass


def add_minutes(hour, minute, extra):
    """Move the clock forward by extra minutes on a 24-hour clock.
    Return the new time as (hour, minute).

        add_minutes(10, 30, 45) -> (11, 15)
        add_minutes(23, 50, 20) -> (0, 10)    (it wraps past midnight)
    """
    # TODO
    pass


# TODO: Write a function called chime, with two parameters:
#         hour   the hour on a 24-hour clock (0 to 23)
#         sound  the bell's sound, which should be "BONG" if not given
#
#       The bell strikes once for each hour on a 12-hour clock, so it
#       strikes 1 to 12 times (13:00 is 1 strike, 0:00 and 12:00 are 12).
#       Return the sound repeated that many times, with single spaces
#       between them.
#
#         chime(3)          -> "BONG BONG BONG"
#         chime(14, "DING") -> "DING DING"


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print(to_24_hour(3, "PM"))       # should print 15
    print(add_minutes(23, 50, 20))   # should print (0, 10)
    # print(chime(3))                # remove the # once chime exists
