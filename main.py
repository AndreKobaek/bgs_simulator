from random import seed
from time import time
from math import factorial
from typing import List
from statistics import quantiles
from itertools import permutations
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
    CaveHydra,
    CobaltScalebane,
    ColdlightSeer,
    CracklingCyclone,
    DazzlingLightspawn,
    DeckSwabbie,
    DefenderofArgus,
    DeflectoBot,
    DrakonidEnforcer,
    DreadAdmiralEliza,
    EvolvingChromawing,
    FreedealingGambler,
    GentleDjinni,
    Ghastcoiler,
    GlyphGuadrdian,
    GoldrintheGreatWolf,
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
    MurlocTidehunter,
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
    Swolefin,
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


def print_boards(top_warband: Warband, bottom_warband: Warband):
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


def dogdog_perm_test():
    warband = Warband()
    warband.add_minion(MonstrousMacaw().set_reborn())
    warband.add_minion(GoldrintheGreatWolf(5, 5).set_taunt().set_reborn())
    warband.add_minion(CaveHydra())
    warband.add_minion(CaveHydra())
    warband.add_minion(DefenderofArgus())
    warband.add_minion(BaronRivendare())
    warband.add_minion(GoldrintheGreatWolf(5, 5).set_taunt())
    return warband


def dogdog_perm_test_2():
    warband = Warband()
    warband.add_minion(MonstrousMacaw().set_reborn())
    warband.add_minion(CaveHydra())
    warband.add_minion(CaveHydra())
    warband.add_minion(GoldrintheGreatWolf(5, 5).set_taunt().set_reborn())
    warband.add_minion(BaronRivendare())
    warband.add_minion(DefenderofArgus())
    warband.add_minion(GoldrintheGreatWolf(5, 5).set_taunt())
    return warband


def dogdog_perm_opp_test():
    warband = Warband()
    warband.add_minion(ColdlightSeer(3, 12).set_poisonous())
    warband.add_minion(Swolefin(56, 55).set_poisonous())
    warband.add_minion(MurlocTidehunter(6, 30).set_poisonous())
    warband.add_minion(MurlocTidehunter(9, 25).set_poisonous())
    warband.add_minion(Swolefin(26, 24).set_poisonous())
    warband.add_minion(SISefin(10, 42).set_poisonous())
    warband.add_minion(Swolefin(16, 8))
    return warband


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


def setup_progress_bar(iterations: int):
    return progressbar.ProgressBar(
        maxval=iterations,
        widgets=[
            progressbar.Bar("=", "[", "]"),
            " ",
            progressbar.Percentage(),
        ],
    )


def standard_setup():
    top_warband = dogdog_perm_opp_test()
    bottom_warband = dogdog_perm_test_2()
    print_boards(top_warband, bottom_warband)

    turns = []
    results = [0] * 3
    average_damage = [0] * 3
    iterations = 1_000
    bar = setup_progress_bar(iterations)
    bar.start()
    start_time = time()
    # seed(5)
    top_warband_damage = []
    bottom_warband_damage = []
    for i in range(iterations):
        board = Board(top_warband, bottom_warband)
        outcome = board.battle()
        results[outcome[0]] += 1
        if outcome[0] != 1:
            if outcome[0] == 0:
                bottom_warband_damage.append(outcome[1])
            elif outcome[0] == 2:
                top_warband_damage.append(outcome[1])
        turns.append(outcome[2])
        bar.update(i + 1)

    bar.finish()
    quantiles_bot = []
    if bottom_warband_damage != []:
        quantiles_bot = [round(q, 1) for q in quantiles(bottom_warband_damage, n=5)]
    quantiles_top = []
    if top_warband_damage != []:
        quantiles_top = [round(q, 1) for q in quantiles(top_warband_damage, n=5)]
    average_damage = [
        float("{0:0.2f}".format(x / y))
        if y > 0 and x > 0
        else float("{0:0.2f}".format(x))
        for x, y in zip(average_damage, results)
    ]
    results = [float("{0:0.2f}".format((x / iterations) * 100)) for x in results]
    print(f"Outcome: {results}")
    print(f"Average damage: {average_damage}")
    print(
        f"Quantiles: {quantiles_bot[1] if quantiles_bot != [] else ' - '} - {quantiles_bot[3] if quantiles_bot != [] else ''} // {' - ' if quantiles_top == [] else quantiles_top[1]} - {'' if quantiles_top == [] else quantiles_top[3]}"
    )
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


def calculate_best_warband_permutation(warbands: List[Warband], iterations: int):
    best_result: int = 0
    prog_bar = setup_progress_bar(iterations * factorial(len(warbands[0].minions)))
    prog_bar.start()
    k = 0
    seed(1)
    for minion_permutation in permutations(warbands[0].minions):
        results = [0] * 3
        # average_damage = [0] * 3
        # start_time = time()
        bottom_warband = Warband(list(minion_permutation))
        for i in range(iterations):
            board = Board(warbands[1], bottom_warband)
            outcome = board.battle()
            results[outcome[0]] += 1
            if results[0] + (iterations - i) < best_result and k != 0:
                break
            # check if permutation is better asap
            # save permutation if better.
            prog_bar.update(i + k + 1)
        if results[0] > best_result:
            best_result = results[0]
            best_permutation = bottom_warband
        k += iterations + 1
    print()
    print(float("{0:0.2f}".format((best_result / iterations) * 100)))
    print(best_permutation)


if __name__ == "__main__":
    json_obj = Warband([Sellemental(), Leapfrogger(), WrathWeaver()]).toJSON()
    warband = Warband()
    warband.from_JSON(json_obj)
    print(warband.minions)
    # standard_setup()
    # calculate_best_warband_permutation(
    #     [dogdog_perm_test(), dogdog_perm_opp_test()], 250
    # )
