import pygame
from gui.components import Button, Text, CheckButton
from gui.abstract import Handler, Drawable
from gui import colors
from gui.gui_operator import GuiOperator
from gui import board_page
from gui import start_page
from gamemode import FlexSquareBuilder, ClassicModeBuilder, AdvancedModeBuilder, AllUnitsModeBuilder, \
    KingPoliceModeBuilder, WallModeBuilder, StupidModeBuilder, Director, AiDecorator
from AI.adapter import AiAdapter
from AI.ai import AI


class ModePage(Handler, Drawable):
    def __init__(self, screen: pygame.Surface, operator: GuiOperator):
        self.screen = screen
        self.operator = operator
        self.title = Text(screen, (100, 20), "Выбор режима", 50)
        builders = [ClassicModeBuilder(),
                    AdvancedModeBuilder(),
                    FlexSquareBuilder(),
                    KingPoliceModeBuilder(),
                    WallModeBuilder(),
                    AllUnitsModeBuilder(),
                    StupidModeBuilder()]

        director = Director()

        modes = [director.construct_game_mode(builder) for builder in builders]

        ai_mode = AiDecorator(director.construct_game_mode(FlexSquareBuilder()), AiAdapter(AI.init()))
        ai_mode.name = "Диагональные уголки с ИИ"

        modes.append(ai_mode)

        buttons = [CheckButton(screen, (100, 100 + 60 * i, 440, 45), modes[i].name) for i in range(len(modes))]

        self.mod_pairs = list(zip(buttons, modes))

        self.back_button = Button(screen, (440, 550, 100, 60), 'Назад')
        self.go_button = Button(screen, (100, 550, 180, 60), 'Играть!', colors.RED, colors.WHITE)

        self.chosen_mode = None
        self.checked_button = None

    def draw(self):
        self.screen.fill(colors.WHITE)
        self.title.draw()
        for pair in self.mod_pairs:
            pair[0].draw()

        self.back_button.draw()
        self.go_button.draw()

    def handle(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            position = event.pos
            for pair in self.mod_pairs:
                button, mode = pair
                if button.accepts(position):
                    button.touch()
                    if self.checked_button != button and self.checked_button is not None:
                        self.checked_button.off()
                    if self.checked_button == button:
                        self.checked_button = None
                        self.chosen_mode = None
                    else:
                        self.checked_button = button
                        self.chosen_mode = mode
            if self.back_button.accepts(position):
                self.operator.state = start_page.StartPage(self.screen, self.operator)
            if self.go_button.accepts(position):
                if self.chosen_mode is not None:
                    self.operator.state = board_page.BoardPage(self.screen, self.operator, self.chosen_mode)
