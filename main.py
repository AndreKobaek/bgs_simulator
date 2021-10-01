from time import time
from minions import (
    Alleycat,
    AnnoyoModule,
    ArmoftheEmpire,
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
    MamaBear,
    MechanoEgg,
    MechanoTank,
    MicroBot,
    MonstrousMacaw,
    OmegaBuster,
    Rat,
    RipsnarlCaptain,
    SISefin,
    Scallywag,
    Sellemental,
    SewerRat,
    SoulJuggler,
    SpawnOfNZoth,
    Tabbycat,
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
    warband.add_minion(MonstrousMacaw())
    SoN = SpawnOfNZoth()
    SoN.reborn = True
    warband.add_minion(SoN)
    minion1 = GlyphGuadrdian()
    minion1._add_stats(1, 1)
    warband.add_minion(minion1)
    warband.add_minion(GlyphGuadrdian())

    return warband


def setup_top():
    warband = Warband()
    warband.add_minion(Leapfrogger())
    warband.add_minion(SewerRat())
    warband.add_minion(Alleycat())
    warband.add_minion(Tabbycat())
    warband.add_minion(Tabbycat())
    warband.add_minion(Sellemental())
    warband.add_minion(Sellemental())
    return warband


if __name__ == "__main__":
    top_warband = setup_top()
    bottom_warband = setup_bottom()
    # top_warband.make_all_minions_golden()
    # bottom_warband.make_all_minions_golden()
    print_boards()

    turns = []
    results = [0] * 3
    average_damage = [0] * 3
    iterations = 10_000
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
        float("{0:0.2f}".format(x / y))
        if y > 0 and x > 0
        else float("{0:0.2f}".format(x))
        for x, y in zip(average_damage, results)
    ]
    results = [float("{0:0.2f}".format((x / iterations) * 100)) for x in results]
    print(f"Outcome: {results}")
    print(f"Average damage: {average_damage}")
    print(f"Average turns: {sum(turns)/iterations:.2f}")

    end_time = time()
    print(f"Turns / Time {sum(turns) / (end_time - start_time):.2f}")
