import pygame
from gui.components import Button, Text
from gui.abstract import Handler, Drawable
from gui import colors
from gui.gui_operator import GuiOperator
from gui import mode_page


class StartPage(Handler, Drawable):
    def __init__(self, screen: pygame.Surface, operator: GuiOperator):
        self.screen = screen
        self.operator = operator
        self.playButton = Button(screen, (260, 100, 200, 80), "PLAY", colors.LIGHT_GREEN, colors.RED)
        self.title = Text(screen, (220, 20), "SUPER GAME", 50, colors.BLUE)

    def draw(self):
        self.screen.fill(colors.LIGHT_GREEN)
        self.playButton.draw()
        self.title.draw()

    def handle(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            position = event.pos
            if self.playButton.accepts(position):
                self.operator.state = mode_page.ModePage(self.screen, self.operator)
