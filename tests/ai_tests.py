from AI.adapter import AiAdapter
from AI.ai import AI
from board import Board
from gamemode import FlexSquareBuilder, Director, AiDecorator, ModeFeature


def test_adapter():
    mode = Director().construct_game_mode(FlexSquareBuilder())
    board = Board(mode)
    adapter = AiAdapter(AI.init())

    move = adapter.get_step(board)
    assert move[:2] != move[2:]
    assert abs(move[0] - move[2]) <= 2 and abs(move[1] - move[3])

    assert board.do_move(*move) is True


def test_decorator():
    mode = Director().construct_game_mode(FlexSquareBuilder())
    adapter = AiAdapter(AI.init())
    new_mode = AiDecorator(mode, adapter)
    assert hasattr(new_mode, 'ai')
    assert ModeFeature.AI in new_mode.features
