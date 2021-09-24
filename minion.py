from copy import deepcopy
from typing import List


class Minion(object):
    name: str
    tribe: List[str]
    tier: int
    attack: int
    base_attack: int
    health: int
    taunt: bool
    alive: bool
    frenzy: bool = False
    # should either be 1 or 2
    windfury: int = 1
    cleave = bool
    poisonous = bool
    reborn: bool
    number_of_attacks: int
    avenge_counter: int
    avenge_limit: int
    divine_shield: bool
    # should either be 1 or 2
    golden: int
    death_rattles: list
    avenge: bool
    start_of_combat: bool
    pre_attack: bool

    def __init__(self) -> None:
        self.name = ""
        self.tribe = ["Neutral"]
        self.tier = 1
        self.attack = None
        self.health = None
        self.base_attack = None
        self.base_health = None
        self.taunt = False
        self.alive = True
        self.frenzy = False
        self.windfury = 1
        self.cleave = 0
        self.poisonous = False
        self.reborn = False
        self.avenge_counter = 0
        self.avenge_limit = 0
        self.number_of_attacks = 0
        self.divine_shield = False
        self.golden = 1
        self.death_rattles = []
        self.start_of_combat = False

        # Observers
        self.pre_attack_observers: List[Minion] = []
        self.pre_defend_observers: List[Minion] = []
        self.divine_observers: List[Minion] = []
        self.post_damage_observers: List[Minion] = []
        self.buff_observers: List[Minion] = []
        self.death_observers: List[Minion] = []

    def make_golden(self):
        self.golden = 2
        self.attack += self.base_attack
        self.base_attack *= 2
        self.add_health(self.base_health)
        self.base_health *= 2

    def set_health(self, health):
        self.health = health

    def _set_attack_and_health(self, atk, hp):
        self.attack = atk
        self.base_attack = atk
        self.health = hp
        self.base_health = hp

    def set_base_attributes(self, base_atk: int, divine_shield: bool):
        self.base_attack = base_atk
        self.base_ds = divine_shield

    def take_damage(self, incoming_damage: int):
        self.health -= incoming_damage

    def add_health(self, incoming_health):
        self.health += incoming_health

    def __str__(self) -> str:
        minion_print = f"{self.name}: {self.attack} / {self.health}{' - Taunt' if self.taunt else ''}{' - Divine Shield' if self.divine_shield else ''}"
        return minion_print

    # TODO redo reborn

    def update_life_status(self) -> bool:
        if self.health <= 0 and self.reborn:
            self.health = 1
            self.attack = self.base_attack
        elif self.health <= 0:
            self.alive = False
        return self.alive

    def update_death_observers(self):
        self.death_observers = [
            death_observer
            for death_observer in self.death_observers
            if death_observer.alive
        ]

    def avenge_tick(self):
        self.avenge_counter += 1
        if self.avenge_counter % self.avenge_limit == 0:
            self.avenge_counter = 0
            return True
        return False

    def pre_combat_effect(self, own_warband, opponent_warband):
        pass

    def activate_frenzy(self, own_warband):
        pass

    def register_observable(self, own_warband, opponent_warband):
        pass

    def buff_summoned_minion(self, summoned_minion):
        pass

    def execute_summon_effect(self, own_warband, opponent_warband):
        pass

    def notify(
        self,
        dealer_minion=None,
        receiver_minion=None,
        own_warband=None,
        opponent_warband=None,
    ):
        pass

    def activate_death_rattle(self, own_warband, opponent_warband):
        return None

    def _add_stats(self, atk, hp):
        self.attack += atk
        self.add_health(hp)

    def _setup_minions_to_summon(self, number_of_minions, minion):
        if self.golden == 2:
            minion.make_golden()
        return [deepcopy(minion) for _ in range(number_of_minions)]

    def get_death_rattles(self):
        return self.deathrattles

    def pop_divine_shield(self, own_warband):
        self.divine_shield = False
        for divine_observer in self.divine_observers:
            divine_observer.notify(self, None, own_warband)

    def gain_divine_shield(self, warband):
        self.divine_shield = True
        for minion in warband.minions:
            minion.register_observable(warband, None)
