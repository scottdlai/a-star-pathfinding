from queue import PriorityQueue
from node_type import NodeType


FAILURE = []

def a_star(graph, start_node, end_node, draw=lambda: None, h=None):
    if h is None:
        h = lambda n: abs(end_node.row - n.row) + abs(end_node.col - n.col)

    if draw is None:
        draw = lambda: None

    graph.clear_path()

    open_set = PriorityQueue()

    came_from = {}

    g_score = {node: float("inf") for row in graph.get_grid() for node in row}

    f_score = {node: float("inf") for row in graph.get_grid() for node in row}

    g_score[start_node] = 0
    f_score[start_node] = h(start_node)

    open_set.put((f_score[start_node], start_node))

    while not open_set.empty():
        # Since Queue.get() returns a pair of (priority, item)
        _, current = open_set.get()

        current.visits()

        if current is end_node:
            return resconstruct_path(came_from, start_node, current, draw)

        for neighbor in graph.get_neighbors(current):
            if neighbor.is_wall():
                continue

            # since 1 is the weight between every node in the grid
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current

                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + h(neighbor)

                draw()

                if not neighbor.is_visited():
                    open_set.put((f_score[neighbor], neighbor))

    return FAILURE


def resconstruct_path(came_from, start, end, draw):
    current = came_from[end]

    total_path = []

    while current is not start:
        total_path.insert(0, current)
        current = came_from[current]

    for path in total_path:
        path.update_type(NodeType.PATH)
        draw()

    return total_path

