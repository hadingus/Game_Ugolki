import pygame
import pygame.gfxdraw
from gui.components import Button, Text
from gui import colors
from gui.gui_operator import GuiOperator
from gui.abstract import Handler, Drawable
from gui import start_page
from board import Board, valid
from gamemode import GameMode
from itertools import product
from gui import mode_page
from gui.unit_drawer import DefaultDrawer


def get_pos(pos, base_len):
    return (pos - 20) // base_len


class BoardPage(Handler, Drawable):
    board_len = 576
    unit_color = dict(PAWN=colors.SADDLEBROWN, USUAL=colors.YELLOW, FLEX=colors.DARK_BLUE, POLICE=colors.BLACK,
                      KING=colors.PURPLE, CHECKERS_KING=colors.PINK, SNAKE=colors.DRIED_MUSTARD,
                      BISHOP=colors.AQUAMARINE, SWAP=colors.SANGRIA, ROOK=colors.SEMI_WHITE)

    unit_name = dict(PAWN='Пешка', USUAL='Обычная фигура', FLEX='Флекс-фигура', POLICE='Полицейский',
                     KING='Король', CHECKERS_KING='Дамка', SNAKE='Змейка',
                     BISHOP='Слон', SWAP='Vengeful Spirit', ROOK='Ладья')

    def __init__(self, screen: pygame.Surface, operator: GuiOperator, mode: GameMode):
        self.screen = screen
        self.operator = operator
        self.board = Board(mode)
        self.elem_size = 0
        self.active_pos = None
        self.move_pos = None
        self.change_button = Button(screen, (15, 615, 300, 50), "Change regime", colors.KHAKI, colors.DARK_BLUE)
        self.back_button = Button(screen, (420, 615, 350, 50), "Back to main menu", colors.KHAKI, colors.DARK_BLUE)

    def upd_regime(self, mode: GameMode):
        self.board.reformat(mode)

    def draw(self):
        self.screen.fill(colors.SAND)
        self.draw_board()
        self.back_button.draw()
        self.change_button.draw()
        self.draw_color_exp()

    def draw_color_exp(self):
        pos_y = 10
        for key in BoardPage.unit_color:
            position = 620, pos_y, 220, 50
            pygame.draw.rect(self.screen, colors.KHAKI, position)
            position_col = 625, pos_y + 5, 40, 40
            pygame.draw.rect(self.screen, BoardPage.unit_color[key], position_col)
            pos_text = 670, pos_y + 10
            Text(self.screen, pos_text, BoardPage.unit_name[key], 20).draw()
            pos_y += 60

    def handle(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_click_position = event.pos
            pos_x, pos_y = [get_pos(pos, self.elem_size) for pos in mouse_click_position]

            if self.active_pos is None:
                if valid(pos_x, pos_y, self.board.size_map) and self.board[pos_x, pos_y] is not None:
                    self.active_pos = (pos_x, pos_y)
            else:
                if self.board.do_move(*self.active_pos, pos_x, pos_y) or self.active_pos == (pos_x, pos_y):
                    self.active_pos = None
                elif valid(pos_x, pos_y, self.board.size_map):
                    if self.board[pos_x, pos_y] is not None:
                        self.active_pos = (pos_x, pos_y)

            if self.change_button.accepts(event.pos):
                self.operator.state = mode_page.ModePage(self.screen, self.operator)
            elif self.back_button.accepts(event.pos):
                self.operator.state = start_page.StartPage(self.screen, self.operator)

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
            if self.board[x, y] is not None:
                position = pos_x + x * self.elem_size, pos_y + y * self.elem_size, self.elem_size, self.elem_size
                active = (x, y) == self.active_pos
                color = BoardPage.unit_color[self.board[x, y].type.name]
                self._draw_unit(self.board[x, y], position, active, color)

    def _draw_unit(self, unit, position, active, color):
        type = unit.player == self.board.player_A
        DefaultDrawer(self.screen).draw_unit(type, active, position, self.elem_size, color)
