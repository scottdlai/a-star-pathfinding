import pygame
from node import Node
from node_type import NodeType
from constants import NODE_SIZE, BORDER, PADDING


class Graph:
    """
    Represents a Graph as a grid (2d list).
    """

    def __init__(self, rows, collumns, window, start=(0, 0), end=None):
        """
        Construct a new Graph.
        """
        if end is None:
            self.end = (rows - 1, collumns - 1)
        else:
            self.end = end

        self.start = start

        self.window = window
        self._grid = []
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
        """
        Returns the neighbors of the specified Node
        """
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
        row, col = coordinate
        return (row >= 0 and row < len(self._grid)
                and col >= 0 and col < len(self._grid[row]))

    def update_start(self, new_start):
        if not self.__in_grid(new_start):
            return

        old_row, old_col = self.start
        row, col = new_start
        self.start = new_start
        self._grid[old_row][old_col].update_type(NodeType.EMPTY)
        self._grid[row][col].update_type(NodeType.START)

    def update_end(self, new_end):
        if not self.__in_grid(new_end):
            return

        old_row, old_col = self.end
        row, col = new_end
        self.end = new_end
        self._grid[old_row][old_col].update_type(NodeType.EMPTY)
        self._grid[row][col].update_type(NodeType.END)

    def make_wall(self, wall):
        if not self.__in_grid(wall):
            return

        row, col = wall
        self._grid[row][col].update_type(NodeType.WALL)

    def make_empty(self, empty):
        if not self.__in_grid(empty):
            return

        row, col = empty
        self._grid[row][col].update_type(NodeType.EMPTY)

    def is_wall(self, coordinate):
        if not self.__in_grid(coordinate):
            return False

        row, col = coordinate

        return self._grid[row][col].is_wall()

    def is_empty(self, coordinate):
        if not self.__in_grid(coordinate):
            return False

        row, col = coordinate
        return self._grid[row][col].is_empty()

    def is_start(self, coordinate):
        return coordinate == self.start

    def is_end(self, coordinate):
        return coordinate == self.end

    def toggle_wall(self, coordinate):
        if self.is_empty(coordinate):
            self.make_wall(coordinate)

        elif self.is_wall(coordinate):
            self.make_empty(coordinate)

    def clear(self):
        self.start = (0, 0)
        self.end = (len(self._grid) - 1, len(self._grid[0]) - 1)

        for row in self._grid:
            for node in row:
                node.update_type(NodeType.EMPTY)

        self._grid[0][0].update_type(NodeType.START)
        self._grid[self.end[0]][self.end[1]].update_type(NodeType.END)

    def draw(self):
        """
        Draws this Graph.
        """
        self.__draw_nodes()
        self.__draw_line()
        pygame.display.update()

    def __draw_line(self):
        """
        Draws the border between each node.
        """
        # top of the Graph
        top = PADDING
        # bottom of the Graph
        bottom = NODE_SIZE * len(self._grid) + PADDING
        # left side of the Graph
        left = PADDING
        # right side of the Graph
        right = NODE_SIZE * len(self._grid[0]) + PADDING

        for i in range(len(self._grid) + 1):
            y = i * NODE_SIZE + PADDING
            pygame.draw.line(self.window, BORDER, (left, y), (right, y))
            for j in range(len(self._grid[0]) + 1):
                x = j * NODE_SIZE + PADDING
                pygame.draw.line(self.window, BORDER, (x, top), (x, bottom))

    def __draw_nodes(self):
        """
        Draws the nodes.
        """
        for row in self._grid:
            for node in row:
                color = node.node_type.value
                x, y = node.coordinate
                pygame.draw.rect(self.window, color,
                                 (x, y, NODE_SIZE, NODE_SIZE))
