from typing import List
import pytest
from board import Board
from minions import (
    GlyphGuadrdian,
    RazorfenGeomancer,
    RefreshingAnomaly,
    RipsnarlCaptain,
    Scallywag,
    Sellemental,
    SpawnOfNZoth,
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


def test_case_2(warbands: List[Warband]):
    warbands[0].add_minion(Scallywag())
    warbands[0].add_minion(RipsnarlCaptain())
    selly = Sellemental()
    selly._add_stats(5, 9)
    warbands[1].add_minion(selly)
    board = Board(warbands[0], warbands[1])
    assert board.battle() == [1, 0, 2]
