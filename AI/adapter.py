from AI import boardstate, ai
from board import Board
from itertools import product


class AiAdapter:
    size = 8

    def __init__(self, external_ai: ai.AI):
        self.external_ai = external_ai

    def get_step(self, board: Board):
        board_state = boardstate.BoardState.initial_state()
        for i, j in product(range(self.size), range(self.size)):
            current_cell = board.map[i][j]
            if current_cell is None:
                board_state.board[i, j] = 0
            elif current_cell.player is board.player_A:
                board_state.board[i, j] = 1
            elif current_cell.player is board.player_B:
                board_state.board[i, j] = -1
            else:
                assert False
        board_state.current_player = 1 if board.current_player == board.player_A else -1
        new_board_state = self.external_ai.next_move(board_state)
        result = boardstate.BoardState.get_diff(new_board_state, board_state)
        return result
