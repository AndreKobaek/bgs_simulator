from copy import deepcopy
from settings import MAX_BOARDSIZE, TRIBE_MECH
from minion import Minion
from random import randint


class Warband(object):
    def __init__(self) -> None:
        self.warband = []
        self.next_attacker = 0
        self.dead_mechs = []

    def add_minion(self, minion):
        self.warband.append(minion)

    def __str__(self) -> str:
        return "\n".join([x.__str__() for x in self.warband])

    def get_next_attacker(self) -> Minion:
        for i in range(self._get_warband_size()):
            if (
                self.warband[i].number_of_attacks
                > self.warband[i + 1].number_of_attacks
            ):
                if self.warband[i + 1].attack > 0:
                    return self.warband[i + 1]
                else:
                    self.warband[i + 1].number_of_attacks += 1
        for minion in self.warband:
            if minion.attack > 0:
                return minion
            else:
                minion.number_of_attacks += 1

    def get_next_defender(self) -> Minion:
        possible_defender = []
        for minion in self.warband:
            if minion.taunt:
                possible_defender.append(minion)
        if len(possible_defender) == 0:
            return self._get_random_minion()
        return self._get_random_minion(possible_defender)

    def get_adjacent_minions(self, minion):
        minion_position = self.warband.index(minion)
        warband_size = self._get_warband_size()

        if 0 < minion_position and minion_position < warband_size:
            return [
                self.warband[minion_position - 1],
                self.warband[minion_position + 1],
            ]
        elif 0 < minion_position and minion_position == warband_size:
            return [self.warband[minion_position - 1]]
        elif minion_position == 0 and minion_position < warband_size:
            return [self.warband[minion_position + 1]]
        elif minion_position == 0 and minion_position == warband_size:
            return []
        else:
            raise Exception("No adjacent minions where found")

    def _get_random_minion(self, minions=None) -> Minion:
        if minions is None:
            alive_minions = [x for x in self.warband if x.alive]
            return self.warband[randint(0, len(alive_minions) - 1)]
        else:
            return minions[randint(0, len(minions) - 1)]

    def minions_alive(self):
        return len([x for x in self.warband if x.alive])

    def update_warband(self):
        for minion in self.warband:
            if not minion.alive and minion.tribe == TRIBE_MECH:
                dead_mech = deepcopy(minion)
                dead_mech.__init__()
                if minion.golden == 2:
                    dead_mech.make_golden()
                self.dead_mechs.append(dead_mech)
        self.warband = [x for x in self.warband if x.alive]

    def calculate_damage(self):
        return sum([x.tier for x in self.warband])

    def _get_warband_size(self):
        return len(self.warband) - 1

    # def _register_observers(self):

    def sniped(self, damage: int):
        receiver = self._get_random_minion()
        if receiver.divine_shield:
            receiver.pop_divine_shield()
        else:
            receiver.health -= damage
            receiver.update_life_status()

    def _get_available_boardspace(self, limit: int):
        return min(
            MAX_BOARDSIZE - len([x for x in self.warband if x.alive]),
            limit,
        )

    def summon_minions(self, summoner, minions):
        board_space = self._get_available_boardspace(len(minions))
        if board_space > 0:
            minions_2_sum = deepcopy(minions)
            for minion in minions_2_sum:
                minion.number_of_attacks = summoner.number_of_attacks

            minions_2_sum = minions_2_sum[:board_space]
            summoner_position = self.warband.index(summoner) + 1
            self.warband = (
                self.warband[:summoner_position]
                + minions_2_sum
                + self.warband[summoner_position:]
            )

    def make_all_minions_golden(self):
        for minion in self.warband:
            minion.make_golden()
