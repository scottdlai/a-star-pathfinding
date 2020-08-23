from random import randint
import time
from constants import SLEEP_SPEEP

HORIZONTAL = 0
VERTICAL = 1


def generate_maze(graph, draw):
    """
    Makes the specified graph into a maze using the Recursive Division Algorithm
    and draws the process specified by the draw function.
    """

    graph.clear()
    divide(graph, draw, (0, 0), (graph.rows - 1, graph.collumns - 1))


def divide(graph, draw, top_left, bottom_right):
    """Recursive Division Algorithm to generate maze."""

    tl_row, tl_col = top_left
    br_row, br_col = bottom_right

    width = abs(tl_col - br_col) + 1
    height = abs(tl_row - br_row) + 1

    MINIMUM_SIZE = 4

    if width < MINIMUM_SIZE or height < MINIMUM_SIZE:
        return

    orientation = choose_orientation(width, height)

    time.sleep(SLEEP_SPEEP)

    if orientation == VERTICAL:
        wall_col = randint(tl_col + 1, br_col - 1)

        # draw walls
        # To compesate for the gap between walls
        for i in range(-2, height + 2):
            graph.make_wall((tl_row + i, wall_col))

        hole_1_row = randint(tl_row, br_row - 2)
        hole_2_row = hole_1_row + 1
        hole_3_row = hole_1_row + 2

        graph.make_empty((hole_1_row, wall_col))
        graph.make_empty((hole_2_row, wall_col))
        graph.make_empty((hole_3_row, wall_col))

        draw()

        divide(graph, draw, top_left, (br_row, wall_col - 2))
        divide(graph, draw, (tl_row, wall_col + 2), bottom_right)

    else:
        wall_row = randint(tl_row + 1, br_row - 1)

        # draw walls
        # To compensate for the gap between the walls
        for i in range(-2, width + 2):
            graph.make_wall((wall_row, tl_col + i))

        hole_1_col = randint(tl_col, br_col - 2)
        hole_2_col = hole_1_col + 1
        hole_3_col = hole_1_col + 2

        graph.make_empty((wall_row, hole_1_col))
        graph.make_empty((wall_row, hole_2_col))
        graph.make_empty((wall_row, hole_3_col))

        draw()

        divide(graph, draw, top_left, (wall_row - 2, br_col))
        divide(graph, draw, (wall_row + 2, tl_col), bottom_right)


def choose_orientation(width, height):
    """Helper function to decide which orientation to draw the wall."""

    if width > height:
        return VERTICAL

    elif width < height:
        return HORIZONTAL

    else:
        return randint(HORIZONTAL, VERTICAL)
