# =====================================================================
#  CHAPTER 2: THE MANOR
#  ROOM 13: THE MAZE
# =====================================================================
#  Behind the manor is a hedge maze. The gardener's map shows it as a
#  list of strings, one string per row:
#
#      #  is a hedge        .  is a path
#      S  is the start      E  is the exit
#
#  A cell's position is (row, column), both counting from 0. So the
#  "S" in the maze below is at (1, 1), and grid[1][1] is "S".
#
#  WHAT TO DO
#  Finish the four functions below.
#
#  TOPICS: lists of lists (2D grids), nested loops, enumerate(), bounds
# =====================================================================

MAZE = [
    "#########",
    "#S..#...#",
    "#.#.#.#.#",
    "#.#...#E#",
    "#########",
]


def count_walls(grid):
    """Return how many hedge cells ("#") there are in the whole grid.

        count_walls(MAZE) -> 30
    """
    walls = 0
    # TODO: a loop over the rows, with a loop over each row's cells inside it
    return walls


def find(grid, symbol):
    """Return the (row, column) of the first cell containing symbol,
    searching row by row. Return None if it isn't there.

        find(MAZE, "S") -> (1, 1)
        find(MAZE, "E") -> (3, 7)
    """
    # TODO: enumerate() gives you the row and column numbers
    pass


def neighbours(grid, row, col):
    """Return a list of the open cells (anything that isn't "#") next to
    (row, col), checking in this order: up, down, left, right.
    Cells off the edge of the grid don't count.

        neighbours(MAZE, 1, 1) -> [(2, 1), (1, 2)]
    """
    # TODO
    pass


def mark_path(grid, path):
    """Return a NEW grid (a new list of strings) where every cell in path
    is replaced by "*", except "S" and "E", which stay as they are.
    Don't change the original grid.

        mark_path(MAZE, [(1, 2), (1, 3)])[1] -> "#S**#...#"

    Hint: strings can't be changed, but list(row) can, and
          "".join(cells) turns a list back into a string.
    """
    # TODO
    pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print(count_walls(MAZE))         # should print 30
    print(find(MAZE, "E"))           # should print (3, 7)
    print(neighbours(MAZE, 1, 1))    # should print [(2, 1), (1, 2)]
    for row in mark_path(MAZE, [(1, 2), (1, 3), (2, 3), (3, 3), (3, 4), (3, 5)]):
        print(row)
