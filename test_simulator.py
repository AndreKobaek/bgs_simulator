from copy import deepcopy
from random import seed
from typing import List
import pytest
from board import Board, register_observers
from main import execute_battles
from minion import on_death
from minions import (
    AcolyteOfCthun,
    AggemThorncurse,
    Alleycat,
    Amalgadon,
    AnnihilanBattlemaster,
    AnnoyoModule,
    ArmoftheEmpire,
    BaronRivendare,
    BristlebackKnight,
    CapnHoggarr,
    CaptainFlatTusk,
    CobaltScalebane,
    CracklingCyclone,
    DazzlingLightspawn,
    DreadAdmiralEliza,
    FreedealingGambler,
    Ghastcoiler,
    GlyphGuadrdian,
    IckyImp,
    ImpMama,
    ImpatientDoomsayer,
    ImpulsiveTrickster,
    InsatiableUrzul,
    Kalecgos,
    KangorsApprentice,
    Leapfrogger,
    LilRag,
    MajordomoExecutus,
    MoltenRock,
    MonstrousMacaw,
    Murozond,
    NomiKitchenNightmare,
    PartyElemental,
    PeggyBrittlebone,
    PrizedPromoDrake,
    RabidSaurolisk,
    RazorfenGeomancer,
    RazorgoretheUntamed,
    ReanimatingRattler,
    RecyclingWraith,
    RefreshingAnomaly,
    RipsnarlCaptain,
    Scallywag,
    SelflessHero,
    Sellemental,
    SewerRat,
    SoulDevourer,
    SouthseaCaptian,
    SouthseaStrongarm,
    SpawnOfNZoth,
    Tabbycat,
    Tarecgosa,
    TonyTwoTusk,
    TwilightEmissary,
    Voidlord,
    WildfireElemental,
    WrathWeaver,
)
from warband import Warband, get_highest_health_minion


@pytest.fixture
def warbands() -> List[Warband]:
    return [Warband(), Warband()]


def test_get_highest_health_minion_highest():
    minions = [Sellemental(), Scallywag(), GlyphGuadrdian()]
    assert get_highest_health_minion(minions) == minions[2]


def test_get_highest_health_minion_none():
    minions = []
    assert get_highest_health_minion(minions) is None


def test_case_1(warbands: List[Warband]):
    warbands[0].add_minion(RazorfenGeomancer().set_reborn())
    warbands[1].add_minion(RefreshingAnomaly())
    board = Board(warbands[0], warbands[1])
    assert board.battle() == [1, 0, 2]


def test_case_2(warbands: List[Warband]):
    warbands[0].add_minion(SpawnOfNZoth().set_reborn())
    warbands[0].add_minion(GlyphGuadrdian(3, 5))
    warbands[1].add_minion(Sellemental(7, 7))
    board = Board(warbands[0], warbands[1])
    # needs accumulated results and bounds


def test_case_3(warbands: List[Warband]):
    warbands[0].add_minion(Scallywag())
    warbands[0].add_minion(RipsnarlCaptain())
    warbands[1].add_minion(Sellemental(7, 11))
    board = Board(warbands[0], warbands[1])
    assert board.battle() == [1, 0, 2]


def test_case_4(warbands: List[Warband]):
    warbands[0].add_minion(MonstrousMacaw())
    warbands[0].add_minion(SpawnOfNZoth().set_reborn())
    warbands[0].add_minion(GlyphGuadrdian(3, 5))
    warbands[0].add_minion(GlyphGuadrdian())

    warbands[1].add_minion(Leapfrogger())
    warbands[1].add_minion(SewerRat())
    warbands[1].add_minion(Alleycat())
    warbands[1].add_minion(Tabbycat())
    warbands[1].add_minion(Tabbycat())
    warbands[1].add_minion(Sellemental())
    warbands[1].add_minion(Sellemental())
    seed(1)
    results = execute_battles(warbands[0], warbands[1], 1_000)
    assert results == [95.9, 3.0, 1.1], "Results were not as expected"


def test_case_5(warbands: List[Warband]):
    warbands[0].add_minion(SpawnOfNZoth().set_reborn())
    warbands[0].add_minion(GlyphGuadrdian(3, 5))

    warbands[1].add_minion(NomiKitchenNightmare(5, 5))
    warbands[1].add_minion(RazorfenGeomancer())

    seed(1)
    results = execute_battles(warbands[0], warbands[1], 1_000)
    assert results == [51.0, 49.0, 0.0], "Results were not as expected"


def test_case_6(warbands: List[Warband]):
    warbands[0].add_minion(GlyphGuadrdian())
    warbands[0].add_minion(FreedealingGambler())
    warbands[0].add_minion(PartyElemental())
    warbands[0].add_minion(Scallywag())

    warbands[1].add_minion(IckyImp(7, 4))
    warbands[1].add_minion(RefreshingAnomaly(5, 6))
    warbands[1].add_minion(RefreshingAnomaly(5, 6))
    warbands[1].add_minion(Sellemental())
    warbands[1].add_minion(AcolyteOfCthun())

    results = execute_battles(warbands[0], warbands[1], 1_000)
    assert results == [0.0, 0.0, 100.0], "Results were not as expected"


def test_case_7(warbands: List[Warband]):
    warbands[0].add_minion(PartyElemental(11, 10).make_golden())
    warbands[0].add_minion(Sellemental(13, 13))
    warbands[0].add_minion(PartyElemental(8, 7))
    warbands[0].add_minion(MajordomoExecutus())
    warbands[0].add_minion(RefreshingAnomaly(5, 8))
    warbands[0].add_minion(MoltenRock(9, 11))
    warbands[0].add_minion(NomiKitchenNightmare())

    warbands[1].add_minion(SpawnOfNZoth().make_golden())
    warbands[1].add_minion(WildfireElemental(11, 8))
    warbands[1].add_minion(PeggyBrittlebone(9, 8))
    warbands[1].add_minion(CapnHoggarr(11, 11))
    warbands[1].add_minion(CapnHoggarr(24, 24))
    warbands[1].add_minion(SouthseaStrongarm(5, 4))
    warbands[1].add_minion(SouthseaCaptian())

    seed(1)
    results = execute_battles(warbands[0], warbands[1], 1_000)
    assert results == [0.5, 5.9, 93.6], "Results were not as expected"


def test_case_8(warbands: List[Warband]):
    warbands[0].add_minion(Scallywag())
    warbands[0].add_minion(Scallywag(3, 2).set_taunt())
    warbands[0].add_minion(Scallywag(13, 16).make_golden().set_taunt())
    warbands[0].add_minion(TonyTwoTusk(14, 51))
    warbands[0].add_minion(PeggyBrittlebone())
    warbands[0].add_minion(DreadAdmiralEliza().make_golden())
    warbands[0].add_minion(BaronRivendare())

    warbands[1].add_minion(MonstrousMacaw())
    warbands[1].add_minion(Leapfrogger())
    warbands[1].add_minion(Leapfrogger(5, 5).make_golden().set_reborn())
    warbands[1].add_minion(ReanimatingRattler())
    warbands[1].add_minion(RabidSaurolisk(12, 19))
    warbands[1].add_minion(BaronRivendare())
    warbands[1].add_minion(InsatiableUrzul(12, 16))

    results = execute_battles(warbands[0], warbands[1], 1_000)
    assert results == [100.0, 0.0, 0.0], "Results were not as expected"


def test_case_9(warbands: List[Warband]):
    # https://youtu.be/uLWnl2_KZCo?t=783
    # [56.9, 26.6, 16.5]

    warbands[0].add_minion(RazorgoretheUntamed(29, 25))
    warbands[0].add_minion(CobaltScalebane(10, 7))
    warbands[0].add_minion(PrizedPromoDrake(7, 7))
    warbands[0].add_minion(Kalecgos(8, 16))
    warbands[0].add_minion(Murozond(8, 8))
    warbands[0].add_minion(CobaltScalebane(10, 7))
    warbands[0].add_minion(TwilightEmissary(8, 5))

    warbands[1].add_minion(WrathWeaver(31, 33))
    warbands[1].add_minion(InsatiableUrzul(22, 23))
    warbands[1].add_minion(SoulDevourer(10, 10))
    warbands[1].add_minion(Voidlord())
    warbands[1].add_minion(ImpMama())
    warbands[1].add_minion(Voidlord())
    warbands[1].add_minion(ImpatientDoomsayer())
    seed(1)
    results = execute_battles(warbands[0], warbands[1], 1_000)
    assert results == [57.5, 25.1, 17.4], "Results were not as expected"


def test_case_10(warbands: List[Warband]):
    # https://youtu.be/uLWnl2_KZCo?t=1114
    # [74.9, 13.4, 11.7]

    warbands[0].add_minion(CracklingCyclone(31, 28))
    warbands[0].add_minion(RecyclingWraith(20, 19))
    warbands[0].add_minion(LilRag(9, 9))
    warbands[0].add_minion(DazzlingLightspawn(9, 10))
    warbands[0].add_minion(MoltenRock(77, 84))
    warbands[0].add_minion(AnnihilanBattlemaster(28, 22).set_taunt())
    warbands[0].add_minion(PartyElemental(18, 11).make_golden().set_taunt())

    amal = Amalgadon(8, 8).set_taunt()
    amal.death_rattles = [amal.amalgadon_deathrattle]
    warbands[1].add_minion(amal)
    warbands[1].add_minion(Kalecgos(17, 31))
    warbands[1].add_minion(PrizedPromoDrake(27, 21).make_golden())
    warbands[1].add_minion(CobaltScalebane(29, 38).make_golden().set_taunt())
    warbands[1].add_minion(RazorgoretheUntamed(55, 59).set_taunt())
    warbands[1].add_minion(Amalgadon(22, 27).set_taunt().set_poisonous())
    warbands[1].add_minion(ArmoftheEmpire())
    seed(1)

    results = execute_battles(warbands[0], warbands[1], 1_000)
    assert results == [12.5, 13.0, 74.5], "Results were not as expected"


def test_case_11(warbands: List[Warband]):

    # https://youtu.be/MHkPMkxj4HE?t=728
    # [49.7, 21.0, 29.3]

    warbands[0].add_minion(CracklingCyclone(13, 10))
    warbands[0].add_minion(CracklingCyclone(23, 20))
    warbands[0].add_minion(BristlebackKnight(9, 13))
    warbands[0].add_minion(RecyclingWraith(12, 10))
    warbands[0].add_minion(MajordomoExecutus())
    warbands[0].add_minion(Sellemental(2, 2))
    warbands[0].add_minion(DazzlingLightspawn(6, 7))

    warbands[1].add_minion(MonstrousMacaw(9, 7))
    warbands[1].add_minion(AggemThorncurse(9, 12))
    warbands[1].add_minion(SelflessHero())
    warbands[1].add_minion(Tarecgosa(8, 8))
    warbands[1].add_minion(WrathWeaver(24, 28))
    warbands[1].add_minion(CaptainFlatTusk(12, 9).set_taunt())
    warbands[1].add_minion(ImpulsiveTrickster(10, 10).make_golden().set_taunt())
    seed(1)
    results = execute_battles(warbands[0], warbands[1], 1_000)
    assert results == [28.6, 20.6, 50.8], "Results were not as expected"


def test_peggy(warbands: List[Warband]):
    warbands[0].add_minion(PeggyBrittlebone())
    cap_check = CapnHoggarr()
    assert cap_check.attack == 6
    assert cap_check.health == 6
    warbands[0].add_minion(cap_check)
    board = Board(warbands[0], warbands[1])
    board.top_warband.add_cards_to_hand()
    cap_check = board.top_warband.minions[1]

    assert cap_check.attack == 7
    assert cap_check.health == 7


def test_skypirate(warbands: List[Warband]):
    warbands[1].add_minion(Scallywag())
    board = Board(warbands[0], warbands[1])
    on_death(
        board.bottom_warband.minions[0], None, board.bottom_warband, board.top_warband
    )
    assert board.bottom_warband.minions[0].name == "Sky Pirate"


def test_edge_case_for_summoning(warbands: List[Warband]):
    for _ in range(7):
        warbands[1].add_minion(Ghastcoiler())
    board = Board(warbands[0], warbands[1])
    board.bottom_warband.minions[0].take_damage_2(
        7, None, board.bottom_warband, board.top_warband
    )
    on_death(
        board.bottom_warband.minions[0], None, board.bottom_warband, board.top_warband
    )
    assert len(board.bottom_warband.minions) == 7


def test_edge_case_for_summoning_2(warbands: List[Warband]):
    for _ in range(1):
        warbands[1].add_minion(ImpMama())
    board = Board(warbands[0], warbands[1])
    for _ in range(10):
        board.bottom_warband.minions[0].take_damage_2(
            1, None, board.bottom_warband, board.top_warband
        )
    board.bottom_warband.update_warband()
    assert len(board.bottom_warband.minions) == 6


def test_kangor(warbands: List[Warband]):
    warbands[0].add_minion(AnnoyoModule())
    warbands[0].add_minion(AnnoyoModule())
    warbands[0].add_minion(KangorsApprentice())

    warbands[1].add_minion(Sellemental(6, 11))

    board = Board(warbands[0], warbands[1])
    board.battle()
    assert board.top_warband.minions[0].divine_shield
    assert board.top_warband.minions[1].divine_shield
    assert board.top_warband.minions[0].attack == 2
    assert board.top_warband.minions[1].attack == 2
