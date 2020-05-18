import pygame
from gui.gui_operator import GuiOperator
from gui.start_page import StartPage


class App:
    def start(self):
        pygame.init()
        screen = pygame.display.set_mode([850, 700])

        pygame.display.flip()

        operator = GuiOperator()
        startPage = StartPage(screen, operator)
        operator.state = startPage

        working = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    working = False
                    break
                operator.state.handle(event)
                operator.state.draw()
                pygame.display.flip()
            if not working:
                break
