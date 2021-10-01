from random import seed
from time import time
from minions import (
    AcolyteOfCthun,
    Alleycat,
    AnnoyoModule,
    ArmoftheEmpire,
    BirdBuddy,
    BronzeWarden,
    BuddingGreenthumb,
    CracklingCyclone,
    DeckSwabbie,
    DreadAdmiralEliza,
    EvolvingChromawing,
    GentleDjinni,
    Ghastcoiler,
    GlyphGuadrdian,
    HarvestGolem,
    ImpMama,
    Imprisoner,
    ImpulsiveTrickster,
    KangorsApprentice,
    Leapfrogger,
    MamaBear,
    MechanoEgg,
    MechanoTank,
    MicroBot,
    MonstrousMacaw,
    NomiKitchenNightmare,
    OmegaBuster,
    PartyElemental,
    Rat,
    RatPack,
    RazorfenGeomancer,
    RazorgoretheUntamed,
    RedWhelp,
    RipsnarlCaptain,
    SISefin,
    Scallywag,
    Sellemental,
    SewerRat,
    SoulJuggler,
    SpawnOfNZoth,
    StatisElemental,
    Tabbycat,
    TonyTwoTusk,
    TwilightEmissary,
    Voidwalker,
    WhelpSmuggler,
)
from test_simulator import warbands
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
    warband.add_minion(RatPack())
    warband.add_minion(StatisElemental())
    return warband


def boje():
    warband = Warband()
    warband.add_minion(GlyphGuadrdian())
    selle = Sellemental()
    selle._add_stats(1, 1)
    warband.add_minion(selle)
    warband.add_minion(Sellemental())
    warband.add_minion(Sellemental())
    warband.add_minion(PartyElemental())
    warband.add_minion(RedWhelp())


def boje_opponent():
    warband = Warband()
    warband.add_minion(Sellemental())
    warband.add_minion(Sellemental())
    warband.add_minion(AcolyteOfCthun())


def Esben1():
    warband = Warband()
    warband.add_minion(ImpulsiveTrickster())
    warband.add_minion(Imprisoner())
    razor = RazorgoretheUntamed()
    razor._add_stats(2, 2)
    warband.add_minion(razor)
    warband.add_minion(TwilightEmissary())
    juggler = SoulJuggler()
    juggler.make_golden()
    warband.add_minion(juggler)
    # 22.7 35.7 41.6


def Esben1_opp():
    warband = Warband()
    warband.add_minion(GlyphGuadrdian())
    warband.add_minion(BronzeWarden())
    selle = Sellemental()
    selle._add_stats(6, 6)
    warband.add_minion(selle)
    razor = RazorgoretheUntamed()
    razor._add_stats(4, 4)
    warband.add_minion(razor)
    warband.add_minion(PartyElemental())
    redwhelp = RedWhelp()
    redwhelp._add_stats(1, 0)


def setup_top():
    warband = Warband()
    evolve = EvolvingChromawing()
    evolve._add_stats(12, 15)
    warband.add_minion(evolve)
    selle = Sellemental()
    selle._add_stats(9, 9)
    warband.add_minion(selle)
    smuggler = WhelpSmuggler()
    smuggler._add_stats(4, 4)
    warband.add_minion(smuggler)
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
    # seed(1)
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


def execute_battles(bottom_warband: Warband, top_warband: Warband, iterations: int):
    results = [0] * 3
    for i in range(iterations):
        board = Board(bottom_warband, top_warband)
        outcome = board.battle()
        results[outcome[0]] += 1
    return [float("{0:0.2f}".format((x / iterations) * 100)) for x in results]
