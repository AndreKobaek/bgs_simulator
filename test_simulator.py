from copy import deepcopy
from random import seed
from typing import List
import pytest
from board import Board
from main import execute_battles
from minions import (
    AcolyteOfCthun,
    Alleycat,
    CapnHoggarr,
    FreedealingGambler,
    GlyphGuadrdian,
    IckyImp,
    Leapfrogger,
    MajordomoExecutus,
    MoltenRock,
    MonstrousMacaw,
    NomiKitchenNightmare,
    PartyElemental,
    PeggyBrittlebone,
    RazorfenGeomancer,
    RefreshingAnomaly,
    RipsnarlCaptain,
    Scallywag,
    Sellemental,
    SewerRat,
    SouthseaCaptian,
    SouthseaStrongarm,
    SpawnOfNZoth,
    Tabbycat,
    WildfireElemental,
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
    RG = RazorfenGeomancer()
    RG.reborn = True
    warbands[0].add_minion(RG)
    warbands[1].add_minion(RefreshingAnomaly())
    board = Board(warbands[0], warbands[1])
    assert board.battle() == [1, 0, 2]


def test_case_2(warbands: List[Warband]):
    SoN = SpawnOfNZoth()
    SoN.reborn = True
    GG = GlyphGuadrdian()
    GG._add_stats(1, 1)
    warbands[0].add_minion(SoN)
    warbands[0].add_minion(GG)
    selly = Sellemental()
    selly._add_stats(5, 5)
    warbands[1].add_minion(selly)
    board = Board(warbands[0], warbands[1])
    # needs accumulated results and bounds


def test_case_3(warbands: List[Warband]):
    warbands[0].add_minion(Scallywag())
    warbands[0].add_minion(RipsnarlCaptain())
    selly = Sellemental()
    selly._add_stats(5, 9)
    warbands[1].add_minion(selly)
    board = Board(warbands[0], warbands[1])
    assert board.battle() == [1, 0, 2]


def test_case_4(warbands: List[Warband]):

    warbands[0].add_minion(MonstrousMacaw())
    SoN = SpawnOfNZoth()
    SoN.reborn = True
    warbands[0].add_minion(SoN)
    minion1 = GlyphGuadrdian()
    minion1._add_stats(1, 1)
    warbands[0].add_minion(minion1)
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
    assert results == [94.9, 4.2, 0.9], "Results were not as expected"


def test_case_5(warbands: List[Warband]):
    SoN = SpawnOfNZoth()
    SoN.reborn = True
    warbands[0].add_minion(SoN)
    minion1 = GlyphGuadrdian()
    minion1._add_stats(1, 1)
    warbands[0].add_minion(minion1)

    nomi = NomiKitchenNightmare()
    nomi._add_stats(1, 1)
    warbands[1].add_minion(nomi)
    warbands[1].add_minion(RazorfenGeomancer())

    seed(1)
    results = execute_battles(warbands[0], warbands[1], 1_000)
    assert results == [51.0, 49.0, 0.0], "Results were not as expected"


def test_case_6(warbands: List[Warband]):
    warbands[0].add_minion(GlyphGuadrdian())
    warbands[0].add_minion(FreedealingGambler())
    warbands[0].add_minion(PartyElemental())
    warbands[0].add_minion(Scallywag())

    icky = IckyImp()
    icky._add_stats(6, 3)
    warbands[1].add_minion(icky)
    refresh = RefreshingAnomaly()
    refresh._add_stats(4, 2)
    rf2 = deepcopy(refresh)
    warbands[1].add_minion(refresh)
    warbands[1].add_minion(rf2)
    warbands[1].add_minion(Sellemental())
    warbands[1].add_minion(AcolyteOfCthun())

    results = execute_battles(warbands[0], warbands[1], 1_000)
    assert results == [0.0, 0.0, 100.0], "Results were not as expected"


def test_case_7(warbands: List[Warband]):
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

    seed(1)
    results = execute_battles(warbands[0], warbands[1], 1_000)
    assert results == [1.0, 3.6, 95.4], "Results were not as expected"
