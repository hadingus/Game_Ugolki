from copy import deepcopy
from game_lib import *

a = Unit('usual', Mover())
b = Unit('flex', FlexMover())

c = deepcopy(b)

mp = {a: 1, b: 2, c: 3}

mp[a] = 4

a.mover.move(0, 0, 0)
b.mover.move(0, 0, 0)
c.mover.move(0, 0, 0)


print(mp[a])