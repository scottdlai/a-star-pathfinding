import pygame
from node import Node
from node_type import NodeType
from constants import NODE_SIZE, BORDER, PADDING

HORIZONTAL = 0
VERTICAL = 1


class Graph:
    """Represents a Graph as a grid (2d list)."""

    def __init__(self, rows, collumns, start=(0, 0), end=None):
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
        return 0 <= row < self.rows and 0 <= col < self.collumns

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

        if not self.__in_grid(coordinate):
            return

        node = self.get(coordinate)
        
        if node.is_start() or node.is_end():
            return

        node.update_type(NodeType.WALL)

    def make_empty(self, coordinate):
        """Makes the Node at the specified (row, col) as an empty Node."""

        if not self.__in_grid(coordinate):
            return

        node = self.get(coordinate)

        if node.is_start() or node.is_end():
            return

        node.update_type(NodeType.EMPTY)

    def is_wall(self, coordinate):
        """Returns if the Node at the specified (row, col) is a wall."""

        if not self.__in_grid(coordinate):
            return False

        node = self.get(coordinate)

        return node.is_wall()

    def is_empty(self, coordinate):
        """Returns if the Node at the specified (row, col) is empty."""

        if not self.__in_grid(coordinate):
            return False

        node = self.get(coordinate)

        return node.is_empty()

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

        if not self.__in_grid(coordinate):
            return

        node = self.get(coordinate)

        if node.is_empty() or node.is_path() or node.is_visited():
            self.make_wall(coordinate)

        elif self.is_wall(coordinate):
            self.make_empty(coordinate)

    def get_start_node(self):
        """Gets the start Node of this Graph."""

        return self.get(self.start)

    def get_end_node(self):
        """Gets the end Node of this Graph."""

        return self.get(self.end)

    def get(self, coordinate):
        """Gets the Node at the specified (row, col)."""

        if not self.__in_grid(coordinate):
            return
        
        row, col = coordinate
        return self._grid[row][col]

    def get_grid(self):
        """Returns the grid of this graph."""

        return self._grid

    def clear_path(self):
        """
        Resets the boards by making all visited Node and path Node into empty 
        node.
        """

        for row in self._grid:
            for node in row:
                if node.is_path() or node.is_visited():
                    node.update_type(NodeType.EMPTY)

    def clear(self):
        """
        Resets the boards by making all nodes empty and set the start Node at
        top left corner and end Node at bottom right corner.
        """

        self.start = (0, 0)
        self.end = (self.rows - 1, self.collumns - 1)

        for row in self._grid:
            for node in row:
                node.update_type(NodeType.EMPTY)

        self._grid[0][0].update_type(NodeType.START)
        self._grid[self.end[0]][self.end[1]].update_type(NodeType.END)

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
