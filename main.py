"""
Maze solver using A* algorithm.
"""
import pygame
from graph import Graph
from constants import WIDTH, HEIGHT, ROWS, COLUMNS, OFF_SET, NODE_SIZE, BACKGROUND

pygame.init()

# Set up window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze solver')
WINDOW.fill(BACKGROUND)


def get_clicked_pos(pos):
    x, y = pos

    row = (y - OFF_SET // 2) // NODE_SIZE
    col = (x - OFF_SET // 2) // NODE_SIZE

    return row, col


def main():
    graph = Graph(ROWS, COLUMNS, WINDOW)

    running = True

    while running:
        graph.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            shift_down = pygame.key.get_mods() & pygame.KMOD_SHIFT

            ctrl_down = pygame.key.get_mods() & pygame.KMOD_CTRL

            alt_down = pygame.key.get_mods() & pygame.KMOD_ALT

            if event.type == pygame.MOUSEBUTTONDOWN:
                left_mouse_clicked = event.button == 1

                if left_mouse_clicked and shift_down:
                    pos = event.pos
                    row, col = get_clicked_pos(pos)
                    graph.update_start((row, col))

                elif left_mouse_clicked and ctrl_down:
                    pos = event.pos
                    row, col = get_clicked_pos(pos)
                    graph.update_end((row, col))

                elif left_mouse_clicked:
                    pos = event.pos
                    row, col = get_clicked_pos(pos)
                    graph.toggle_wall((row, col))

            # Left mouse down (event.buttons[0])
            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                current = event.pos
                pos = get_clicked_pos(current)

                if graph.is_empty(pos) or graph.is_wall(pos):
                    if alt_down:
                        graph.make_empty(pos)
                    else:
                        graph.make_wall(pos)

            elif event.type == pygame.KEYDOWN:
                c_down = event.key == pygame.K_c

                if c_down and ctrl_down and not alt_down and not shift_down:
                    graph.clear()

    pygame.quit()


main()
