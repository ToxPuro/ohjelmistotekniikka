import pygame as pg
from pygame.constants import MOUSEBUTTONDOWN, K_RETURN, K_BACKSPACE, QUIT


pg.init()
screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)


class ClickBox():

    def __init__(self, x_coordinate, y_coordinate, width, height, function, text='', font=pg.font.SysFont('Corbel', 35), rec_color=(100, 100, 100), text_color=(255, 255, 255)):
        self.rect = pg.Rect(x_coordinate, y_coordinate, width, height)
        self.rec_color = rec_color
        self.text = text
        self.txt_surface = font.render(text, True, text_color)
        self.function = function

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return self.function()

    def draw(self, screen):
        # Blit the text.
        pg.draw.rect(screen, self.rec_color, self.rect)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.


class InputBox:

    def __init__(self, x_coordinate, y_coordinate, width, height, text=''):
        self.rect = pg.Rect(x_coordinate, y_coordinate, width, height)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == KEYDOWN:
            if self.active:
                if event.key == K_RETURN:
                    result = self.text
                    self.text = ''
                    self.txt_surface = FONT.render(self.text, True, self.color)
                    return result
                if event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


def main():
    clock = pg.time.Clock()
    input_box1 = InputBox(100, 100, 140, 32)
    input_box2 = InputBox(100, 300, 140, 32)
    input_boxes = [input_box1, input_box2]
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()
