from copy import deepcopy
from random import randint
from minion import Minion
from warband import Warband

MAX_BOARDSIZE = 7
TRIBE_MECH = "Mech"
TRIBE_DRAGON = "Dragon"
TRIBE_DEMON = "Demon"
TRIBE_BEAST = "Beast"
TRIBE_ELEMENTAL = "Elemental"


class OmegaBuster(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Omega Buster"
        self.tribe = TRIBE_MECH
        self.tier = 6
        self.attack = 6
        self.health = 6
        self.base_attack = 6
        self.base_health = 6
        self.death_rattle = True

    def activate_death_rattle(self, **kwargs):
        if "warband" in kwargs:
            warband: Warband = kwargs["warband"]
        else:
            raise Exception("warband not passed to OmegaBuster DR")
        # check out of minions alive
        board_space = min(
            MAX_BOARDSIZE - len([x for x in warband.warband if x.alive]), 6
        )
        buff_size = (6 - board_space) * self.golden
        if board_space > 0:
            microbot = MicroBot()
            microbot.number_of_attacks = self.number_of_attacks
            if self.golden == 2:
                microbot.make_golden()
            microbots = [deepcopy(microbot) for _ in range(board_space)]
            summoner_position = warband.warband.index(self)
            warband.warband = (
                warband.warband[:summoner_position]
                + microbots
                + warband.warband[summoner_position:]
            )
        if buff_size > 0:
            for minion in warband.warband:
                if minion.tribe == TRIBE_MECH and minion is not self:
                    minion._add_stats(buff_size, buff_size)


class SpawnOfNZoth(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Spawn of N'Zoth"
        self.tier = 2
        self.attack = 2
        self.health = 2
        self.base_attack = 2
        self.base_health = 2
        self.death_rattle = True

    def activate_death_rattle(self, **kwargs):
        if "warband" in kwargs:
            warband: Warband = kwargs["warband"]
        else:
            raise Exception("warband not passed to spawn of N'zoth")
        for minion in warband.warband:
            if minion is not self:
                minion._add_stats(self.golden, self.golden)


class Ghastcoiler(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Ghastcoiler"
        self.tribe = TRIBE_BEAST
        self.tier = 6
        self.attack = 7
        self.health = 7
        self.base_attack = 7
        self.base_health = 7
        self.death_rattle = True

    def activate_death_rattle(self, **kwargs):
        if "warband" in kwargs:
            warband: Warband = kwargs["warband"]
        else:
            raise Exception("warband not passed to Ghastcoiler")
        board_space = min(
            MAX_BOARDSIZE - len([x for x in warband.warband if x.alive]),
            2 * self.golden,
        )
        if board_space > 0:
            possible_minions = [OmegaBuster(), SpawnOfNZoth()]
            chosen_minions = [
                deepcopy(possible_minions[randint(0, len(possible_minions) - 1)])
                for _ in range(board_space)
            ]
            for chosen_minion in chosen_minions:
                chosen_minion.number_of_attacks = self.number_of_attacks
            summoner_position = warband.warband.index(self)
            warband.warband = (
                warband.warband[:summoner_position]
                + chosen_minions
                + warband.warband[summoner_position:]
            )


class MicroBot(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Microbot"
        self.tribe = TRIBE_MECH
        self.attack = 1
        self.health = 1
        self.base_attack = 1
        self.base_health = 1


class Sellemental(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Sellemental"
        self.tribe = TRIBE_ELEMENTAL
        self.attack = 2
        self.health = 2
        self.base_attack = 2
        self.base_health = 2


DEATH_RATTLE_MINIONS = [OmegaBuster(), SpawnOfNZoth(), Ghastcoiler()]
