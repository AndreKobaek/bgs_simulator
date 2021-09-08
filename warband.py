from minion import Minion
from random import randint


class Warband(object):
    # warband: list(Minion)

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

    def _get_random_minion(self, minions=None):
        if minions is None:
            return self.warband[randint(0, len(self.warband) - 1)]
        else:
            return minions[randint(0, len(minions) - 1)]

    def minions_alive(self):
        return len(self.warband)

    def update_warband(self):
        self.warband = [x for x in self.warband if x.alive]
