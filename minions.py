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
        self._set_attack_and_health(6, 6)
        self.death_rattle = True

    def activate_death_rattle(self, **kwargs):
        if "warband" in kwargs:
            warband: Warband = kwargs["warband"]
        else:
            raise Exception(f"warband not passed to {self.name}")
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
        self._set_attack_and_health(2, 2)
        self.death_rattle = True

    def activate_death_rattle(self, **kwargs):
        if "warband" in kwargs:
            warband: Warband = kwargs["warband"]
        else:
            raise Exception(f"warband not passed to {self.name}")
        for minion in warband.warband:
            if minion is not self:
                minion._add_stats(self.golden, self.golden)


class Ghastcoiler(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Ghastcoiler"
        self.tribe = TRIBE_BEAST
        self.tier = 6
        self._set_attack_and_health(7, 7)
        self.death_rattle = True

    def activate_death_rattle(self, **kwargs):
        if "warband" in kwargs:
            warband: Warband = kwargs["warband"]
        else:
            raise Exception(f"warband not passed to {self.name}")
        board_space = min(
            MAX_BOARDSIZE - len([x for x in warband.warband if x.alive]),
            2 * self.golden,
        )
        if board_space > 0:
            possible_minions = [
                OmegaBuster(),
                SpawnOfNZoth(),
                IckyImp(),
                HarvestGolem(),
            ]
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
        self._set_attack_and_health(1, 1)


class Sellemental(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Sellemental"
        self.tribe = TRIBE_ELEMENTAL
        self._set_attack_and_health(2, 2)


class Imp(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Imp"
        self.tribe = TRIBE_DEMON
        self._set_attack_and_health(1, 1)


class IckyImp(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Icky Imp"
        self.tribe = TRIBE_DEMON
        self._set_attack_and_health(1, 1)
        self.death_rattle = True

    def activate_death_rattle(self, **kwargs):
        if "warband" in kwargs:
            warband: Warband = kwargs["warband"]
        else:
            raise Exception(f"warband not passed to {self.name}")
        board_space = min(
            MAX_BOARDSIZE - len([x for x in warband.warband if x.alive]),
            2,
        )
        if board_space > 0:
            imp = Imp()
            imp.number_of_attacks = self.number_of_attacks
            if self.golden == 2:
                imp.make_golden()
            imps = [deepcopy(imp) for _ in range(board_space)]
            summoner_position = warband.warband.index(self)
            warband.warband = (
                warband.warband[:summoner_position]
                + imps
                + warband.warband[summoner_position:]
            )


class Imprisoner(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Imprisoner"
        self.tribe = TRIBE_DEMON
        self.tier = 2
        self._set_attack_and_health(3, 3)
        self.taunt = True
        self.death_rattle = True

    def activate_death_rattle(self, **kwargs):
        if "warband" in kwargs:
            warband: Warband = kwargs["warband"]
        else:
            raise Exception(f"warband not passed to {self.name}")
        board_space = min(
            MAX_BOARDSIZE - len([x for x in warband.warband if x.alive]),
            1,
        )
        if board_space > 0:
            imp = Imp()
            imp.number_of_attacks = self.number_of_attacks
            if self.golden == 2:
                imp.make_golden()
            imps = [deepcopy(imp) for _ in range(board_space)]
            summoner_position = warband.warband.index(self)
            warband.warband = (
                warband.warband[:summoner_position]
                + imps
                + warband.warband[summoner_position:]
            )


class HarvestGolem(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Harvest Golem"
        self.tribe = TRIBE_MECH
        self.tier = 2
        self._set_attack_and_health(2, 3)
        self.death_rattle = True

    def activate_death_rattle(self, **kwargs):
        if "warband" in kwargs:
            warband: Warband = kwargs["warband"]
        else:
            raise Exception(f"warband not passed to {self.name}")
        board_space = min(
            MAX_BOARDSIZE - len([x for x in warband.warband if x.alive]),
            1,
        )
        if board_space > 0:
            golem = DamagedGolem()
            golem.number_of_attacks = self.number_of_attacks
            if self.golden == 2:
                golem.make_golden()
            golems = [deepcopy(golem) for _ in range(board_space)]
            summoner_position = warband.warband.index(self)
            warband.warband = (
                warband.warband[:summoner_position]
                + golems
                + warband.warband[summoner_position:]
            )


class DamagedGolem(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Damaged Golem"
        self.tribe = TRIBE_MECH
        self._set_attack_and_health(2, 1)


class KaboomBot(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Kaboom Bot"
        self.tribe = TRIBE_MECH
        self.tier = 2
        self._set_attack_and_health(2, 2)
        self.death_rattle = True

    def activate_death_rattle(self, **kwargs):
        if "opponent_warband" in kwargs:
            opponent_warband: Warband = kwargs["opponent_warband"]
        else:
            raise Exception(f"opponent_warband not passed to {self.name}")
        if len([x for x in opponent_warband.warband if x.alive]) > 0:
            for _ in range(self.golden):
                opponent_warband.sniped(4)


class SelflessHero(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Selfless Hero"
        self.tier = 2
        self._set_attack_and_health(2, 1)
        self.death_rattle = True

    def activate_death_rattle(self, **kwargs):
        if "warband" in kwargs:
            warband: Warband = kwargs["warband"]
        else:
            raise Exception(f"warband not passed to {self.name}")
        if warband.minions_alive() > 0:
            for _ in range(self.golden):
                no_ds_minions = [x for x in warband.warband if not x.divine_shield]
                warband._get_random_minion(no_ds_minions).divine_shield = True
