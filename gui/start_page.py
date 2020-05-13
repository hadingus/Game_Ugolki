import pygame
from gui.components import Button, Text
from gui.abstract import Handler, Drawable
from gui import colors
from gui.gui_operator import GuiOperator
from gui import mode_page
import webbrowser


class Photo(Drawable, Handler):
    width = 300

    def __init__(self, screen: pygame.Surface, path_to_image: str, center, link: str):
        self.screen = screen
        self.path_to_image = path_to_image
        self.center = center
        self.img = pygame.image.load(self.path_to_image).convert()
        self.img = pygame.transform.scale(self.img, (self.width, self.width))
        self.link = link

    def draw(self):
        rect = self.img.get_rect(center=self.center)
        self.screen.blit(self.img, rect)

    def handle(self, event: pygame.event):
        position = event.pos
        lx, rx = self.center[0] - self.width // 2, self.center[0] + self.width // 2
        ly, ry = self.center[1] - self.width // 2, self.center[1] + self.width // 2
        x, y = position
        if lx <= x <= rx and ly <= y <= ry:
            webbrowser.open(self.link)


class StartPage(Handler, Drawable):
    def __init__(self, screen: pygame.Surface, operator: GuiOperator):
        self.screen = screen
        self.operator = operator
        self.playButton = Button(screen, (180, 70, 500, 250), "PLAY", colors.LIGHT_GREEN, colors.RED)
        self.authors = Text(screen, (340, 300), "Authors:", 40, colors.BEIGE)
        self.author_surok = Text(screen, (160, 650), "surokpro", 20, colors.BEIGE)
        self.author_hadingus = Text(screen, (570, 650), "hadingus", 20, colors.BEIGE)
        self.title = Text(screen, (220, 20), "SUPER GAME", 50, colors.BLUE)
        self.surok = Photo(self.screen, "sprites/surok.jpg", (200, 500), "https://github.com/surkovv/")
        self.zhekek = Photo(self.screen, "sprites/zhekek.jpg", (600, 500), "https://github.com/hadingus/")

    def draw(self):
        self.screen.fill(colors.LIGHT_GREEN)
        self.playButton.draw()
        self.authors.draw()
        self.author_surok.draw()
        self.author_hadingus.draw()
        self.title.draw()
        self.surok.draw()
        self.zhekek.draw()

    def handle(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            position = event.pos
            if self.playButton.accepts(position):
                self.operator.state = mode_page.ModePage(self.screen, self.operator)

            self.surok.handle(event)
            self.zhekek.handle(event)
