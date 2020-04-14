from unit import Type, Unit, FlexMover, KingMover
from enum import Enum


class CustomType(Enum):
    SUPER = 0


def test_changing_type():
    figure = Unit(FlexMover())
    assert figure.type == Type.FLEX
    figure.set_mover(KingMover())
    assert figure.type == Type.KING
    figure.type = CustomType.SUPER
    assert figure.type == CustomType.SUPER
    figure.set_mover(FlexMover(), keep_type=True)
    assert figure.type == CustomType.SUPER
    assert figure.type != Type.PAWN
