from minions import (
    AnnoyoModule,
    CracklingCyclone,
    GentleDjinni,
    Ghastcoiler,
    HarvestGolem,
    KangorsApprentice,
    Leapfrogger,
    MicroBot,
    OmegaBuster,
    Rat,
    Sellemental,
    Voidwalker,
)
from warband import Warband
from minion import Minion
from board import Board
from copy import deepcopy
import progressbar


def print_boards():
    print("Top board:")
    print(top_warband)
    print("")
    print("Bottom board:")
    print(bottom_warband)
    print("")


def setup_bottom():
    warband = Warband()
    warband.add_minion(Ghastcoiler())
    warband.add_minion(Ghastcoiler())
    return warband


def setup_top():
    warband = Warband()
    warband.add_minion(Ghastcoiler())
    warband.add_minion(Ghastcoiler())
    return warband


if __name__ == "__main__":
    top_warband = setup_top()
    bottom_warband = setup_bottom()
    top_warband.make_all_minions_golden()
    bottom_warband.make_all_minions_golden()
    print_boards()

    results = [0] * 3
    average_damage = [0] * 3
    iterations = 100
    bar = progressbar.ProgressBar(
        maxval=iterations,
        widgets=[
            progressbar.Bar("=", "[", "]"),
            " ",
            progressbar.Percentage(),
        ],
    )
    bar.start()

    for i in range(iterations):
        board = Board(top_warband, bottom_warband)
        outcome = board.battle()
        results[outcome[0]] += 1
        average_damage[outcome[0]] += outcome[1]
        bar.update(i + 1)

    bar.finish()
    average_damage = [
        x / y if y > 0 and x > 0 else x for x, y in zip(average_damage, results)
    ]
    results = [(x / iterations) * 100 for x in results]
    print(f"Outcome: {results}")
    print(f"Average damage: {average_damage}")
