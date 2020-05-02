import pygame
from gui.components import Button, Text, CheckButton
from gui.abstract import Handler, Drawable
from gui import colors
from gui.gui_operator import GuiOperator
from gui import start_page
from board import Board, valid
from gamemode import GameMode
from itertools import product

def get_pos(pos, base_len):
    return (pos - 20) // base_len


class BoardPage:
    board_len = 576
    def __init__(self, screen: pygame.Surface, operator: GuiOperator, mode: GameMode):
        self.screen = screen
        self.operator = operator
        self.board = Board(mode)
        self.elem_size = 0
        self.move_from = (None, None)
        self.active = None

    def upd_regime(self, mode: GameMode):
        self.board.reformat(mode)

    def draw(self):
        self.screen.fill(colors.SAND)
        self.draw_board()

    def handle(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_click_position = event.pos
            pos_x, pos_y = [get_pos(pos, self.elem_size) for pos in mouse_click_position]

            if valid(pos_x, pos_y, self.board.size_map) and self.board[pos_x][pos_y] is not None:
                self.move_from = [pos_x, pos_y]
                if self.board[pos_x][pos_y].player == self.board.player_A:
                    ...


        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            from_x, from_y = self.move_from
            to_x, to_y = [get_pos(pos, self.elem_size) for pos in event.pos]
            self.board.do_move(from_x, from_y, to_x, to_y)

    def draw_board(self):
        self.elem_size = BoardPage.board_len // self.board.size_map
        pos_x = 10
        pos_y = 10
        position = pos_x, pos_y, self.elem_size * self.board.size_map + 20, self.elem_size * self.board.size_map + 20
        pygame.draw.rect(self.screen, colors.DARK_BLUE, position)
        pos_x += 10
        pos_y += 10
        for x, y in product(range(self.board.size_map), range(self.board.size_map)):
            color = colors.GREY if (x + y) % 2 == 0 else colors.BLACK
            position = pos_x + x * self.elem_size, pos_y + y * self.elem_size, self.elem_size, self.elem_size
            pygame.draw.rect(self.screen, color, position)

        for x, y in product(range(self.board.size_map), range(self.board.size_map)):
            if self.board.map[x][y] is not None:
                cir_rad = self.elem_size // 2 - 5
                position = pos_x + x * self.elem_size, pos_y + y * self.elem_size, self.elem_size, self.elem_size
                if self.board.map[x][y].player == self.board.player_A:
                    figure_colour = colors.RED
                else:
                    figure_colour = colors.GREEN
                pygame.draw.circle(self.screen, figure_colour,
                                   (position[0] + self.elem_size // 2, position[1] + self.elem_size // 2), cir_rad)
