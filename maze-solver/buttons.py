import pygame


class Button:
    def __init__(self, color, x, y, size, event_handler):
        """Constructs a button."""

        width, height = size
        self.rect = (x, y, width, height)
        self.event_handler = event_handler
        self.color = color
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

        pygame.display.update()

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return False

        if event.button != 1:
            return False

        if not self._is_inside_button(event.pos):
            return False
        
        self.event_handler()

        return True

    def _is_inside_button(self, pos):
        x, y, width, height = self.rect

        pos_x, pos_y = pos

        return x <= pos_x <= x + width and y <= pos_y <= y + height
