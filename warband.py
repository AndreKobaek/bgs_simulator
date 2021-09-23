from copy import deepcopy
from typing import List, Optional
from settings import MAX_BOARDSIZE, TRIBE_MECH
from minion import Minion
from random import randint


class Warband(object):
    def __init__(self) -> None:
        self.minions: List[Minion] = []
        self.next_attacker = 0
        self.dead_mechs = []
        self.summon_observers: List[Minion] = []

    def add_minion(self, minion):
        self.minions.append(minion)

    def __str__(self) -> str:
        return "\n".join([x.__str__() for x in self.minions])

    def get_next_attacker(self) -> Optional[Minion]:
        for i in range(len(self.minions) - 1):
            if (
                self.minions[i].number_of_attacks
                > self.minions[i + 1].number_of_attacks
            ):
                if self.minions[i + 1].attack > 0:
                    return self.minions[i + 1]
                else:
                    self.minions[i + 1].number_of_attacks += 1
        for minion in self.minions:
            if minion.attack > 0:
                return minion
            else:
                minion.number_of_attacks += 1
        return None

    def get_adjacent_minions(self, minion):
        minion_position = self.minions.index(minion)
        warband_size = self._get_warband_size()

        if 0 < minion_position and minion_position < warband_size:
            return [
                self.minions[minion_position - 1],
                self.minions[minion_position + 1],
            ]
        elif 0 < minion_position and minion_position == warband_size:
            return [self.minions[minion_position - 1]]
        elif minion_position == 0 and minion_position < warband_size:
            return [self.minions[minion_position + 1]]
        elif minion_position == 0 and minion_position == warband_size:
            return []
        else:
            raise Exception("No adjacent minions where found")

    def minions_alive(self) -> int:
        return len([x for x in self.minions if x.alive])

    def update_warband(self):
        for minion in self.minions:
            if not minion.alive and minion.tribe == TRIBE_MECH:
                dead_mech = deepcopy(minion)
                dead_mech.__init__()
                if minion.golden == 2:
                    dead_mech.make_golden()
                self.dead_mechs.append(dead_mech)
        self.minions = [x for x in self.minions if x.alive]
        self.summon_observers = [x for x in self.summon_observers if x.alive]

    def calculate_damage(self):
        return sum([x.tier for x in self.minions])

    def _get_warband_size(self):
        return len(self.minions) - 1

    # def _register_observers(self):

    def sniped(self, damage: int):
        receiver = get_random_minion(self.minions)
        if receiver.divine_shield:
            receiver.pop_divine_shield(self)
        else:
            receiver.health -= damage
            receiver.update_life_status()

    def _get_available_boardspace(self, limit: int):
        return min(
            MAX_BOARDSIZE - len([x for x in self.minions if x.alive]),
            limit,
        )

    def summon_minions(self, summoner, minions):
        board_space = self._get_available_boardspace(len(minions))
        if board_space > 0:
            minions_2_sum = deepcopy(minions)
            for minion in minions_2_sum:
                minion.number_of_attacks = summoner.number_of_attacks

            minions_2_sum = minions_2_sum[:board_space]
            summoner_position = self.minions.index(summoner) + 1
            self.minions = (
                self.minions[:summoner_position]
                + minions_2_sum
                + self.minions[summoner_position:]
            )

    def can_do_battle(self):
        return self.minions_alive() > 0

    def has_attackers(self):
        if self.minions_alive() > 0:
            for minion in self.minions:
                if minion.attack > 0:
                    return True
        return False

    def make_all_minions_golden(self):
        for minion in self.minions:
            minion.make_golden()


def get_next_defender(minions: List[Minion]) -> Minion:
    taunts = []
    # Hvis du har en funktion der ikke opdaterer objektet selv, bør det være en util funk.
    for minion in minions:
        if minion.taunt:
            taunts.append(minion)
    if len(taunts) > 0:
        return get_random_minion(taunts)
    return get_random_minion(minions)


def get_random_minion(minions: List[Minion]) -> Minion:
    alive_minions = [x for x in minions if x.alive]
    if alive_minions != []:
        return alive_minions[randint(0, len(alive_minions) - 1)]
