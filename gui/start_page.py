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
        self.playButton = Button(screen, (180, 70, 500, 250), "PLAY", colors.LIGHT_GREEN, colors.RED)
        self.authors = Text(screen, (340, 300), "Authors:", 40, colors.BEIGE)
        self.author_surok = Text(screen, (160, 650), "surokpro", 20, colors.BEIGE)
        self.author_hadingus = Text(screen, (570, 650), "hadingus", 20, colors.BEIGE)
        self.title = Text(screen, (220, 20), "SUPER GAME", 50, colors.BLUE)
        self.surok_img = pygame.image.load("sprites/surok.jpg").convert()
        self.surok_img = pygame.transform.scale(self.surok_img, (300, 300))
        self.zhekek_img = pygame.image.load("sprites/zhekek.jpg").convert()
        self.zhekek_img = pygame.transform.scale(self.zhekek_img, (300, 300))

    def draw(self):
        self.screen.fill(colors.LIGHT_GREEN)
        self.playButton.draw()
        self.authors.draw()
        self.author_surok.draw()
        self.author_hadingus.draw()
        self.title.draw()
        surok_rect = self.surok_img.get_rect(center=(200, 500))
        zhekek_rect = self.zhekek_img.get_rect(center=(600, 500))
        self.screen.blit(self.zhekek_img, zhekek_rect)
        self.screen.blit(self.surok_img, surok_rect)

    def handle(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            position = event.pos
            if self.playButton.accepts(position):
                self.operator.state = mode_page.ModePage(self.screen, self.operator)
