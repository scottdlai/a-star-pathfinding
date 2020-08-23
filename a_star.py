from queue import PriorityQueue
from node_type import NodeType


FAILURE = []

def a_star(graph, start_node, end_node, draw):
    open_set = PriorityQueue()

    start_node.g_score = 0
    start_node.h_score = 0
    start_node.f_score = 0

    open_set.put((start_node.f_score, start_node))

    while not open_set.empty():
        # Since Queue.get() returns a pair of (priority, item)
        _, current = open_set.get()

        current.visits()

        if current is end_node:
            return resconstruct_path(end_node.parent, draw)

        for neighbor in graph.get_neighbors(current):
            if neighbor.is_wall():
                continue

            # since 1 is the weight between every node in the grid
            tentative_g_score = current.g_score + 1

            if tentative_g_score < neighbor.g_score:
                neighbor.update_parent(current)

                neighbor.g_score = tentative_g_score
                neighbor.h_score = h(neighbor, end_node)
                neighbor.f_score = neighbor.g_score + neighbor.h_score

                draw()

                if not neighbor.is_visited():
                    open_set.put((neighbor.f_score, neighbor))

    return FAILURE


def resconstruct_path(current, draw):
    total_path = []

    while current.parent is not None:
        total_path.append(current)
        current.update_type(NodeType.PATH)
        current = current.parent
        draw()

    return total_path

def h(node, end):
    return abs(end.row - node.row) + abs(end.col - node.col)
