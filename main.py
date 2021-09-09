from warband import Warband
from minion import Minion
from board import Board

yeti = Minion("Yeti", "Neutral", 3, 4, 5, False, False)
senjin = Minion("Senjin", "Neutral", 3, 3, 6, True, False)
holy_mackerel = Minion("Holy Mackerel", "Mech", 5, 8, 4, False, True)
sunwalker = Minion("Sunwalker", "Neutral", 4, 4, 5, True, True)
murloc_scout = Minion("Murloc Scout", "Murloc", 1, 1, 1, False, False)
gambler = Minion("Freedealing Gambler", "Pirate", 2, 3, 3, False, False)
sellemental = Minion("Sellemental", "Elemental", 1, 2, 2, False, False)
firefire = Minion("44", "Neutral", 3, 4, 4, False, False)
hydra = Minion("Hydra", "Beast", 4, 2, 4, False, False, False, 1, False, True)


def setup_demon_board():
    demon_board = Warband()
    demon_board.add_minion(Minion("Imprisoner", "Demon", 2, 3, 3, True, False))
    demon_board.add_minion(Minion("Imprisoner", "Demon", 2, 3, 3, True, False))
    demon_board.add_minion(
        Minion(
            "Soul Juggler",
            "Neutral",
            3,
            3,
            5,
            False,
            False,
            False,
            1,
            False,
            False,
            True,
            1,
        )
    )
    return demon_board


bottom_warband = setup_demon_board()

# bottom_warband.add_minion(murloc_scout)
# bottom_warband.add_minion(gambler)
# bottom_warband.add_minion(gambler)
# bottom_warband.add_minion(Minion("Sellemental", "Elemental", 1, 2, 2, False, False))
# bottom_warband.add_minion(Minion("Sellemental", "Elemental", 1, 2, 2, False, False))
# bottom_warband.add_minion(Minion("Sellemental", "Elemental", 1, 2, 2, False, False))
# bottom_warband.add_minion(sellemental)
# bottom_warband.add_minion(sellemental)


# bottom_warband.add_minion(yeti)
# bottom_warband.add_minion(senjin)


top_warband = Warband()
top_warband.add_minion(Minion("Sellemental", "Elemental", 1, 5, 12, False, False))
# top_warband.add_minion(firefire)
# top_warband.add_minion(sunwalker)
# top_warband.add_minion(murloc_scout)
# top_warband.add_minion(hydra)

# top_warband.add_minion(sunwalker)
# top_warband.add_minion(senjin)
# top_warband.add_minion(yeti)


# bottom_warband.add_minion(holy_mackerel)

print("Top board:")
print(top_warband)
print("")
print("Bottom board")
print(bottom_warband)
print("")
results = [0] * 3
average_damage = [0] * 3
iterations = 1
for _ in range(iterations):
    board = Board(top_warband, bottom_warband)
    outcome = board.battle()
    results[outcome[0]] += 1
    average_damage[outcome[0]] += outcome[1]

average_damage = [
    x / y if y > 0 and x > 0 else x for x, y in zip(average_damage, results)
]
results = [(x / iterations) * 100 for x in results]
print(f"Outcome: {results}")
print(f"Average damage: {average_damage}")
