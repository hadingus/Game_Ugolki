from gamemode import GameMode
from player import Player
from unit import Unit
from copy import deepcopy


def sym_coord(x, y, size):
    return size - 1 - x, size - 1 - y


def valid(x, y, board):
    return 0 <= x < board and 0 <= y < board


class Board:
    def __init__(self, mode: GameMode):
        self.current_mode = mode
        self.player_A = Player()
        self.player_B = Player()
        self.current_player = self.player_A
        self.arrange_template = []
        self.map = []
        self.size_map = 0
        self.position_of_unit = {}
        self.reformat(mode)

    def __getitem__(self, pos):
        return self.map[pos[0]][pos[1]]

    def __setitem__(self, pos, value):
        self.map[pos[0]][pos[1]] = value

    def reformat(self, mode: GameMode):
        self.current_mode = mode
        self.arrange_template = []
        self.map = []
        self.size_map = mode.size_map
        for i in range(mode.size_map):
            self.map.append([])
            for j in range(mode.size_map):
                self.map[i].append(None)
        for units in mode.arrangement:
            unit: Unit = units[0]
            unit_x = units[1]
            unit_y = units[2]
            self.arrange_template.append((unit_x, unit_y))

            self.map[unit_x][unit_y] = deepcopy(unit)
            self.map[unit_x][unit_y].set_player(self.player_A)
            self.map[unit_x][unit_y].set_board(self)
            self.position_of_unit[self.map[unit_x][unit_y]] = (unit_x, unit_y)
            unit_x, unit_y = sym_coord(unit_x, unit_y, self.size_map)
            self.map[unit_x][unit_y] = deepcopy(unit)
            self.map[unit_x][unit_y].set_player(self.player_B)
            self.map[unit_x][unit_y].set_board(self)
            self.position_of_unit[self.map[unit_x][unit_y]] = (unit_x, unit_y)

    def __deepcopy__(self, memo={}):
        new_board = Board(self.current_mode)
        for x in range(self.size_map):
            for y in range(self.size_map):
                if self.map[x][y] is None:
                    new_board.map[x][y] = None
                else:
                    new_board.map[x][y] = deepcopy(self.map[x][y])
                    if self.map[x][y].player == self.player_A:
                        new_board.map[x][y].set_player(new_board.player_A)
                    else:
                        new_board.map[x][y].set_player(new_board.player_B)
        if self.current_player == self.player_A:
            new_board.current_player = new_board.player_A
        else:
            new_board.current_player = new_board.player_B

    def is_game_finished(self):
        cnt_a = len(self.arrange_template)
        cnt_b = cnt_a
        for pos in self.arrange_template:
            x = pos[0]
            y = pos[1]
            if self.map[x][y] is not None and self.map[x][y].player == self.player_B:
                cnt_b -= 1
            x, y = sym_coord(x, y, self.size_map)
            if self.map[x][y] is not None and self.map[x][y].player == self.player_A:
                cnt_a -= 1
        if cnt_b == 0 and cnt_a == 0:
            return [self.player_A, self.player_B]
        elif cnt_b == 0:
            return self.player_B
        elif cnt_a == 0:
            return self.player_A
        else:
            return None

    def get_current_player(self):
        return self.current_player

    def get_unit(self, x, y):
        if valid(x, y, self.size_map):
            return self.map[x][y]
        return None

    def change_player(self):
        self.current_player = self.player_A if self.current_player == self.player_B else self.player_B

    def do_move(self, from_x, from_y, to_x, to_y):
        current_unit = self.map[from_x][from_y]
        if current_unit is None or self.current_player is not current_unit.player:
            return False
        if current_unit.move((to_x, to_y)):
            self.change_player()
            return True
        return False

    def do_pofig_move(self, from_x, from_y, to_x, to_y):
        current_unit = self.map[from_x][from_y]
        return current_unit.move((to_x, to_y))

    def force_move(self, from_pos, to_pos):
        fx, fy = from_pos
        tx, ty = to_pos
        current_unit = self.map[fx][fy]
        self.position_of_unit[current_unit] = (tx, ty)
        self.map[tx][ty] = current_unit
        self.map[fx][fy] = None

    def force_swap(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        unit1, unit2 = self.map[x1][y1], self.map[x2][y2]
        self.position_of_unit[unit1] = pos2
        self.position_of_unit[unit2] = pos1
        self.map[x1][y1], self.map[x2][y2] = self.map[x2][y2], self.map[x1][y1]

    def print_board(self):
        for x in range(self.size_map):
            for y in range(self.size_map):
                print(self.map[x][y], end=' ')
                if self.map[x][y] is not None:
                    if self.map[x][y].player == self.player_A:
                        print("A", end=' ')
                    else:
                        print("B", end=' ')
            print('')
