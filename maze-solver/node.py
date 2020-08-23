import pygame
from constants import NODE_SIZE, PADDING
from node_type import NodeType


class Node:
    """Represent a node in the graph."""

    def __init__(self, row, col, node_type):
        """Constructs a Node object."""

        self.row = row
        self.col = col
        # Top left coordinate of this Node on the screen
        # Account for the PADDING to center the whole graph
        self.coordinate = (col * NODE_SIZE + PADDING,
                           row * NODE_SIZE + PADDING)
        self.node_type = node_type

    def is_wall(self):
        """Returns if this node is a wall."""

        return self.node_type is NodeType.WALL

    def is_start(self):
        """Returns if this node is the start node"""

        return self.node_type is NodeType.START

    def is_end(self):
        """Returns if this Node is the end node."""

        return self.node_type is NodeType.END

    def is_empty(self):
        """Returns if this Node is an empty node."""

        return self.node_type is NodeType.EMPTY

    def is_visited(self):
        """Returns if this Node is visited."""

        return self.node_type is NodeType.VISITED

    def is_path(self):
        """Returns if this Node is a path Node."""

        return self.node_type is NodeType.PATH

    def visits(self):
        """Set this Node as visited"""

        if not self.is_empty():
            return

        self.update_type(NodeType.VISITED)

    def update_type(self, new_type):
        """Changes the type of this Node."""

        self.node_type = new_type

    def draw(self, window):
        """Draws this Node on the specified window."""

        color = self.node_type.value
        x, y = self.coordinate
        pygame.draw.rect(window, color, (x, y, NODE_SIZE, NODE_SIZE))

    def __lt__(self, other):
        return True
