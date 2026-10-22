from escape.testkit import Fail, check_call, need_function

MAZE = [
    "#########",
    "#S..#...#",
    "#.#.#.#.#",
    "#.#...#E#",
    "#########",
]


def test_count_walls(s):
    """count_walls counts every hedge"""
    check_call(s, "count_walls", (MAZE,), 30)
    check_call(s, "count_walls", (["..", ".."],), 0)
    check_call(s, "count_walls", (["#", "##", "###"],), 6)


def test_find(s):
    """find returns the (row, column) of a symbol"""
    check_call(s, "find", (MAZE, "S"), (1, 1))
    check_call(s, "find", (MAZE, "E"), (3, 7))
    check_call(s, "find", (MAZE, "#"), (0, 0))


def test_find_missing(s):
    """find returns None when the symbol isn't there"""
    check_call(s, "find", (MAZE, "X"), None)


def test_neighbours(s):
    """neighbours finds open cells up, down, left and right"""
    check_call(s, "neighbours", (MAZE, 1, 1), [(2, 1), (1, 2)])
    check_call(s, "neighbours", (MAZE, 3, 7), [(2, 7)])
    check_call(s, "neighbours", (MAZE, 3, 4), [(3, 3), (3, 5)])


def test_neighbours_edges(s):
    """neighbours doesn't go off the edge of the grid"""
    check_call(s, "neighbours", (["S."], 0, 0), [(0, 1)])
    check_call(s, "neighbours", (["..", ".."], 1, 1), [(0, 1), (1, 0)])
    check_call(s, "neighbours", (["..", ".."], 0, 0), [(1, 0), (0, 1)])


def test_mark_path(s):
    """mark_path draws the path with * (but keeps S and E)"""
    path = [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 4), (3, 5)]
    check_call(s, "mark_path", (MAZE, path), [
        "#########",
        "#S**#...#",
        "#.#*#.#.#",
        "#.#***#E#",
        "#########",
    ])
    check_call(s, "mark_path", (MAZE, []), MAZE)


def test_mark_path_keeps_original(s):
    """mark_path doesn't change the original grid"""
    grid = list(MAZE)
    need_function(s, "mark_path")(grid, [(1, 2)])
    if grid != MAZE:
        raise Fail("mark_path changed the grid it was given. Build a new list of rows and return that.")
