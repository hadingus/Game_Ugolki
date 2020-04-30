import pygame
from gui.components import Button, Text, CheckButton
from gui.abstract import Handler, Drawable
from gui import colors
from gui.gui_operator import GuiOperator
from gui import start_page


class ModePage(Handler, Drawable):
    def __init__(self, screen: pygame.Surface, operator: GuiOperator):
        self.screen = screen
        self.operator = operator
        self.title = Text(screen, (100, 20), "Выбор режима", 50)
        names = ['Тупой режим',
                 'Умный режим',
                 'Чилл режим',
                 'Флекс режим',
                 'Режем режим']
        self.mods = [CheckButton(screen, (100, 100 + 40 * i, 200, 30), names[i]) for i in range(len(names))]

        self.back_button = Button(screen, (400, 400, 100, 30), 'Назад')
        self.go_button = Button(screen, (100, 350, 100, 30), 'Играть!', colors.RED, colors.WHITE)

    def draw(self):
        self.screen.fill(colors.WHITE)
        self.title.draw()
        for button in self.mods:
            button.draw()

        self.back_button.draw()
        self.go_button.draw()

    def handle(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            position = event.pos
            for button in self.mods:
                if button.accepts(position):
                    button.touch()
            if self.back_button.accepts(position):
                self.operator.state = start_page.StartPage(self.screen, self.operator)
