from warband import Warband
from minion import Minion
from board import Board

yeti = Minion("Yeti", 4, 5, False, False)
senjin = Minion("Senjin", 3, 6, True, False)
holy_mackerel = Minion("Holy Mackerel", 8, 4, False, True)
sunwalker = Minion("Sunwalker", 4, 5, True, True)
whisp = Minion("Whisp", 1, 1, False, False)
tretre = Minion("33", 3, 3, False, False)
toto = Minion("22", 2, 2, False, False)
firefire = Minion("44", 4, 4, False, False)

bottom_warband = Warband()
bottom_warband.add_minion(tretre)
bottom_warband.add_minion(toto)


# bottom_warband.add_minion(yeti)
# bottom_warband.add_minion(whisp)
# bottom_warband.add_minion(senjin)


top_warband = Warband()
top_warband.add_minion(firefire)
# top_warband.add_minion(sunwalker)
top_warband.add_minion(whisp)
# top_warband.add_minion(sunwalker)
# top_warband.add_minion(senjin)
# top_warband.add_minion(yeti)


# bottom_warband.add_minion(holy_mackerel)


board = Board(top_warband, bottom_warband)
results = [0] * 3
for _ in range(10):
    # print(f"Top:\n{top_warband}")
    # print(f"Bottom:\n{bottom_warband}")
    results[board.battle()] += 1

print(results)
