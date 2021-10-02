from copy import deepcopy
from random import randint
from board import combat_sequence
from warband import (
    Warband,
    get_deathrattle_minion,
    get_highest_health_minion,
    get_next_defender,
)
from warband import get_random_minion
from minion import Minion, execute_deathrattles
from settings import (
    TRIBE_BEAST,
    TRIBE_DEMON,
    TRIBE_DRAGON,
    TRIBE_ELEMENTAL,
    TRIBE_MECH,
    TRIBE_MURLOC,
    TRIBE_PIRATE,
    TRIBE_QUILBOAR,
)

# ###### TIER ONE ########


class AcolyteOfCthun(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Acolyte of C'thun"
        self.reborn = True
        self._set_attack_and_health(2, 2)


class Alleycat(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Alleycat"
        self.tribe = [TRIBE_BEAST]
        self._set_attack_and_health(1, 1)


class DeckSwabbie(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Deck Swabbie"
        self.tribe = [TRIBE_PIRATE]
        self._set_attack_and_health(2, 2)


class EvolvingChromawing(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Evolving Chromawing"
        self.tribe = [TRIBE_DRAGON]
        self._set_attack_and_health(1, 3)


class IckyImp(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Icky Imp"
        self.tribe = [TRIBE_DEMON]
        self._set_attack_and_health(1, 1)
        self.death_rattles = [self.ickyimp_deathrattle]

    def ickyimp_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        _generic_summon_deathrattle(self, 2, Imp(), own_warband, opponent_warband)


class ImpulsiveTrickster(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Impulsive Trickster"
        self.tribe = [TRIBE_DEMON]
        self._set_attack_and_health(2, 2)
        self.max_health = self.health
        self.death_rattles = [self.impulsivetrickster_deathrattle]

    def _set_attack_and_health(self, atk, hp):
        self.max_health = hp
        return super()._set_attack_and_health(atk, hp)

    def add_health(self, incoming_health):
        super().add_health(incoming_health)
        self.max_health += incoming_health

    def impulsivetrickster_deathrattle(
        self, own_warband: Warband, opponent_warband: Warband
    ):
        health_to_transfer = self.max_health
        # TODO Get more evidence
        if own_warband.can_do_battle():
            for _ in range(self.golden):
                get_random_minion(own_warband.minions).add_health(health_to_transfer)


class MicroMummy(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Micro Mummy"
        self.tribe = [TRIBE_MECH]
        self.reborn = True
        self._set_attack_and_health(1, 2)


class MurlocTidehunter(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Murloc Tidehunter"
        self.tribe = [TRIBE_MURLOC]
        self._set_attack_and_health(2, 1)


class Pupbot(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Pupbot"
        self.tribe = [TRIBE_MECH]
        self.set_divine_shield(True)
        self._set_attack_and_health(2, 1)


class RazorfenGeomancer(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Razorfen Geomancer"
        self.tribe = [TRIBE_QUILBOAR]
        self._set_attack_and_health(3, 1)


class RedWhelp(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Red Whelp"
        self.tribe = [TRIBE_DRAGON]
        self._set_attack_and_health(1, 2)

    def pre_combat_effect(self, own_warband: Warband, opponent_warband: Warband):
        damage = len(
            [
                minion
                for minion in own_warband
                if TRIBE_DRAGON in minion.tribe and minion.alive
            ]
        )
        for _ in range(self.golden):
            opponent_warband.sniped(damage, self, own_warband)


class RefreshingAnomaly(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Refreshing Anomaly"
        self.tribe = [TRIBE_ELEMENTAL]
        self._set_attack_and_health(1, 4)


class RockpoolHunter(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Rockpool Hunter"
        self.tribe = [TRIBE_MURLOC]
        self._set_attack_and_health(2, 3)


class Scallywag(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Scallywag"
        self.tribe = [TRIBE_PIRATE]
        self._set_attack_and_health(2, 1)
        self.death_rattles = [self.scallywag_deathrattle]

    def scallywag_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        _generic_summon_deathrattle(self, 1, SkyPirate(), own_warband, opponent_warband)


class ScavengingHyena(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Scavenging Hyena"
        self.tribe = [TRIBE_BEAST]
        self._set_attack_and_health(2, 2)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if TRIBE_BEAST in minion.tribe and minion is not self:
                minion.death_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        self.attack += 2 * self.golden
        self.health += 1 * self.golden


class Sellemental(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Sellemental"
        self.tribe = [TRIBE_ELEMENTAL]
        self._set_attack_and_health(2, 2)


class SunBaconRelaxer(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Sun-Bacon Relaxer"
        self.tribe = [TRIBE_QUILBOAR]
        self._set_attack_and_health(1, 2)


class WrathWeaver(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Wrath Weaver"
        self._set_attack_and_health(1, 3)


# ###### TIER TWO ########


class FreedealingGambler(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Freedealing Gambler"
        self.tier = 2
        self.tribe = [TRIBE_PIRATE]
        self._set_attack_and_health(3, 3)


class GlyphGuadrdian(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Glyph Guadrdian"
        self.tribe = [TRIBE_DRAGON]
        self.tier = 2
        self._set_attack_and_health(2, 4)
        self.pre_attack_observers = [self]

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        self.attack *= 1 + self.golden


class HarvestGolem(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Harvest Golem"
        self.tribe = [TRIBE_MECH]
        self.tier = 2
        self._set_attack_and_health(2, 3)
        self.death_rattles = [self.harvestgolem_deathrattle]

    def harvestgolem_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        _generic_summon_deathrattle(
            self, 1, DamagedGolem(), own_warband, opponent_warband
        )


class Imprisoner(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Imprisoner"
        self.tribe = [TRIBE_DEMON]
        self.tier = 2
        self._set_attack_and_health(3, 3)
        self.taunt = True
        self.death_rattles = [self.imprisoner_deathrattle]

    def imprisoner_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        _generic_summon_deathrattle(self, 1, Imp(), own_warband, opponent_warband)


class KaboomBot(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Kaboom Bot"
        self.tribe = [TRIBE_MECH]
        self.tier = 2
        self._set_attack_and_health(2, 2)
        self.death_rattles = [self.kaboombot_deathrattle]

    def kaboombot_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        if len([x for x in opponent_warband.minions if x.alive]) > 0:
            for _ in range(self.golden):
                opponent_warband.sniped(4, self, own_warband)


class Leapfrogger(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Leapfrogger"
        self.tribe = [TRIBE_BEAST]
        self.tier = 2
        self._set_attack_and_health(3, 3)
        self.death_rattles = [self.leapfrog_deathrattle]

    def leapfrog_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        beasts_alive = [
            x for x in own_warband.minions if TRIBE_BEAST in x.tribe and x.alive
        ]
        if beasts_alive != []:
            receiver = get_random_minion(beasts_alive)
            receiver._add_stats(self.golden, self.golden)
            receiver.death_rattles.append(self.leapfrog_deathrattle)


class MenagerieMug(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Menagerie Mug"
        self.tier = 2
        self._set_attack_and_health(2, 2)


class MetaltoothLeaper(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "MetaltoothLeaper"
        self.tier = 2
        self.tribe = [TRIBE_MECH]
        self._set_attack_and_health(3, 3)


class MoltenRock(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Molten Rock"
        self.tier = 2
        self.tribe = [TRIBE_ELEMENTAL]
        self._set_attack_and_health(2, 4)
        self.taunt = True


class MurlocWarleader(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Murloc Warleader"
        self.tribe = [TRIBE_MURLOC]
        self.tier = 2
        self._set_attack_and_health(3, 3)
        self.death_observer = [self]

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        if self not in own_warband.summon_observers:
            own_warband.summon_observers.append(self)

    def execute_summon_effect(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if TRIBE_MURLOC in minion.tribe and minion is not self:
                minion.attack += 2 * self.golden

    def buff_summoned_minion(self, summoned_minion: Minion, own_warband: Warband):
        if (
            TRIBE_MURLOC in summoned_minion.tribe
            and summoned_minion is not self
            and self.alive
        ):
            summoned_minion.attack += 2 * self.golden

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        for minion in own_warband.minions:
            if TRIBE_MURLOC in minion.tribe and minion is not self:
                minion.attack -= 2 * self.golden


class NathrezimOverseer(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Nathrezim Overseer"
        self.tribe = [TRIBE_DEMON]
        self.tier = 2
        self._set_attack_and_health(2, 4)


class OldMurcEye(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Old Murk-Eye"
        self.tribe = [TRIBE_MURLOC]
        self.tier = 2
        self._set_attack_and_health(2, 4)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband + opponent_warband:
            if (
                TRIBE_MURLOC in minion.tribe
                and minion is not self
                and self not in minion.death_observers
            ):
                minion.death_observers.append(self)

    def execute_summon_effect(self, own_warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if TRIBE_MURLOC in minion.tribe and minion is not self:
                self.attack += self.golden

    def buff_summoned_minion(self, summoned_minion: Minion, own_warband: Warband):
        if (
            TRIBE_MURLOC in summoned_minion.tribe
            and summoned_minion is not self
            and self.alive
        ):
            self.attack += self.golden

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        self.attack -= self.golden


class PartyElemental(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Party Elemental"
        self.tier = 2
        self.tribe = [TRIBE_ELEMENTAL]
        self._set_attack_and_health(3, 2)


class ProphetoftheBoar(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Prophet of the Boar"
        self.tier = 2
        self._set_attack_and_health(3, 3)


class RabidSaurolisk(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Rabid Saurolisk"
        self.tier = 2
        self.tribe = [TRIBE_BEAST]
        self._set_attack_and_health(3, 2)


class Roadboar(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Roadboar"
        self.tier = 2
        self.tribe = [TRIBE_QUILBOAR]
        self._set_attack_and_health(2, 4)
        self.frenzy = True

    def activate_frenzy(self, own_warband: Warband):
        pass
        # TODO add blood gem to hand


class SaltscaleHoncho(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Saltscale Honcho"
        self.tier = 2
        self.tribe = [TRIBE_MURLOC]
        self._set_attack_and_health(3, 2)


class SelflessHero(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Selfless Hero"
        self.tier = 2
        self._set_attack_and_health(2, 1)
        self.death_rattles = [self.selflesshero_deathrattle]

    def selflesshero_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        for _ in range(self.golden):
            no_ds_minions = [
                x for x in own_warband.minions if not x.divine_shield and x.alive
            ]
            if no_ds_minions != []:
                get_random_minion(no_ds_minions).gain_divine_shield(own_warband)


class SewerRat(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Sewer Rat"
        self.tribe = [TRIBE_BEAST]
        self.tier = 2
        self._set_attack_and_health(3, 2)
        self.death_rattles = [self.sewerrat_deathrattle]

    def sewerrat_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        _generic_summon_deathrattle(self, 1, HalfShell(), own_warband, opponent_warband)


class SpawnOfNZoth(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Spawn of N'Zoth"
        self.tier = 2
        self._set_attack_and_health(2, 2)
        self.death_rattles = [self.spawnofnzoth_deathrattle]

    def spawnofnzoth_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion.alive:
                minion._add_stats(self.golden, self.golden)


# TODO skal have en broadcasting funktion som den sender ud til alle abbonenter,
# alle pirates skal abbonere på ham, fx i tilfælde af han bliver golden mid game. ØV
class SouthseaCaptian(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Southsea Captain"
        self.tribe = [TRIBE_PIRATE]
        self.tier = 2
        self._set_attack_and_health(3, 3)
        self.death_observer = [self]

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        if self not in own_warband.summon_observers:
            own_warband.summon_observers.append(self)

    def execute_summon_effect(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if TRIBE_PIRATE in minion.tribe and minion is not self:
                minion.attack += self.golden
                minion.add_health(self.golden)

    def buff_summoned_minion(self, summoned_minion: Minion, own_warband: Warband):
        if (
            TRIBE_PIRATE in summoned_minion.tribe
            and summoned_minion is not self
            and self.alive
        ):
            summoned_minion.attack += self.golden
            summoned_minion.add_health(self.golden)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        for minion in own_warband.minions:
            if TRIBE_PIRATE in minion.tribe and minion is not self:
                minion.attack -= self.golden
                if minion.damage_taken < self.golden:
                    health_loss = self.golden - minion.damage_taken
                    minion.take_damage(health_loss)


class ToughTusk(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Tough Tusk"
        self.tier = 2
        self.tribe = [TRIBE_QUILBOAR]
        self._set_attack_and_health(4, 3)


class UnstableGhoul(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Unstable Ghoul"
        self.tier = 2
        self._set_attack_and_health(1, 3)
        self.death_rattles = [self.unstableghoul_deathrattle]

    def unstableghoul_deathrattle(
        self, own_warband: Warband, opponent_warband: Warband
    ):
        for _ in range(self.golden):
            _aoe_damage(1, self, opponent_warband, own_warband)
            _aoe_damage(1, self, own_warband, opponent_warband)


def _aoe_damage(
    damage: int, dealer_minion: Minion, own_warband: Warband, opponent_warband: Warband
):
    minions_to_damage = [minion for minion in own_warband.minions if minion.alive]
    for minion in minions_to_damage:
        minion.take_damage_2(damage, dealer_minion, own_warband, opponent_warband)


class WhelpSmuggler(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Whelp Smuggler"
        self.tier = 2
        self._set_attack_and_health(2, 5)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if TRIBE_DRAGON in minion.tribe and self not in minion.pre_attack_observers:
                minion.buff_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        dealer_minion.add_health(self.golden)


class YoHoOgre(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Yo-Ho-Ogre"
        self.tier = 2
        self.tribe = [TRIBE_PIRATE]
        self._set_attack_and_health(2, 6)
        self.post_damage_observers[self]

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        combat_sequence(
            self,
            get_next_defender(opponent_warband.minions),
            own_warband,
            opponent_warband,
        )


# ###### TIER THREE ########


class ArmoftheEmpire(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Arm of the Empire"
        self.tier = 3
        self._set_attack_and_health(4, 4)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion.taunt and self not in minion.pre_attack_observers:
                minion.pre_defend_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        receiver_minion.attack += 2 * self.golden


class Bannerboar(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Bannerboar"
        self.tier = 3
        self.tribe = [TRIBE_QUILBOAR]
        self._set_attack_and_health(1, 4)


class BirdBuddy(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Bird Buddy"
        self.tier = 3
        self.avenge_limit = 1
        self._set_attack_and_health(2, 4)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion is not self and self not in minion.divine_observers:
                minion.death_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        if self.avenge_tick():
            for minion in own_warband.minions:
                if TRIBE_BEAST in minion.tribe and minion.alive:
                    minion._add_stats(self.golden, self.golden)


class BrinyBootlegger(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Briny Bootlegger"
        self.tier = 3
        self._set_attack_and_health(4, 4)
        self.tribe = [TRIBE_PIRATE]


class BristlebackBrute(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Bristleback Brute"
        self.tier = 3
        self._set_attack_and_health(4, 4)
        self.tribe = [TRIBE_QUILBOAR]


class BronzeWarden(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Bronze Warden"
        self.tier = 3
        self._set_attack_and_health(2, 1)
        self.tribe = [TRIBE_DRAGON]
        self.reborn = True
        self.set_divine_shield(True)


class BuddingGreenthumb(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Budding Greenthumb"
        self.tier = 3
        self.avenge_limit = 3
        self._set_attack_and_health(1, 4)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion is not self and self not in minion.divine_observers:
                minion.death_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        if self.avenge_tick():
            adjacent_minions = own_warband.get_adjacent_minions(self)
            for minion in adjacent_minions:
                if minion.alive:
                    minion._add_stats(2 * self.golden, self.golden)


class ColdlightSeer(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "ColdlightSeer"
        self.tier = 3
        self.tribe = [TRIBE_MURLOC]
        self._set_attack_and_health(2, 3)


class CracklingCyclone(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Crackling Cyclone"
        self.tier = 3
        self.tribe = [TRIBE_ELEMENTAL]
        self._set_attack_and_health(4, 1)
        self.set_divine_shield(True)
        self.windfury = 2


class DeflectoBot(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Deflect-o-Bot"
        self.tribe = [TRIBE_MECH]
        self.tier = 3
        self._set_attack_and_health(3, 2)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        if self not in own_warband.summon_observers:
            own_warband.summon_observers.append(self)

    def buff_summoned_minion(self, summoned_minion: Minion, own_warband: Warband):
        if (
            TRIBE_MECH in summoned_minion.tribe
            and summoned_minion is not self
            and self.alive
        ):
            self.gain_divine_shield(own_warband)


class FelfinNavigator(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Felfin Navigator"
        self.tribe = [TRIBE_MURLOC]
        self.tier = 3
        self._set_attack_and_health(4, 4)


class Gemsplitter(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Gemsplitter"
        self.tribe = [TRIBE_QUILBOAR]
        self.tier = 3
        self._set_attack_and_health(2, 4)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if self not in minion.divine_observers:
                minion.divine_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        pass
        # TODO add card to hand


class Houndmaster(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Houndmaster"
        self.tier = 3
        self._set_attack_and_health(4, 3)


class Kathranatir(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Kathra'natir"
        self.tribe = [TRIBE_DEMON]
        self.tier = 3
        self._set_attack_and_health(5, 4)
        self.death_observer = [self]

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        if self not in own_warband.summon_observers:
            own_warband.summon_observers.append(self)

    def execute_summon_effect(self, own_warband):
        for minion in own_warband.minions:
            if TRIBE_DEMON in minion.tribe and minion is not self:
                minion.attack += 2 * self.golden

    def buff_summoned_minion(self, summoned_minion: Minion, own_warband: Warband):
        if (
            TRIBE_DEMON in summoned_minion.tribe
            and summoned_minion is not self
            and self.alive
        ):
            summoned_minion.attack += 2 * self.golden

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        for minion in own_warband.minions:
            if TRIBE_DEMON in minion.tribe and minion is not self:
                minion.attack -= 2 * self.golden


class Khadgar(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Khadgar"
        self.tier = 3
        self._set_attack_and_health(2, 2)


class MonstrousMacaw(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Monstrous Macaw"
        self.tribe = [TRIBE_BEAST]
        self.tier = 3
        self._set_attack_and_health(5, 3)
        self.post_attack_observers = [self]

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        for _ in range(self.golden):
            deathrattle_minion = get_deathrattle_minion(own_warband.minions)
            if deathrattle_minion is None:
                break
            execute_deathrattles(deathrattle_minion, own_warband, opponent_warband)


class Necrolyte(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Necrolyte"
        self._set_attack_and_health(3, 3)
        self.tier = 3
        self.tribe = [TRIBE_QUILBOAR]


class RatPack(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Rat Pack"
        self._set_attack_and_health(2, 2)
        self.tier = 3
        self.tribe = [TRIBE_BEAST]
        self.death_rattles = [self.ratpack_deathrattle]

    def ratpack_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        _generic_summon_deathrattle(
            self, self.attack, Rat(), own_warband, opponent_warband
        )


class ReplicatingMenace(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Replicating Menace"
        self.tribe = [TRIBE_MECH]
        self.tier = 3
        self._set_attack_and_health(3, 1)
        self.death_rattles = [self.replicatingmenace_deathrattle]

    def replicatingmenace_deathrattle(
        self, own_warband: Warband, opponent_warband: Warband
    ):
        _generic_summon_deathrattle(self, 3, MicroBot(), own_warband, opponent_warband)


class SaltyLooter(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Salty Looter"
        self._set_attack_and_health(4, 5)
        self.tier = 3
        self.tribe = [TRIBE_PIRATE]


class ScrewjankClunker(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Screwjank Clunker"
        self._set_attack_and_health(2, 5)
        self.tier = 3
        self.tribe = [TRIBE_MECH]


class Smogger(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Smogger"
        self._set_attack_and_health(3, 3)
        self.tier = 3
        self.tribe = [TRIBE_ELEMENTAL]


class SoulDevourer(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Soul Devourer"
        self._set_attack_and_health(3, 3)
        self.tier = 3
        self.tribe = [TRIBE_DEMON]


class SoulJuggler(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Soul Juggler"
        self.tier = 3
        self._set_attack_and_health(3, 5)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if TRIBE_DEMON in minion.tribe and self not in minion.death_observers:
                minion.death_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        for _ in range(self.golden):
            opponent_warband.sniped(3, self, own_warband)


class SouthseaStrongarm(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "SouthseaStrongarm"
        self._set_attack_and_health(4, 3)
        self.tier = 3
        self.tribe = [TRIBE_PIRATE]


class StatisElemental(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Statis Elemental"
        self.tier = 3
        self.tribe = [TRIBE_ELEMENTAL]
        self._set_attack_and_health(4, 4)


class Swolefin(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Swolefin"
        self._set_attack_and_health(4, 2)
        self.tier = 3
        self.tribe = [TRIBE_MURLOC]


class Tarecgosa(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Tarecgosa"
        self._set_attack_and_health(4, 4)
        self.tier = 3
        self.tribe = [TRIBE_DRAGON]


class TwilightEmissary(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Twilight Emissary"
        self.tier = 3
        self.tribe = [TRIBE_DRAGON]
        self._set_attack_and_health(4, 4)


# ###### TIER FOUR ########


class AnnoyoModule(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Annoy-o-Module"
        self.tier = 4
        self.tribe = [TRIBE_MECH]
        self._set_attack_and_health(2, 4)
        self.taunt = True
        self.set_divine_shield(True)


class Bigfernal(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Bigfernal"
        self.tribe = [TRIBE_DEMON]
        self.tier = 4
        self._set_attack_and_health(6, 6)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        if self not in own_warband.summon_observers:
            own_warband.summon_observers.append(self)

    def buff_summoned_minion(self, summoned_minion: Minion, own_warband: Warband):
        if (
            TRIBE_DEMON in summoned_minion.tribe
            and summoned_minion is not self
            and self.alive
        ):
            self._add_stats(self.golden, self.golden)


class Bonker(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Bonker"
        self._set_attack_and_health(3, 7)
        self.tier = 4
        self.windfury = 1
        self.tribe = [TRIBE_QUILBOAR]
        self.post_attack_observers[self]

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        pass
        # TODO add bloodgem to hand


class CaveHydra(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Cave Hydra"
        self._set_attack_and_health(2, 4)
        self.tier = 4
        self.cleave = True
        self.tribe = [TRIBE_BEAST]


class ChampionofYShaarj(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Champion of Y'Shaarj"
        self.tier = 3
        self._set_attack_and_health(4, 4)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion.taunt and self not in minion.pre_attack_observers:
                minion.pre_defend_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        self._add_stats(self.golden, self.golden)


class DrakonidEnforcer(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Drakonid Enforcer"
        self.tribe = [TRIBE_DRAGON]
        self.tier = 4
        self._set_attack_and_health(3, 6)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion.divine_shield and self not in minion.divine_observers:
                minion.divine_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        self.attack += 2 * self.golden
        self.health += 2 * self.golden


class CobaltScalebane(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Cobalt Scalebane"
        self._set_attack_and_health(5, 5)
        self.tier = 4
        self.tribe = [TRIBE_DRAGON]


class DazzlingLightspawn(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Dazzling Lightspawn"
        self._set_attack_and_health(4, 5)
        self.tier = 4
        self.tribe = [TRIBE_ELEMENTAL]


class DefenderofArgus(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Defender of Argus"
        self._set_attack_and_health(3, 3)
        self.tier = 4


class DynamicDuo(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Dynamic Duo"
        self._set_attack_and_health(4, 5)
        self.tier = 4
        self.tribe = [TRIBE_QUILBOAR]


class Goldgrubber(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Goldgrubber"
        self._set_attack_and_health(4, 4)
        self.tier = 4
        self.tribe = [TRIBE_PIRATE]


class GreaseBot(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "GreaseBot"
        self.tribe = [TRIBE_MECH]
        self.tier = 4
        self._set_attack_and_health(3, 6)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion.divine_shield and self not in minion.divine_observers:
                minion.divine_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        dealer_minion._add_stats(2 * self.golden, self.golden)


class Groundshaker(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Groundshaker"
        self._set_attack_and_health(2, 6)
        self.tier = 4
        self.tribe = [TRIBE_QUILBOAR]


class ImpatientDoomsayer(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Impatient Doomsayer"
        self._set_attack_and_health(2, 6)
        self.tier = 4
        self.avenge_limit = 4

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion is not self and self not in minion.divine_observers:
                minion.death_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        if self.avenge_tick():
            pass
            # TODO add card to hand


class MajordomoExecutus(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Majordomo Executus"
        self._set_attack_and_health(6, 3)
        self.tier = 4


class MechanoEgg(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Mechano-Egg"
        self.tribe = [TRIBE_MECH]
        self.tier = 4
        self._set_attack_and_health(0, 5)
        self.death_rattles = [self.mechanoegg_deathrattle]

    def mechanoegg_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        _generic_summon_deathrattle(self, 1, Robosaur(), own_warband, opponent_warband)


class MechanoTank(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Mechano-Tank"
        self.tribe = [TRIBE_MECH]
        self.tier = 4
        self.avenge_limit = 2
        self._set_attack_and_health(6, 3)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion is not self and self not in minion.divine_observers:
                minion.death_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        if self.avenge_tick():
            for _ in range(self.golden):
                target = get_highest_health_minion(opponent_warband.minions)
                if target is not None:
                    target.take_damage_2(6, self, opponent_warband, own_warband)


class MenagerieJug(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Menagerie Mug"
        self._set_attack_and_health(3, 3)
        self.tier = 4


class PeggyBrittlebone(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "PeggyBrittlebone"
        self._set_attack_and_health(6, 5)
        self.tier = 4
        self.tribe = [TRIBE_PIRATE]

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        pirates = [
            minion
            for minion in own_warband.minions
            if TRIBE_PIRATE in minion.tribe and minion is not self
        ]
        buff_target = get_random_minion(pirates)
        if buff_target is not None:
            buff_target._add_stats(self.golden, self.golden)


class PrestorsPyrospawn(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Prestor's Pyrospawn"
        self.tribe = [TRIBE_DRAGON]
        self.tier = 4
        self._set_attack_and_health(3, 5)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if (
                TRIBE_DRAGON in minion.tribe
                and minion is not self
                and self not in minion.pre_attack_observers
            ):
                minion.pre_attack_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        for _ in range(self.golden):
            receiver_minion.take_damage_2(
                3 * self.golden, self, opponent_warband, own_warband
            )


class PrimalfinLookout(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Primalfin Lookout"
        self._set_attack_and_health(3, 2)
        self.tier = 4
        self.tribe = [TRIBE_MURLOC]


class PrizedPromoDrake(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Prized Promo-Drake"
        self._set_attack_and_health(5, 5)
        self.tier = 4
        self.tribe = [TRIBE_DRAGON]

    def pre_combat_effect(self, own_warband: Warband, opponent_warband: Warband):
        dragon_count = len(
            [minion for minion in own_warband.minions if TRIBE_DRAGON in minion.tribe]
        )
        minions_to_buff = own_warband.get_adjacent_minions(self)
        for minion in minions_to_buff:
            minion._add_stats(dragon_count * self.golden, dragon_count * self.golden)


class RecyclingWraith(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "RecyclingWraith"
        self._set_attack_and_health(5, 4)
        self.tier = 4
        self.tribe = [TRIBE_ELEMENTAL]


class RingMatron(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Ring Matron"
        self.tribe = [TRIBE_DEMON]
        self.tier = 4
        self.taunt = True
        self._set_attack_and_health(6, 4)
        self.death_rattles = [self.ringmatron_deathrattle]

    def ringmatron_deathrattle(
        self: Minion, own_warband: Warband, opponent_warband: Warband
    ):
        _generic_summon_deathrattle(self, 2, FieryImp(), own_warband, opponent_warband)


class RipsnarlCaptain(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Ripsnarl Captain"
        self.tribe = [TRIBE_PIRATE]
        self.tier = 4
        self._set_attack_and_health(4, 5)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if TRIBE_PIRATE in minion.tribe and minion is not self:
                minion.pre_attack_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        dealer_minion._add_stats(2 * self.golden, 2 * self.golden)


class SavannahHighmane(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Savannah Highmane"
        self.tribe = [TRIBE_BEAST]
        self.tier = 4
        self._set_attack_and_health(6, 5)
        self.death_rattles = [self.savannahhighmane_deathrattle]

    def savannahhighmane_deathrattle(
        self, own_warband: Warband, opponent_warband: Warband
    ):
        _generic_summon_deathrattle(self, 2, Hyena(), own_warband, opponent_warband)


class WildfireElemental(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Wildfire Elemental"
        self._set_attack_and_health(7, 4)
        self.tier = 4
        self.tribe = [TRIBE_ELEMENTAL]
        self.post_attack_observers = [self]

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        if not receiver_minion.alive:
            overkill_damage = receiver_minion.health
            if overkill_damage > 0:
                next_receivers = opponent_warband.get_adjacent_minions(receiver_minion)
                if next_receivers != []:
                    if len(next_receivers) > self.golden:
                        next_receivers = get_random_minion(next_receivers)
                    for next_receiver in next_receivers:
                        next_receiver.take_damage_2(
                            overkill_damage, self, opponent_warband, own_warband
                        )


class WitchwingNestmatron(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Wildfire Elemental"
        self._set_attack_and_health(3, 5)
        self.tier = 4
        self.avenge_limit = 3

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        if self.avenge_tick():
            pass
            # TODO add card to hand


# ###### TIER FIVE ########


class AgamaggantheGreatBoar(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Agamaggan, the Great Boar"
        self._set_attack_and_health(6, 6)
        self.tier = 5
        self.tribe = [TRIBE_BEAST]


class AggemThorncurse(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Aggem Thornecurse"
        self._set_attack_and_health(3, 6)
        self.tier = 5
        self.tribe = [TRIBE_QUILBOAR]


class AnnihilanBattlemaster(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Annihilan Battlemaster"
        self._set_attack_and_health(3, 1)
        self.tier = 5
        self.tribe = [TRIBE_DEMON]


class BaronRivendare(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Baron Rivendare"
        self._set_attack_and_health(1, 7)
        self.tier = 5


class BrannBronzebeard(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "BrannBronzebeard"
        self._set_attack_and_health(2, 4)
        self.tier = 5


class BristlebackKnight(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Bristleback Knight"
        self.tribe = [TRIBE_QUILBOAR]
        self.tier = 5
        self._set_attack_and_health(4, 8)
        self.windfury = 2
        self.set_divine_shield(True)
        self.frenzy_ready = True

    def activate_frenzy(self, own_warband):
        if self.frenzy_ready:
            self.gain_divine_shield(own_warband)
            self.frenzy = False


class CapnHoggarr(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Cap'n Hoggarr"
        self._set_attack_and_health(6, 6)
        self.tier = 5
        self.tribe = [TRIBE_PIRATE]


class DeadlySpore(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Deadly Spore"
        self._set_attack_and_health(1, 1)
        self.tier = 5
        self.poisonous = True


class HolyMecherel(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Holy Mecherel"
        self.tribe = [TRIBE_MECH]
        self.tier = 5
        self._set_attack_and_health(8, 4)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion.divine_shield and self not in minion.divine_observers:
                minion.divine_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        self.gain_divine_shield(own_warband)


class InsatiableUrzul(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Insatiable Ur'zul"
        self._set_attack_and_health(4, 6)
        self.tier = 5
        self.tribe = [TRIBE_DEMON]
        self.taunt = True


class KangorsApprentice(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Kangor's Apprentice"
        self.tier = 5
        self._set_attack_and_health(3, 6)
        self.death_rattles = [self.kangor_deathrattle]

    def kangor_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        minions_to_summon = own_warband.dead_mechs[: 2 * self.golden]
        if len(minions_to_summon) > 0:
            own_warband.summon_minions(self, minions_to_summon, opponent_warband)


class KingBagurgle(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "King Bagurgle"
        self.tribe = [TRIBE_MURLOC]
        self.tier = 5
        self._set_attack_and_health(6, 3)
        self.death_rattles = [self.kingbagurgle_deathrattle]

    def kingbagurgle_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if TRIBE_MURLOC in minion.tribe and minion.alive:
                minion._add_stats(2 * self.golden, 2 * self.golden)


class LightfangEnforcer(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Lightfang Enforcer"
        self._set_attack_and_health(2, 2)
        self.tier = 5


class MamaBear(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Mama Bear"
        self.tribe = [TRIBE_BEAST]
        self.tier = 5
        self._set_attack_and_health(4, 4)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        if self not in own_warband.summon_observers:
            own_warband.summon_observers.append(self)

    def buff_summoned_minion(self, summoned_minion: Minion, own_warband: Warband):
        if (
            TRIBE_BEAST in summoned_minion.tribe
            and summoned_minion is not self
            and self.alive
        ):
            summoned_minion._add_stats(5 * self.golden, 5 * self.golden)


class MasterofRealities(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Master of Realities"
        self._set_attack_and_health(6, 6)
        self.tier = 5

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if TRIBE_ELEMENTAL in minion.tribe and self not in minion.buff_observers:
                minion.buff_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion,
        receiver_minion: Minion,
        own_warband: Warband,
        opponent_warband: Warband,
    ):
        self._add_stats(self.golden, self.golden)


class Murozond(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Murozond"
        self._set_attack_and_health(5, 5)
        self.tier = 5
        self.tribe = [TRIBE_DRAGON]


class NomiKitchenNightmare(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Nomi, Kitchen Nightmare"
        self.tier = 5
        self._set_attack_and_health(4, 4)


class PalescaleCrocolisk(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Palescale Crocolisk"
        self.tribe = [TRIBE_BEAST]
        self.tier = 5
        self.avenge_limit = 2
        self._set_attack_and_health(4, 5)
        self.death_rattles = [self.palescalecrocolisk_deathrattle]

    def palescalecrocolisk_deathrattle(
        self, own_warband: Warband, opponent_warband: Warband
    ):
        beasts_alive = [
            minion
            for minion in own_warband.minions
            if TRIBE_BEAST in minion.tribe and minion.alive
        ]
        if beasts_alive != []:
            get_random_minion(beasts_alive)._add_stats(6 * self.golden, 6 * self.golden)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion is not self and self not in minion.divine_observers:
                minion.death_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        if self.avenge_tick():
            beasts_alive = [
                minion
                for minion in own_warband.minions
                if TRIBE_BEAST in minion.tribe and minion.alive and minion is not self
            ]
            if beasts_alive != []:
                get_random_minion(beasts_alive)._add_stats(
                    6 * self.golden, 6 * self.golden
                )


class RazorgoretheUntamed(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Razorgore, the Untamed"
        self.tier = 5
        self.tribe = [TRIBE_DRAGON]
        self._set_attack_and_health(4, 6)


class ReanimatingRattler(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Reanimating Rattler"
        self._set_attack_and_health(7, 3)
        self.tier = 5
        self.tribe = [TRIBE_BEAST]


class SISefin(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "SI:Sefin"
        self.tribe = [TRIBE_MURLOC]
        self.tier = 5
        self.avenge_limit = 3
        self._set_attack_and_health(2, 6)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion is not self and self not in minion.divine_observers:
                minion.death_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        if self.avenge_tick():
            for _ in range(self.golden):
                potential_recievers = [
                    minion
                    for minion in own_warband.minions
                    if minion.alive
                    and TRIBE_MURLOC in minion.tribe
                    and not minion.poisonous
                ]
                if potential_recievers != []:
                    get_random_minion(potential_recievers).poisonous = True
                else:
                    break


class StrongshellScavenger(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Strongshell Scavenger"
        self._set_attack_and_health(2, 3)
        self.tier = 5


class TavernTempest(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Tavern Tempest"
        self._set_attack_and_health(4, 4)
        self.tier = 5
        self.tribe = [TRIBE_ELEMENTAL]


class TonyTwoTusk(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Tony Two-Tusk"
        self.tribe = [TRIBE_PIRATE]
        self.tier = 5
        self.avenge_limit = 5
        self._set_attack_and_health(4, 6)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion is not self and self not in minion.divine_observers:
                minion.death_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        if self.avenge_tick():
            for _ in range(self.golden):
                potential_recievers = [
                    minion
                    for minion in own_warband.minions
                    if minion.alive
                    and TRIBE_PIRATE in minion.tribe
                    and minion.golden == 1
                ]
                if potential_recievers != []:
                    get_random_minion(potential_recievers).make_golden()
                else:
                    break


class Voidlord(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Voidlord"
        self.tribe = [TRIBE_DEMON]
        self.tier = 5
        self.taunt = True
        self._set_attack_and_health(3, 9)
        self.death_rattles = [self.voidlord_deathrattle]

    def voidlord_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        _generic_summon_deathrattle(
            self, 3, Voidwalker(), own_warband, opponent_warband
        )


# ###### TIER SIX ########


class Amalgadon(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Amalgadon"
        self.tier = 6
        self.tribe = [
            TRIBE_BEAST,
            TRIBE_DEMON,
            TRIBE_DRAGON,
            TRIBE_ELEMENTAL,
            TRIBE_MECH,
            TRIBE_MURLOC,
            TRIBE_PIRATE,
            TRIBE_QUILBOAR,
        ]
        self._set_attack_and_health(6, 6)

    def amalgadon_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        _generic_summon_deathrattle(self, 2, Plant(), own_warband, opponent_warband)


class ArchdruidHamuul(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Archdruid Hamuul"
        self._set_attack_and_health(4, 4)
        self.tier = 6


class CaptainFlatTusk(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Captain Flat Tusk"
        self._set_attack_and_health(9, 6)
        self.tier = 6
        self.tribe = [TRIBE_QUILBOAR]


class Charlga(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Charlga"
        self._set_attack_and_health(4, 4)
        self.tier = 6
        self.tribe = [TRIBE_QUILBOAR]


class DreadAdmiralEliza(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Dread Admiral Eliza"
        self.tribe = [TRIBE_PIRATE]
        self.tier = 6
        self._set_attack_and_health(6, 7)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if (
                TRIBE_PIRATE in minion.tribe
                and minion not in minion.pre_attack_observers
            ):
                minion.pre_attack_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        for minion in own_warband.minions:
            minion._add_stats(2 * self.golden, 1 * self.golden)


class FamishedFelbat(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "FamishedFelbat"
        self._set_attack_and_health(9, 5)
        self.tier = 6
        self.tribe = [TRIBE_DEMON]


class FoeReaper4000(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Foe Reaper 4000"
        self._set_attack_and_health(6, 9)
        self.tier = 6
        self.tribe = [TRIBE_MECH]
        self.cleave = True


class GentleDjinni(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Gentle Djinni"
        self.tribe = [TRIBE_ELEMENTAL]
        self.tier = 6
        self.taunt = True
        self._set_attack_and_health(4, 5)
        self.death_rattles = [self.gentledjinni_deathrattle]

    def gentledjinni_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        possible_elementals = [
            RefreshingAnomaly(),
            Sellemental(),
            MoltenRock(),
            PartyElemental(),
            CracklingCyclone(),
            Smogger(),
            StatisElemental(),
            DazzlingLightspawn(),
            RecyclingWraith(),
            WildfireElemental(),
            TavernTempest(),
            Amalgadon(),
            LilRag(),
        ]
        chosen_elementals = [
            deepcopy(possible_elementals[randint(0, len(possible_elementals) - 1)])
            for _ in range(self.golden)
        ]
        own_warband.summon_minions(self, chosen_elementals, opponent_warband)
        # TODO add card to hand


class Ghastcoiler(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Ghastcoiler"
        self.tribe = [TRIBE_BEAST]
        self.tier = 6
        self._set_attack_and_health(7, 7)
        self.death_rattles = [self.ghastcoiler_deathrattle]

    def ghastcoiler_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        possible_minions = [
            IckyImp(),
            ImpulsiveTrickster(),
            Scallywag(),
            HarvestGolem(),
            Imprisoner(),
            KaboomBot(),
            Leapfrogger(),
            SelflessHero(),
            SewerRat(),
            SpawnOfNZoth(),
            UnstableGhoul(),
            RatPack(),
            ReplicatingMenace(),
            MechanoEgg(),
            RingMatron(),
            SavannahHighmane(),
            KangorsApprentice(),
            KingBagurgle(),
            PalescaleCrocolisk(),
            Voidlord(),
            GentleDjinni(),
            GoldrintheGreatWolf(),
            NadinaTheRed(),
            OmegaBuster(),
        ]
        chosen_minions = [
            deepcopy(possible_minions[randint(0, len(possible_minions) - 1)])
            for _ in range(2 * self.golden)
        ]
        own_warband.summon_minions(self, chosen_minions, opponent_warband)


class GoldrintheGreatWolf(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Goldrinn, the Great Wolf"
        self.tribe = [TRIBE_BEAST]
        self.tier = 6
        self._set_attack_and_health(4, 4)
        self.death_rattles = [self.goldrinthegreatwolf_deathrattle]

    def goldrinthegreatwolf_deathrattle(
        self, own_warband: Warband, opponent_warband: Warband
    ):
        beasts_alive = [
            x for x in own_warband.minions if TRIBE_BEAST in x.tribe and x.alive
        ]
        for beast in beasts_alive:
            beast._add_stats(5 * self.golden, 5 * self.golden)


class ImpMama(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Imp Mama"
        self.tribe = [TRIBE_DEMON]
        self.tier = 6
        self._set_attack_and_health(6, 10)
        self.post_damage_observers = [self]

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        if own_warband._get_available_boardspace(self.golden) > 0:
            possible_minions = [
                IckyImp(),
                ImpulsiveTrickster(),
                Imprisoner(),
                NathrezimOverseer(),
                Kathranatir(),
                SoulDevourer(),
                Bigfernal(),
                RingMatron(),
                AnnihilanBattlemaster(),
                InsatiableUrzul(),
                Voidlord(),
                Amalgadon(),
                FamishedFelbat(),
            ]
            chosen_minions = [
                deepcopy(possible_minions[randint(0, len(possible_minions) - 1)])
                for _ in range(self.golden)
            ]
            for chosen_minion in chosen_minions:
                chosen_minion.taunt = True
            own_warband.summon_minions(self, chosen_minions, opponent_warband)


class Kalecgos(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Kalecgos"
        self.tier = 6
        self.tribe = [TRIBE_DRAGON]
        self._set_attack_and_health(4, 12)


class LilRag(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Lil' Rag"
        self._set_attack_and_health(6, 6)
        self.tier = 6
        self.tribe = [TRIBE_ELEMENTAL]


class Maexxna(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Maexxna"
        self._set_attack_and_health(2, 8)
        self.tier = 6
        self.tribe = [TRIBE_BEAST]
        self.poisonous = True


class NadinaTheRed(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Nadina the Red"
        self.tier = 6
        self._set_attack_and_health(7, 5)
        self.death_rattles = [self.nadinathered_deathrattle]

    def nadinathered_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        dragons_alive = [
            x for x in own_warband.minions if x.tribe == TRIBE_DRAGON and x.alive
        ]
        for dragon in dragons_alive:
            dragon.gain_divine_shield()


class NosyLooter(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Noosy Looter"
        self._set_attack_and_health(7, 6)
        self.tier = 6
        self.tribe = [TRIBE_PIRATE]


class OmegaBuster(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Omega Buster"
        self.tribe = [TRIBE_MECH]
        self.tier = 6
        self._set_attack_and_health(6, 6)
        self.death_rattles = [self.omegabuster_deathrattle]

    def omegabuster_deathrattle(self, own_warband: Warband, opponent_warband: Warband):
        buff_size = (6 - own_warband._get_available_boardspace(6)) * self.golden
        _generic_summon_deathrattle(self, 6, MicroBot(), own_warband, opponent_warband)
        if buff_size > 0:
            for minion in own_warband.minions:
                if minion.tribe == TRIBE_MECH and minion.alive:
                    minion._add_stats(buff_size, buff_size)


class SeafoodSlinger(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Seafood Slinger"
        self._set_attack_and_health(5, 5)
        self.tier = 6


class ZappSlywick(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Zapp Slywick"
        self._set_attack_and_health(7, 10)
        self.tier = 6
        self.windfury = 1


# ###### TOKEN MINIONS ########


class Tabbycat(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Tabbycat"
        self.tribe = [TRIBE_BEAST]
        self._set_attack_and_health(1, 1)


class SkyPirate(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Sky Pirate"
        self.tribe = [TRIBE_PIRATE]
        self._set_attack_and_health(1, 1)

    def execute_summon_effect(self, own_warband: Warband, opponent_warband: Warband):
        combat_sequence(
            self,
            get_next_defender(opponent_warband.minions),
            own_warband,
            opponent_warband,
        )


class MicroBot(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Microbot"
        self.tribe = [TRIBE_MECH]
        self._set_attack_and_health(1, 1)


class Robosaur(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Robosaur"
        self.tribe = [TRIBE_MECH]
        self._set_attack_and_health(8, 8)


class Imp(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Imp"
        self.tribe = [TRIBE_DEMON]
        self._set_attack_and_health(1, 1)


class Voidwalker(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Voidwalker"
        self.tribe = [TRIBE_DEMON]
        self.taunt = True
        self._set_attack_and_health(1, 3)


class FieryImp(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Imp"
        self.tribe = [TRIBE_DEMON]
        self._set_attack_and_health(3, 2)


class DamagedGolem(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Damaged Golem"
        self.tribe = [TRIBE_MECH]
        self._set_attack_and_health(2, 1)


class HalfShell(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Half-Shell"
        self.tribe = [TRIBE_BEAST]
        self.taunt = True
        self._set_attack_and_health(2, 3)


class Rat(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Rat"
        self.tribe = [TRIBE_BEAST]
        self._set_attack_and_health(1, 1)


class Hyena(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Hyena"
        self.tribe = [TRIBE_BEAST]
        self._set_attack_and_health(2, 2)


class Plant(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Plant"
        self._set_attack_and_health(1, 1)

    def make_golden(self):
        pass


class FishOfNzoth(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Fish of N'Zoth"
        self._set_attack_and_health(2, 2)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion.death_rattles != [] and self not in minion.death_observers:
                minion.death_observers.append(self)

    def notify(
        self,
        dealer_minion: Minion = None,
        receiver_minion: Minion = None,
        own_warband: Warband = None,
        opponent_warband: Warband = None,
    ):
        for _ in range(self.golden):
            for deathrattle in dealer_minion.death_rattles:
                self.death_rattles.append[deathrattle]


# #### UTILITY FUNCTIONS #####


def _generic_summon_deathrattle(
    deathrattle_owner: Minion,
    number_of_minions: int,
    minion: Minion,
    own_warband: Warband,
    opponent_warband: Warband,
):
    minions = deathrattle_owner._setup_minions_to_summon(number_of_minions, minion)
    own_warband.summon_minions(deathrattle_owner, minions, opponent_warband)
