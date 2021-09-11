from minion import Minion
from random import randint


class Warband(object):
    def __init__(self) -> None:
        self.warband = []
        self.next_attacker = 0

    def add_minion(self, minion):
        self.warband.append(minion)

    def __str__(self) -> str:
        return "\n".join([x.__str__() for x in self.warband])

    def get_next_attacker(self) -> Minion:
        for i in range(len(self.warband) - 1):
            if (
                self.warband[i].number_of_attacks
                > self.warband[i + 1].number_of_attacks
            ):
                return self.warband[i + 1]
        return self.warband[0]

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
            print("Minion has no adjacent???")

    def _get_random_minion(self, minions=None) -> Minion:
        if minions is None:
            return self.warband[randint(0, len(self.warband) - 1)]
        else:
            return minions[randint(0, len(minions) - 1)]

    def minions_alive(self):
        return len([x for x in self.warband if x.alive])

    def update_warband(self):
        self.warband = [x for x in self.warband if x.alive]

    def calculate_damage(self):
        return sum([x.tier for x in self.warband])

    def _get_warband_size(self):
        return len(self.warband) - 1

    def sniped(self, damage: int):
        receiver = self._get_random_minion()
        if receiver.divine_shield:
            receiver.divine_shield = False
        else:
            receiver.health -= damage
            receiver.update_life_status()
