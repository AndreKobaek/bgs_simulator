from copy import deepcopy
from typing import List


class Minion(object):
    name: str
    tribe: List[str]
    tier: int
    attack: int
    base_attack: int
    health: int
    damage_taken: int
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
    base_divine_shield: bool
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
        self.damage_taken = 0
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
        self.base_divine_shield = False
        self.golden = 1
        self.death_rattles = []
        self.start_of_combat = False

        # Observers
        self.pre_attack_observers: List[Minion] = []
        self.pre_defend_observers: List[Minion] = []
        self.divine_observers: List[Minion] = []
        self.post_attack_observers: List[Minion] = []
        self.post_damage_observers: List[Minion] = []
        self.buff_observers: List[Minion] = []
        self.death_observers: List[Minion] = []

    def make_golden(self):
        self.golden = 2
        self.windfury *= 2
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

    def set_divine_shield(self, divine_shield: bool):
        self.divine_shield = divine_shield
        self.base_ds = divine_shield

    def take_damage(self, incoming_damage: int):
        self.health -= incoming_damage
        self.damage_taken += incoming_damage

    def take_damage_2(
        self,
        incoming_damage: int,
        receiver_minion,
        own_warband,
        opponent_warband,
    ):
        if incoming_damage > 0:
            if self.divine_shield:
                self.pop_divine_shield(own_warband)
            elif receiver_minion is not None and receiver_minion.poisonous:
                self.alive = False
            else:
                self.health -= incoming_damage
                self.damage_taken += incoming_damage

            if self.health <= 0:
                self.alive = False

            if self.alive:
                self.activate_frenzy(own_warband)

    def add_health(self, incoming_health):
        self.health += incoming_health

    def __str__(self) -> str:
        minion_print = f"{self.name}: {self.attack} / {self.health}{' - Taunt' if self.taunt else ''}{' - Divine Shield' if self.divine_shield else ''}"
        return minion_print

    def _reborn(self):
        if self.reborn:
            self.alive = True
            self.divine_shield = self.base_divine_shield
            self._set_attack_and_health(self.base_attack, 1)
            self.damage_taken = self.base_health - 1
            self.reborn = False

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

    def buff_summoned_minion(self, summoned_minion, own_warband):
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

    def gain_divine_shield(self, own_warband):
        self.divine_shield = True
        for minion in own_warband.minions:
            minion.register_observable(own_warband, None)


def on_death(
    dealer_minion: Minion,
    receiver_minion: Minion,
    own_warband,
    opponent_warband,
):
    dealer_minion.update_death_observers()
    notify_observers(
        dealer_minion.death_observers,
        dealer_minion,
        receiver_minion,
        own_warband,
        opponent_warband,
    )
    execute_deathrattles(dealer_minion, own_warband, opponent_warband)

    if dealer_minion.reborn:
        dealer_minion._reborn()
    else:
        own_warband.remove_minion(dealer_minion)


def execute_deathrattles(dealer_minion: Minion, own_warband, opponent_warband):
    barons = [
        minion.golden + 1
        for minion in own_warband.minions
        if minion.name == "Baron Rivendare"
    ]
    if barons != []:
        baron_count = max(barons)
    else:
        baron_count = 1
    # TODO undersøge baron interaction, er det alle deathrattles 3 gange eller hvert deathrattle 3 gange
    for _ in range(baron_count):
        for deathrattle in dealer_minion.death_rattles:
            deathrattle(own_warband, opponent_warband)


def notify_observers(
    observers: List[Minion],
    dealer_minion: Minion,
    receiver_minion: Minion,
    own_warband,
    opponent_warband,
):
    for observer in observers:
        observer.notify(dealer_minion, receiver_minion, own_warband, opponent_warband)
