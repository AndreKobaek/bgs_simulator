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
    DreadAdmiralEliza,
    EvolvingChromawing,
    FreedealingGambler,
    GentleDjinni,
    Ghastcoiler,
    GlyphGuadrdian,
    HarvestGolem,
    IckyImp,
    ImpMama,
    ImpatientDoomsayer,
    Imprisoner,
    ImpulsiveTrickster,
    InsatiableUrzul,
    Kalecgos,
    KangorsApprentice,
    Leapfrogger,
    LilRag,
    MajordomoExecutus,
    MamaBear,
    MechanoEgg,
    MechanoTank,
    MicroBot,
    MoltenRock,
    MonstrousMacaw,
    Murozond,
    NomiKitchenNightmare,
    NosyLooter,
    OmegaBuster,
    PartyElemental,
    PeggyBrittlebone,
    PrizedPromoDrake,
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
    return warband


def boje_opponent():
    warband = Warband()
    warband.add_minion(Sellemental())
    warband.add_minion(Sellemental())
    warband.add_minion(AcolyteOfCthun())
    return warband


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
    return warband


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
    return warband


def Esben2():
    warbands: List[Warband] = [Warband(), Warband()]
    party1 = PartyElemental()
    party1.make_golden()
    party1._add_stats(8, 8)
    warbands[0].add_minion(party1)
    selle = Sellemental()
    selle._add_stats(11, 11)
    warbands[0].add_minion(selle)
    party2 = PartyElemental()
    party2._add_stats(5, 5)
    warbands[0].add_minion(party2)
    warbands[0].add_minion(MajordomoExecutus())
    refresh = RefreshingAnomaly()
    refresh._add_stats(4, 4)
    warbands[0].add_minion(refresh)
    molten = MoltenRock()
    molten._add_stats(7, 7)
    warbands[0].add_minion(molten)
    warbands[0].add_minion(NomiKitchenNightmare())
    return warbands[0]


def Esben_opp2():
    warbands: List[Warband] = [Warband(), Warband()]
    SoN = SpawnOfNZoth()
    SoN.make_golden()
    warbands[1].add_minion(SoN)
    wfe = WildfireElemental()
    wfe._add_stats(4, 4)
    warbands[1].add_minion(wfe)
    peggy = PeggyBrittlebone()
    peggy._add_stats(3, 3)
    warbands[1].add_minion(peggy)
    hog1 = CapnHoggarr()
    hog1._add_stats(5, 5)
    warbands[1].add_minion(hog1)
    hog2 = CapnHoggarr()
    hog2._add_stats(18, 18)
    warbands[1].add_minion(hog2)
    ss = SouthseaStrongarm()
    ss._add_stats(1, 1)
    warbands[1].add_minion(ss)
    warbands[1].add_minion(SouthseaCaptian())
    return warbands[1]


def andre_søn():
    warbands = [Warband(), Warband()]
    warbands[1].add_minion(MonstrousMacaw())
    warbands[1].add_minion(Leapfrogger())
    warbands[1].add_minion(Leapfrogger(5, 5).make_golden().set_reborn())
    warbands[1].add_minion(ReanimatingRattler())
    warbands[1].add_minion(RabidSaurolisk(12, 19))
    warbands[1].add_minion(BaronRivendare())
    warbands[1].add_minion(InsatiableUrzul(12, 16))
    return warbands[1]


def oliver_søn():
    warbands = [Warband(), Warband()]
    warbands[0].add_minion(MonstrousMacaw())
    warbands[0].add_minion(OmegaBuster())
    warbands[0].add_minion(Amalgadon(9, 6).set_poisonous().set_windfury())
    warbands[0].add_minion(NosyLooter())
    warbands[0].add_minion(MechanoTank())
    warbands[0].add_minion(MechanoTank())
    warbands[0].add_minion(BaronRivendare())

    return warbands[0]


def boje_søn():
    warbands = [Warband(), Warband()]
    warbands[1].add_minion(MonstrousMacaw())
    warbands[1].add_minion(MonstrousMacaw())
    warbands[1].add_minion(OmegaBuster())
    warbands[1].add_minion(DeflectoBot())
    warbands[1].add_minion(BaronRivendare())
    warbands[1].add_minion(DeflectoBot())
    warbands[1].add_minion(AcolyteOfCthun(6, 2).make_golden())
    return warbands[1]


def esben_søn():
    warbands = [Warband(), Warband()]
    warbands[0].add_minion(Scallywag())
    warbands[0].add_minion(Scallywag(3, 2).set_taunt())
    warbands[0].add_minion(Scallywag(13, 16).make_golden().set_taunt())
    warbands[0].add_minion(TonyTwoTusk(14, 51))
    warbands[0].add_minion(PeggyBrittlebone())
    warbands[0].add_minion(DreadAdmiralEliza().make_golden())
    warbands[0].add_minion(BaronRivendare())
    return warbands[0]


def esben_ny():
    warbands = [Warband(), Warband()]
    warbands[0].add_minion(RazorfenGeomancer().set_reborn())
    return warbands[0]


def oli():
    warbands = [Warband(), Warband()]
    warbands[1].add_minion(RefreshingAnomaly())
    return warbands[1]


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
    # top_warband = setup_top()
    # bottom_warband = setup_bottom()
    top_warband = esben_ny()
    bottom_warband = oli()
    # top_warband.make_all_minions_golden()
    # bottom_warband.make_all_minions_golden()
    print_boards()

    turns = []
    results = [0] * 3
    average_damage = [0] * 3
    iterations = 1  # _000
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
