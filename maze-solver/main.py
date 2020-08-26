"""
Maze solver using A* algorithm.
"""
import pygame
from graph import Graph
from maze import generate_maze
from constants import WIDTH, HEIGHT, ROWS, COLUMNS, PADDING, NODE_SIZE
from a_star import a_star
from buttons import Button

pygame.init()

# Set up window
BACKGROUND = (0x00, 0x17, 0x1F)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze solver")
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
    btn_size = (NODE_SIZE * 3, NODE_SIZE)

    clear_btn_color = (0xFF, 0x28, 0x00)
    maze_btn_color = (0x00, 0xC0, 0x41)
    search_btn_color = (0x00, 0xA8, 0xE8)

    graph = Graph(ROWS, COLUMNS)

    clear_btn = Button(clear_btn_color, PADDING, NODE_SIZE * 0.5, btn_size, graph.clear)
    clear_btn.draw(WINDOW)

    maze_btn = Button(
        maze_btn_color,
        WIDTH - NODE_SIZE * 5,
        NODE_SIZE * 0.5,
        btn_size,
        lambda: generate_maze(graph, lambda: graph.draw(WINDOW)),
    )
    maze_btn.draw(WINDOW)

    search_btn = Button(
        search_btn_color,
        (WIDTH - 2 * PADDING) / 2,
        NODE_SIZE * 0.5,
        btn_size,
        lambda: a_star(
            graph,
            graph.get_start_node(),
            graph.get_end_node(),
            lambda: graph.draw(WINDOW),
        ),
    )
    search_btn.draw(WINDOW)

    running = True

    start_clicked = end_clicked = False

    has_searched = False

    while running:
        graph.draw(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            alt_down = pygame.key.get_mods() & pygame.KMOD_ALT

            if event.type == pygame.MOUSEBUTTONDOWN:
                if clear_btn.handle_event(event):
                    has_searched = False

                if maze_btn.handle_event(event):
                    has_searched = False

                if search_btn.handle_event(event):
                    has_searched = True

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

                if start_clicked and not graph.is_wall(pos) and not graph.is_end(pos):
                    graph.update_start(pos)

                    if has_searched:
                        a_star(graph, graph.get_start_node(), graph.get_end_node())

                elif end_clicked and not graph.is_wall(pos) and not graph.is_start(pos):
                    graph.update_end(pos)

                    if has_searched:
                        a_star(graph, graph.get_start_node(), graph.get_end_node())

                elif not graph.is_start(pos) and not graph.is_end(pos):
                    if alt_down:
                        graph.make_empty(pos)
                    else:
                        graph.make_wall(pos)

    pygame.quit()


main()
