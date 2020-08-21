import pygame
from constants import NODE_SIZE, PADDING
from node_type import NodeType

class Node:
    """
    Represent a node in the graph.
    """

    def __init__(self, row, col, node_type):
        """
        Constructs a Node object.
        """
        self.row = row
        self.col = col
        # Top left coordinate of this Node on the screen
        # Account for the offset to center the whole graph
        self.coordinate = (col * NODE_SIZE + PADDING, row * NODE_SIZE + PADDING)
        self.node_type = node_type
        self.parent = None
        self.distance = {
            "g": float("inf"),
            "f": float("inf"),
            "h": float("inf")
        }

    def is_wall(self):
        """
        Returns if this node is a wall.
        """
        return self.node_type is NodeType.WALL

    def is_start(self):
        """
        Returns if this node is the start node
        """
        return self.node_type is NodeType.START

    def is_end(self):
        """
        Returns if this Node is the end node.
        """
        return self.node_type is NodeType.END

    def is_empty(self):
        """
        """
        return self.node_type is NodeType.EMPTY

    def update_type(self, new_type):
        """
        Changes the type of this Node.
        """
        self.node_type = new_type

    def update_parent(self, new_parent):
        """
        Changes the parent of this Node.
        """
        self.parent = new_parent

    def update_distance(self, new_distance):
        """
        Updates the distance of this Node.
        """
        self.distance = new_distance
