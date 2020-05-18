from typing import Optional

from .boardstate import BoardState

from itertools import product

import numpy as np


class PositionEvaluation:
    values = [
        [-4, -3, -2, 1, 1, 1, 0, 0],
        [-3, -2, -1, 3, 3, 2, 1, 1],
        [-2, -1, 0, 3, 5, 4, 1, 1],
        [1, 3, 3, 3, 6, 6, 6, 4],
        [1, 3, 5, 6, 8, 8, 8, 8],
        [1, 2, 4, 6, 8, 10, 11, 11],
        [0, 1, 1, 6, 8, 11, 12, 12],
        [0, 1, 1, 4, 8, 11, 12, 14]
    ]

    def __call__(self, board: BoardState) -> float:
        my_board = board if board.current_player == 1 else board.inverted()
        enemy_board = my_board.inverted()

        if board.is_game_finished:
            winner = board.winner
            if winner == board.current_player:
                return 10000
            elif winner == -board.current_player:
                return -10000
            else:
                return 0

        result = 0
        my_min = 100
        enemy_min = 100
        for x, y in product(range(8), range(8)):
            if my_board.board[x, y] == 1:
                my_min = min(my_min, self.values[x][y])
                result += self.values[x][y]
            if enemy_board.board[x, y] == 1:
                enemy_min = min(enemy_min, self.values[x][y])
                result -= self.values[x][y]

        result += my_min * 1
        result -= enemy_min * 1
        return result


class AI:
    def __init__(self, position_evaluation: PositionEvaluation, search_depth: int):
        self.position_evaluation: PositionEvaluation = position_evaluation
        self.depth: int = search_depth
        self.first_check = 5

    @staticmethod
    def init():
        return AI(PositionEvaluation(), 3)

    # @timeLimit(2)
    def next_move(self, board: BoardState) -> Optional[BoardState]:
        result = self._minimax(self.depth, board)
        return result[1]

    def _minimax(self, depth, state: BoardState):
        if state.is_game_finished:
            return self.position_evaluation(state), state

        if depth == 0:
            return self.position_evaluation(state), state

        moves = state.possible_moves
        moves.sort(key=self.position_evaluation)
        answer = None

        for i in range(min(len(moves), self.first_check)):
            move = moves[i]
            tmp = self._minimax(depth - 1, move)
            if answer is None or answer[0] < -tmp[0]:
                answer = tmp[0] * -1, move

        return answer