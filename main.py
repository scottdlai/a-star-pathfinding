"""
Maze solver using A* algorithm.
"""
import pygame
from graph import Graph
from constants import WIDTH, HEIGHT, ROWS, COLUMNS, PADDING, NODE_SIZE, BACKGROUND

pygame.init()

# Set up window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze solver')
WINDOW.fill(BACKGROUND)


def get_clicked_pos(pos):
    x, y = pos

    row = (y - PADDING) // NODE_SIZE
    col = (x - PADDING) // NODE_SIZE

    return row, col


def main():
    graph = Graph(ROWS, COLUMNS, WINDOW)

    running = True

    start_clicked = end_clicked = False

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

                if start_clicked and graph.is_empty(pos):
                    graph.update_start(pos)

                elif end_clicked and graph.is_empty(pos):
                    graph.update_end(pos)

                elif graph.is_empty(pos) or graph.is_wall(pos):
                    if alt_down:
                        graph.make_empty(pos)
                    else:
                        graph.make_wall(pos)

            elif event.type == pygame.KEYDOWN:
                c_down = event.key == pygame.K_c
                m_down = event.key == pygame.K_m

                if c_down and ctrl_down:
                    graph.clear()
                elif m_down:
                    graph.generate_maze(WINDOW)

    pygame.quit()


main()
