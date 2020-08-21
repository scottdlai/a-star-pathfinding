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
        graph.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            alt_down = pygame.key.get_mods() & pygame.KMOD_ALT

            if event.type == pygame.MOUSEBUTTONDOWN:
                left_mouse_clicked = event.button == 1

                if left_mouse_clicked:
                    pos = event.pos
                    row, col = get_clicked_pos(pos)

                    if (row, col) == graph.start:
                        start_clicked = True
                    elif (row, col) == graph.end:
                        end_clicked = True
                    else: 
                        graph.toggle_wall((row, col))

            elif event.type == pygame.MOUSEBUTTONUP:
                start_clicked = False
                end_clicked = False

            # Left mouse down (event.buttons[0])
            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                current = event.pos
                pos = get_clicked_pos(current)

                if start_clicked:
                    graph.update_start(pos)
                elif end_clicked:
                    graph.update_end(pos)
                elif graph.is_empty(pos) or graph.is_wall(pos):
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
