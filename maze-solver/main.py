"""
Maze solver using A* algorithm.
"""
import pygame
from graph import Graph
from maze import generate_maze
from constants import WIDTH, HEIGHT, ROWS, COLUMNS, PADDING, NODE_SIZE, BACKGROUND
from a_star import a_star

pygame.init()

# Set up window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze solver')
WINDOW.fill(BACKGROUND)


def get_clicked_pos(pos):
    """
    Returns the (row, col) pair on the graph from the specified (x, y) on the
    screen.
    """

    x, y = pos

    row = (y - PADDING) // NODE_SIZE
    col = (x - PADDING) // NODE_SIZE

    return row, col


def main():
    graph = Graph(ROWS, COLUMNS, WINDOW)

    running = True

    start_clicked = end_clicked = False

    has_searched = False

    while running:
        graph.draw(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            alt_down = pygame.key.get_mods() & pygame.KMOD_ALT

            ctrl_down = pygame.key.get_mods() & pygame.KMOD_CTRL

            if event.type == pygame.MOUSEBUTTONDOWN:
                left_mouse_clicked = event.button == 1

                if left_mouse_clicked:
                    pos = event.pos
                    # row, col on the graph
                    graph_coordinate = get_clicked_pos(pos)

                    if graph.is_start(graph_coordinate):
                        start_clicked = True

                    elif graph.is_end(graph_coordinate):
                        end_clicked = True

                    else:
                        graph.toggle_wall(graph_coordinate)

            elif event.type == pygame.MOUSEBUTTONUP:
                start_clicked = False
                end_clicked = False

            # Left mouse down (event.buttons[0])
            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                current = event.pos
                pos = get_clicked_pos(current)

                if start_clicked and not graph.is_wall(pos):
                    graph.update_start(pos)

                    if has_searched:
                        a_star(graph, graph.get_start_node(), graph.get_end_node())

                elif end_clicked and not graph.is_wall(pos):
                    graph.update_end(pos)

                    if has_searched:
                        a_star(graph, graph.get_start_node(), graph.get_end_node())

                elif graph.is_empty(pos) or graph.is_wall(pos):
                    if alt_down:
                        graph.make_empty(pos)
                    else:
                        graph.make_wall(pos)

            elif event.type == pygame.KEYDOWN:
                c_down = event.key == pygame.K_c
                m_down = event.key == pygame.K_m
                s_down = event.key == pygame.K_s

                if c_down and ctrl_down:
                    graph.clear()
                    has_searched = False

                elif m_down:
                    generate_maze(graph, lambda: graph.draw(WINDOW))
                    has_searched = False

                elif s_down:
                    a_star(graph, graph.get_start_node(),
                                   graph.get_end_node(),
                                   lambda: graph.draw(WINDOW))
                    has_searched = True

    pygame.quit()


main()
