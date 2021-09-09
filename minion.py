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
    reborn: bool
    number_of_attacks: int
    divine_shield: bool
    death_observer: bool
    # should either be 1 or 2
    golden: int

    def __init__(
        self,
        name,
        tribe,
        tier,
        attack,
        health,
        taunt,
        divine_shield,
        frenzy=False,
        windfury=1,
        reborn=False,
        cleave=False,
        death_observer=False,
        golden=1,
    ) -> None:
        self.name = name
        self.tribe = tribe
        self.tier = tier
        self.attack = attack
        self.health = health
        self.taunt = taunt
        self.alive = True
        self.number_of_attacks = 0
        self.divine_shield = divine_shield
        self.frenzy = frenzy
        self.windfury = windfury
        self.reborn = reborn
        self.cleave = cleave
        self.death_observer = death_observer
        self.golden = golden

    def set_health(self, health):
        self.health = health

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

    def activate_upon_death(self, dead_minion, opponent_warband):
        if self.name == "Scavenging Hyena" and dead_minion.tribe == "Beast":
            self.attack += 2 * self.golden
            self.health += 1 * self.golden
        if self.name == "Soul Juggler" and dead_minion.tribe == "Demon":
            for _ in range(self.golden):
                opponent_warband.sniped(3)

        # Soul Juggler
        # Kangor's Apprentice
        # TODO if dead_minion is mech and self.deathrattle is available
        # add dead_minion to death_rattle
