import pygame
import time
from random import randrange, randint
from node import Node
from node_type import NodeType
from constants import NODE_SIZE, BORDER, PADDING, SLEEP_SPEEP

HORIZONTAL = 0
VERTICAL = 1


class Graph:
    """Represents a Graph as a grid (2d list)."""

    def __init__(self, rows, collumns, window, start=(0, 0), end=None):
        """Construct a new Graph."""

        if end is None:
            self.end = (rows - 1, collumns - 1)
        else:
            self.end = end

        self.start = start

        self._grid = []
        self.rows = rows
        self.collumns = collumns

        for row in range(rows):
            self._grid.append([])
            for col in range(collumns):
                if (row, col) == self.start:
                    node_type = NodeType.START
                elif (row, col) == self.end:
                    node_type = NodeType.END
                else:
                    node_type = NodeType.EMPTY

                self._grid[row].append(Node(row, col, node_type))

    def get_neighbors(self, node: Node):
        """Returns the neighbors of the specified Node."""

        neighbors = []
        row, col = node.row, node.col

        # top
        if self.__in_grid((row - 1, col)):
            neighbors.append(self._grid[row - 1][col])

        # left
        if self.__in_grid((row, col - 1)):
            neighbors.append(self._grid[row][col - 1])

        # right
        if self.__in_grid((row, col + 1)):
            neighbors.append(self._grid[row][col + 1])

        # bottom
        if self.__in_grid((row + 1, col)):
            neighbors.append(self._grid[row + 1][col])

        return neighbors

    def __in_grid(self, coordinate):
        """
        Returns if the specified coordinate (row, col) is in this graph's
        boundary.
        """

        row, col = coordinate
        return (row >= 0 and row < self.rows
                and col >= 0 and col < self.collumns)

    def update_start(self, new_start):
        """Makes the Node at the specified (row, col) as the start Node."""

        if not self.__in_grid(new_start):
            return

        old_row, old_col = self.start
        row, col = new_start
        self.start = new_start
        self._grid[old_row][old_col].update_type(NodeType.EMPTY)
        self._grid[row][col].update_type(NodeType.START)

    def update_end(self, new_end):
        """Makes the Node at the specified (row, col) as the end Node."""

        if not self.__in_grid(new_end):
            return

        old_row, old_col = self.end
        row, col = new_end
        self.end = new_end
        self._grid[old_row][old_col].update_type(NodeType.EMPTY)
        self._grid[row][col].update_type(NodeType.END)

    def make_wall(self, coordinate):
        """Makes the Node at the specified (row, col) as a wall Node."""

        if not self.__in_grid(coordinate) or not self.is_empty(coordinate):
            return

        row, col = coordinate
        self._grid[row][col].update_type(NodeType.WALL)

    def make_empty(self, coordinate):
        """Makes the Node at the specified (row, col) as an empty Node."""

        if not self.__in_grid(coordinate):
            return

        row, col = coordinate
        self._grid[row][col].update_type(NodeType.EMPTY)

    def is_wall(self, coordinate):
        """Returns if the Node at the specified (row, col) is a wall."""

        if not self.__in_grid(coordinate):
            return False

        row, col = coordinate

        return self._grid[row][col].is_wall()

    def is_empty(self, coordinate):
        """Returns if the Node at the specified (row, col) is empty."""

        if not self.__in_grid(coordinate):
            return False

        row, col = coordinate
        return self._grid[row][col].is_empty()

    def is_start(self, coordinate):
        """Returns if the Node at the specified (row, col) is a start Node."""

        return coordinate == self.start

    def is_end(self, coordinate):
        """Returns if the Node at the specified (row, col) is an end Node."""

        return coordinate == self.end

    def toggle_wall(self, coordinate):
        """
        Makes the Node at the specified (row, col) empty if it's a wall;
        otherwise a wall.
        """

        if self.is_empty(coordinate):
            self.make_wall(coordinate)

        elif self.is_wall(coordinate):
            self.make_empty(coordinate)

    def clear(self):
        """
        Resets the boards by making all nodes empty and set the start Node at
        top left corner and end Node at bottom right corner.
        """

        self.start = (0, 0)
        self.end = (len(self._grid) - 1, len(self._grid[0]) - 1)

        for row in self._grid:
            for node in row:
                node.update_type(NodeType.EMPTY)

        self._grid[0][0].update_type(NodeType.START)
        self._grid[self.end[0]][self.end[1]].update_type(NodeType.END)

    def generate_maze(self, window):
        """
        Makes this graph into a maze using the Recursive Division Algorithm and
        draws the graph on the specified window.
        """

        self.clear()
        self.divide((0, 0), (self.rows - 1, self.collumns - 1), window)

    def divide(self, top_left, bottom_right, window):
        """Recursive Division Algorithm to generate maze."""

        tl_row, tl_col = top_left
        br_row, br_col = bottom_right

        width = abs(tl_col - br_col) + 1
        height = abs(tl_row - br_row) + 1

        MINIMUM_SIZE = 4

        if width < MINIMUM_SIZE or height < MINIMUM_SIZE:
            return

        orientation = self.__choose_orientation(width, height)

        time.sleep(SLEEP_SPEEP)

        if orientation == VERTICAL:
            wall_col = randint(tl_col + 1, br_col - 1)

            # draw walls
            # To compesate for the gap between walls
            for i in range(-2, height + 2):
                self.make_wall((tl_row + i, wall_col))

            hole_1_row = randint(tl_row, br_row - 2)
            hole_2_row = hole_1_row + 1
            hole_3_row = hole_1_row + 2

            self.make_empty((hole_1_row, wall_col))
            self.make_empty((hole_2_row, wall_col))
            self.make_empty((hole_3_row, wall_col))

            self.draw(window)

            self.divide(top_left, (br_row, wall_col - 2), window)
            self.divide((tl_row, wall_col + 2), bottom_right, window)

        else:
            wall_row = randint(tl_row + 1, br_row - 1)

            # draw walls
            # To compensate for the gap between the walls
            for i in range(-2, width + 2):
                self.make_wall((wall_row, tl_col + i))

            hole_1_col = randint(tl_col, br_col - 2)
            hole_2_col = hole_1_col + 1
            hole_3_col = hole_1_col + 2

            self.make_empty((wall_row, hole_1_col))
            self.make_empty((wall_row, hole_2_col))
            self.make_empty((wall_row, hole_3_col))

            self.draw(window)

            self.divide(top_left, (wall_row - 2, br_col), window)
            self.divide((wall_row + 2, tl_col), bottom_right, window)

    def __choose_orientation(self, width, height):
        """Helper function to decide which orientation to draw the wall."""

        if width > height:
            return VERTICAL

        elif width < height:
            return HORIZONTAL

        else:
            return randint(HORIZONTAL, VERTICAL)

    def draw(self, window):
        """Draws this Graph on the specified window."""

        self.__draw_nodes(window)
        self.__draw_line(window)
        pygame.display.update()

    def __draw_line(self, window):
        """Draws the border between each node on the specified window."""

        # top of the Graph
        top = PADDING
        # bottom of the Graph
        bottom = NODE_SIZE * self.rows + PADDING
        # left side of the Graph
        left = PADDING
        # right side of the Graph
        right = NODE_SIZE * self.collumns + PADDING

        for i in range(self.rows + 1):
            y = i * NODE_SIZE + PADDING
            pygame.draw.line(window, BORDER, (left, y), (right, y))
            for j in range(self.collumns + 1):
                x = j * NODE_SIZE + PADDING
                pygame.draw.line(window, BORDER, (x, top), (x, bottom))

    def __draw_nodes(self, window):
        """Draws the nodes of this graph on the specified window."""

        for row in self._grid:
            for node in row:
                node.draw(window)
