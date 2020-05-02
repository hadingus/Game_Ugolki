import pygame
from gui.components import Button, Text, CheckButton
from gui.abstract import Handler, Drawable
from gui import colors
from gui.gui_operator import GuiOperator
from gui import start_page
from board import Board
from itertools import product


class Board_page:
    def __init__(self, screen: pygame.Surface, operator: GuiOperator, board: Board):
        self.screen = screen
        self.operator = operator
        self.board = board

    def draw(self):
        self.screen.fill(colors.SAND)
        self.draw_board()

    def handle(self, event: pygame.event):
        ...

    def draw_board(self):
        board_len = 576
        elem_size = board_len // self.board.size_map
        pos_x = 10
        pos_y = 10
        position = pos_x, pos_y, elem_size * self.board.size_map + 20, elem_size * self.board.size_map + 20
        pygame.draw.rect(self.screen, colors.DARK_BLUE, position)
        pos_x += 10
        pos_y += 10
        for x, y in product(range(self.board.size_map), range(self.board.size_map)):
            color = colors.GREY if (x + y) % 2 == 0 else colors.BLACK
            position = pos_x + x * elem_size, pos_y + y * elem_size, elem_size, elem_size
            pygame.draw.rect(self.screen, color, position)

        for x, y in product(range(self.board.size_map), range(self.board.size_map)):
            if self.board.map[x][y] is not None:
                cir_rad = elem_size // 2 - 5
                position = pos_x + x * elem_size, pos_y + y * elem_size, elem_size, elem_size
                figure_colour = 0
                if self.board.map[x][y].player == self.board.player_A:
                    figure_colour = colors.RED
                else:
                    figure_colour = colors.GREEN
                pygame.draw.circle(self.screen, figure_colour,
                                   (position[0] + elem_size // 2, position[1] + elem_size // 2), cir_rad)