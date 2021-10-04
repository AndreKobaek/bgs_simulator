from copy import deepcopy
from random import seed
from typing import List
import pytest
from board import Board
from main import execute_battles
from minions import (
    AcolyteOfCthun,
    Alleycat,
    BaronRivendare,
    CapnHoggarr,
    CobaltScalebane,
    DreadAdmiralEliza,
    FreedealingGambler,
    GlyphGuadrdian,
    IckyImp,
    ImpMama,
    ImpatientDoomsayer,
    InsatiableUrzul,
    Kalecgos,
    Leapfrogger,
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
    RefreshingAnomaly,
    RipsnarlCaptain,
    Scallywag,
    Sellemental,
    SewerRat,
    SoulDevourer,
    SouthseaCaptian,
    SouthseaStrongarm,
    SpawnOfNZoth,
    Tabbycat,
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
    assert results == [93.6, 5.0, 1.4], "Results were not as expected"


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
    assert results == [1.0, 3.6, 95.4], "Results were not as expected"


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
    assert results == [61.5, 24.8, 13.7], "Results were not as expected"
