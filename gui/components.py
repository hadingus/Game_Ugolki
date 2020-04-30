from gui.abstract import Drawable
from gui.abstract import Handler
import pygame
from gui import colors


class Text(Drawable):
    def __init__(self, screen: pygame.Surface, position, text: str, size: int, color=colors.BLACK):
        self.text = text
        self.size = size
        self.color = color
        self.font = pygame.font.SysFont('Arial', self.size)
        self.screen = screen
        self.position = position
        pygame.font.init()

    def draw(self):
        self.screen.blit(self.font.render(self.text, False, self.color), self.position)


class Button(Drawable):
    def __init__(self, screen: pygame.Surface, rect, text: str, my_color=colors.WHITE, text_color=colors.BLACK):
        self.font_size = rect[3] * 4 // 5
        self.text = Text(screen, rect[:2], text, self.font_size, text_color)
        self.screen = screen
        self.rect = rect
        self.my_color = my_color
        self.text_color = text_color

    def draw(self):
        pygame.draw.rect(self.screen, self.my_color, self.rect)
        self.text.draw()

    def set_color(self, other_color):
        self.my_color = other_color

    def accepts(self, point):
        return self.rect[0] <= point[0] <= self.rect[0] + self.rect[2] \
               and self.rect[1] <= point[1] <= self.rect[1] + self.rect[3]


class CheckButton(Drawable):
    def __init__(self, screen: pygame.Surface, rect, text: str, my_color=colors.WHITE,
                 checked_color=colors.GREY, text_color=colors.BLACK):
        self.button = Button(screen, rect, text, my_color, text_color)
        self.my_color = my_color
        self.checked_color = checked_color
        self.checked = False

    def draw(self):
        self.button.draw()

    def on(self):
        self.checked = True
        self.button.my_color = self.checked_color

    def off(self):
        self.checked = False
        self.button.my_color = self.my_color

    def touch(self):
        if self.checked:
            self.off()
        else:
            self.on()

    def accepts(self, point):
        return self.button.accepts(point)
