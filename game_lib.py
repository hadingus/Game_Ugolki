import copy


class Unit:
    __next_id = 0

    def __init__(self, category, mover):
        self.id = Unit.__next_id
        self.type = category
        self.mover = mover

    def __copy__(self):
        new_unit = self.__class__(self.type, self.mover)
        new_unit.__dict__.update(self.__dict__)
        new_unit.mover = copy.copy(self.mover)
        return new_unit

    def __deepcopy__(self, memo={}):
        new_unit = self.__class__(self.type, self.mover)
        new_unit.__dict__.update(self.__dict__)
        new_unit.mover = copy.deepcopy(self.mover, memo)
        return new_unit

    def __hash__(self):
        return hash(id)


class Cell:
    def __init__(self, state):
        self.state = state


class Mover:
    def move(self, unit, board, position):
        print('I am standard mover')


class FlexMover(Mover):
    def move(self, unit, board, position):
        print('Hehehehe')