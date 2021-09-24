from time import time
from minions import (
    AnnoyoModule,
    BirdBuddy,
    BuddingGreenthumb,
    CracklingCyclone,
    DeckSwabbie,
    DreadAdmiralEliza,
    GentleDjinni,
    Ghastcoiler,
    GlyphGuadrdian,
    HarvestGolem,
    ImpMama,
    KangorsApprentice,
    Leapfrogger,
    MechanoEgg,
    MechanoTank,
    MicroBot,
    OmegaBuster,
    Rat,
    RipsnarlCaptain,
    SISefin,
    Sellemental,
    TonyTwoTusk,
    Voidwalker,
)
from warband import Warband
from minion import Minion
from board import Board
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
    # drag = GlyphGuadrdian()
    # drag.make_golden()
    # drag._add_stats(0, 30)
    # warband.add_minion(drag)
    warband.add_minion(Ghastcoiler())
    warband.add_minion(Ghastcoiler())
    warband.add_minion(BuddingGreenthumb())
    warband.add_minion(SISefin())
    warband.add_minion(MechanoTank())

    return warband


def setup_top():
    warband = Warband()
    # egg = ImpMama()
    # egg.make_golden()
    # warband.add_minion(egg)
    warband.add_minion(Ghastcoiler())
    warband.add_minion(Ghastcoiler())
    warband.add_minion(BirdBuddy())
    warband.add_minion(TonyTwoTusk())
    return warband


if __name__ == "__main__":
    top_warband = setup_top()
    bottom_warband = setup_bottom()
    top_warband.make_all_minions_golden()
    bottom_warband.make_all_minions_golden()
    print_boards()

    turns = []
    results = [0] * 3
    average_damage = [0] * 3
    iterations = 1_000
    bar = progressbar.ProgressBar(
        maxval=iterations,
        widgets=[
            progressbar.Bar("=", "[", "]"),
            " ",
            progressbar.Percentage(),
        ],
    )
    bar.start()
    start_time = time()

    for i in range(iterations):
        board = Board(top_warband, bottom_warband)
        outcome = board.battle()
        results[outcome[0]] += 1
        average_damage[outcome[0]] += outcome[1]
        turns.append(outcome[2])
        bar.update(i + 1)

    bar.finish()
    average_damage = [
        x / y if y > 0 and x > 0 else x for x, y in zip(average_damage, results)
    ]
    results = [(x / iterations) * 100 for x in results]
    print(f"Outcome: {results}")
    print(f"Average damage: {average_damage}")
    print(f"Average turns: {sum(turns)/iterations:.2f}")

    end_time = time()
    print(f"Turns / Time {sum(turns) / (end_time - start_time):.2f}")
