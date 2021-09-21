from settings import MAX_BOARDSIZE
from copy import deepcopy


class Minion(object):
    name: str
    tribe: str
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
    # TODO implement lose_divine_shield to ease observer task
    divine_shield: bool
    death_observer: bool
    # should either be 1 or 2
    golden: int
    death_rattles: list
    avenge: bool
    start_of_combat: bool
    pre_attack: bool

    def __init__(self) -> None:
        self.name = ""
        self.tribe = "Neutral"
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
        self.number_of_attacks = 0
        self.divine_shield = False
        self.golden = 1
        self.death_rattles = []
        self.start_of_combat = False

        # Observers
        self.death_observers = []
        self.pre_attack_observers = []
        self.divine_observers = []
        self.pre_defend_observers = []

    def make_golden(self):
        self.golden = 2
        self.attack += self.base_attack
        self.base_attack *= 2
        self.health += self.base_health
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

    def __str__(self) -> str:
        minion_print = f"{self.name}: {self.attack} / {self.health}{' - Taunt' if self.taunt else ''}{' - Divine Shield' if self.divine_shield else ''}"
        return minion_print

    def update_life_status(self) -> bool:
        if self.health <= 0 and self.reborn:
            self.health = 1
            self.attack = self.base_attack
        elif self.health <= 0:
            self.alive = False
        return self.alive

    def activate_frenzy(self):
        # TODO Implement a more scalable Frenzy solution
        self.divine_shield = True
        # frenzy triggered
        self.frenzy = False

    def register_observable(self, own_warband, opponent_warband):
        pass

    def notify(self, dealer_minion=None, own_warband=None, opponent_warband=None):
        pass

    def activate_death_rattle(self, own_warband, opponent_warband):
        return None

    def _add_stats(self, atk, hp):
        self.attack += atk
        self.health += hp

    def _setup_minions_to_summon(self, number_of_minions, minion):
        if self.golden == 2:
            minion.make_golden()
        return [deepcopy(minion) for _ in range(number_of_minions)]

    def get_death_rattles(self):
        return self.deathrattles

    def pop_divine_shield(self):
        self.divine_shield = False
        for divine_observer in self.divine_observers:
            divine_observer.notify(self)

    def gain_divine_shield(self, warband):
        self.divine_shield = True
        for minion in warband.warband:
            minion.register_observable(warband, None)
