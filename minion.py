class Minion(object):
    name: str
    type: str
    tier: int
    attack: int
    base_attack: int
    health: int
    taunt: bool
    alive: bool
    frenzy: bool = False
    # should either be 1 or 2
    windfury: int = 1
    reborn: bool
    number_of_attacks: int
    divine_shield: bool

    def __init__(
        self,
        name,
        attack,
        health,
        taunt,
        divine_shield,
        frenzy=False,
        windfury=1,
        reborn=False,
    ) -> None:
        self.name = name
        self.attack = attack
        self.health = health
        self.taunt = taunt
        self.alive = True
        self.number_of_attacks = 0
        self.divine_shield = divine_shield
        self.frenzy = frenzy
        self.windfury = windfury
        self.reborn = reborn

    def set_health(self, health):
        self.health = health

    def set_base_attack(self, base_atk):
        self.base_attack = base_atk

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
        self.divine_shield = True
        # frenzy triggered
        self.frenzy = False
