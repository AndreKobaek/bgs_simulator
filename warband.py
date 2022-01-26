from copy import deepcopy
from typing import List, Optional
from settings import MAX_BOARDSIZE, TRIBE_MECH
from minion import Minion, get_random_minion
import json
import pickle


class Warband(object):
    def __init__(self, list_of_minions=None) -> None:
        if list_of_minions is not None:
            self.minions = list_of_minions
        else:
            self.minions: List[Minion] = []
        self.next_attacker = 0
        self.dead_mechs = []
        self.summon_observers: List[Minion] = []
        self.card_gain_observers: List[Minion] = []
        self.cards_in_hand: int = 0

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def toPickle(self):
        return pickle.dumps(self, protocol=5)

    def from_Pickle(self, pickle_object):
        self = pickle.loads(pickle_object)

    def from_JSON(self, json_object):
        self.__dict__ = json.loads(json_object)
        new_minions = []
        for minion in self.minions:
            import minions

            class_ = getattr(minions, clean_minion_name(minion["name"]))
            new_minion: Minion = class_()
            deathrattles = minion.pop("death_rattles")
            new_minion.from_JSON(minion)
            if len(new_minion.death_rattles) < len(deathrattles):
                if len(new_minion.death_rattles) == 1:
                    deathrattles = deathrattles[1:]
                for dr in deathrattles:
                    insert_dr = getattr(minions, dr)
                    new_minion.death_rattles.append(insert_dr)
            new_minions.append(new_minion)
        self.minions = new_minions

    def add_minion(self, minion):
        self.minions.append(minion)
        return self

    def add_list_of_minions(self, minions_list):
        self.minions.extend(minions_list)
        return self

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
        warband_size = len(self.minions) - 1

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

    def add_cards_to_hand(self):
        if self.cards_in_hand < 10:
            self.cards_in_hand += 1
            for minion in self.card_gain_observers:
                minion.notify(None, None, self, None)

    def update_warband(self):
        for minion in self.minions:
            if not minion.alive and TRIBE_MECH in minion.tribe:
                self.add_dead_mechs_if_dead(minion)
        self.minions = [x for x in self.minions if x.alive]
        self.summon_observers = [x for x in self.summon_observers if x.alive]

    def add_dead_mechs_if_dead(self, dead_minion: Minion = None):
        dead_mech = deepcopy(dead_minion)
        dead_mech.__init__()
        if dead_minion.golden == 2:
            dead_mech.make_golden()
        self.dead_mechs.append(dead_mech)

    def sniped(self, damage: int, dealer_minion: Minion, shooter_warband):
        receiver = get_random_minion(self.minions)
        if receiver is not None:
            # receiver.take_damage_2(damage, dealer_minion, shooter_warband, self)
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

    def summon_scale(self):
        khadgars = [
            minion.golden + 1 for minion in self.minions if minion.name == "Khadgar"
        ]
        if khadgars == []:
            return [1]
        else:
            return khadgars

    def remove_minion(self, dead_minion: Minion):
        if TRIBE_MECH in dead_minion.tribe:
            self.add_dead_mechs_if_dead(dead_minion)
        if dead_minion in self.summon_observers:
            self.summon_observers.remove(dead_minion)
        self.minions.remove(dead_minion)

    def summon_minions(self, summoner: Minion, minions: List[Minion], opponent_warband):
        minions_2_sum = deepcopy(minions)
        number_of_attacks = summoner.number_of_attacks
        summoner_position = self.minions.index(summoner) + 1
        scales = self.summon_scale()
        for minion in minions_2_sum:
            for scale in scales:
                summoned_minions = self.summon_minion(
                    summoner_position,
                    number_of_attacks,
                    minion,
                    scale,
                    opponent_warband,
                )
                summoner_position += len(summoned_minions)
                for sum_minion in summoned_minions:
                    sum_minion.execute_summon_effect(self, opponent_warband)

    def summon_minion(
        self,
        summoner_position: int,
        number_of_attacks: int,
        minion: Minion,
        amount_to_summon: int,
        opponent_warband,
    ) -> List[Minion]:
        summoned_minions = []
        board_space = self._get_available_boardspace(amount_to_summon)
        for _ in range(board_space):
            minion.number_of_attacks = max(number_of_attacks - 1, 0)
            self.minions.insert(summoner_position, minion)
            for observers in self.minions:
                observers.register_observable(self, opponent_warband)
            for summon_observer in self.summon_observers:
                summon_observer.buff_summoned_minion(minion, self)
            summoner_position += 1
            summoned_minions.append(minion)
        return summoned_minions

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


def clean_minion_name(name: str) -> str:
    return "".join(e for e in name if e.isalnum())


def calculate_damage(minions: List[Minion]) -> int:
    return sum([minion.tier for minion in minions])


def get_highest_health_minion(minions: List[Minion]) -> Optional[Minion]:
    highest_health_minions = [minion.health for minion in minions if minion.alive]
    if highest_health_minions != []:
        highest_health = max(highest_health_minions)
        potential_minions = [
            minion for minion in minions if minion.health == highest_health
        ]
        if len(potential_minions) > 1:
            return get_random_minion(potential_minions)
        elif len(potential_minions) == 1:
            return potential_minions[0]
    return None


def get_deathrattle_minion(
    minions: List[Minion], exclude_minion: Minion = None
) -> Optional[Minion]:
    deathrattle_minions = [
        minion
        for minion in minions
        if minion.death_rattles != [] and minion is not exclude_minion
    ]
    if deathrattle_minions != []:
        if len(deathrattle_minions) > 1:
            return get_random_minion(deathrattle_minions)
        elif len(deathrattle_minions) == 1:
            return deathrattle_minions[0]
    return None
