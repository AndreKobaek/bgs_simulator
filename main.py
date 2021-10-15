from copy import deepcopy
from random import seed
from time import time
from typing import List
from minions import (
    AcolyteOfCthun,
    AggemThorncurse,
    Alleycat,
    Amalgadon,
    AnnihilanBattlemaster,
    AnnoyoModule,
    ArmoftheEmpire,
    BaronRivendare,
    BirdBuddy,
    BristlebackKnight,
    BronzeWarden,
    BuddingGreenthumb,
    CapnHoggarr,
    CaptainFlatTusk,
    CobaltScalebane,
    CracklingCyclone,
    DazzlingLightspawn,
    DeckSwabbie,
    DeflectoBot,
    DrakonidEnforcer,
    DreadAdmiralEliza,
    EvolvingChromawing,
    FreedealingGambler,
    GentleDjinni,
    Ghastcoiler,
    GlyphGuadrdian,
    HarvestGolem,
    HolyMecherel,
    IckyImp,
    ImpMama,
    ImpatientDoomsayer,
    Imprisoner,
    ImpulsiveTrickster,
    InsatiableUrzul,
    Kalecgos,
    KangorsApprentice,
    Khadgar,
    Leapfrogger,
    LilRag,
    MajordomoExecutus,
    MamaBear,
    MechanoEgg,
    MechanoTank,
    MicroBot,
    MicroMummy,
    MoltenRock,
    MonstrousMacaw,
    Murozond,
    NomiKitchenNightmare,
    NosyLooter,
    OmegaBuster,
    PartyElemental,
    PeggyBrittlebone,
    PrizedPromoDrake,
    Pupbot,
    RabidSaurolisk,
    Rat,
    RatPack,
    RazorfenGeomancer,
    RazorgoretheUntamed,
    ReanimatingRattler,
    RecyclingWraith,
    RedWhelp,
    RefreshingAnomaly,
    RipsnarlCaptain,
    SISefin,
    Scallywag,
    SelflessHero,
    Sellemental,
    SewerRat,
    SoulDevourer,
    SoulJuggler,
    SouthseaCaptian,
    SouthseaStrongarm,
    SpawnOfNZoth,
    StatisElemental,
    Tabbycat,
    Tarecgosa,
    TonyTwoTusk,
    TwilightEmissary,
    UnstableGhoul,
    Voidlord,
    Voidwalker,
    WhelpSmuggler,
    WildfireElemental,
    WrathWeaver,
    YoHoOgre,
)
from warband import Warband
from board import Board
import progressbar


def print_boards():
    print("Top board:")
    print(top_warband)
    print("")
    print("Bottom board:")
    print(bottom_warband)
    print("")


def dogdog():
    warbands = [Warband(), Warband()]
    warbands[0].add_minion(UnstableGhoul())
    warbands[0].add_minion(Scallywag())
    warbands[0].add_minion(Scallywag())
    warbands[0].add_minion(DreadAdmiralEliza().make_golden())
    warbands[0].add_minion(Khadgar(3, 3).make_golden())
    warbands[0].add_minion(Khadgar(4, 4))
    warbands[0].add_minion(BaronRivendare(4, 10))
    return warbands[0]


def dogopp():
    warbands = [Warband(), Warband()]
    warbands[1].add_minion(BronzeWarden(10, 3))
    warbands[1].add_minion(Tarecgosa(32, 30).set_ds())
    warbands[1].add_minion(PrizedPromoDrake(17, 7).set_ds())
    warbands[1].add_minion(Tarecgosa(11, 10).set_ds())
    warbands[1].add_minion(DrakonidEnforcer(11, 10).set_ds())
    warbands[1].add_minion(MicroMummy(13, 6).make_golden().set_ds().set_taunt())
    warbands[1].add_minion(AnnoyoModule())
    return warbands[1]
    # 100% loss


def dogopp2():
    warbands = [Warband(), Warband()]
    warbands[1].add_minion(OmegaBuster(24, 17).set_ds().set_taunt())
    warbands[1].add_minion(HolyMecherel(26, 13))
    warbands[1].add_minion(Pupbot(14, 6).make_golden())
    warbands[1].add_minion(OmegaBuster())
    warbands[1].add_minion(KangorsApprentice().make_golden())
    warbands[1].add_minion(BaronRivendare(3, 9))
    warbands[1].add_minion(MechanoTank(8, 3).make_golden())

    return warbands[1]


if __name__ == "__main__":
    top_warband = dogopp()
    bottom_warband = dogdog()
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
    seed(5)
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
        board = Board(top_warband, bottom_warband)
        outcome = board.battle()
        results[outcome[0]] += 1
    return [float("{0:0.2f}".format((x / iterations) * 100)) for x in results]


# 49.7 21 29.3
