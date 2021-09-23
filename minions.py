from copy import deepcopy
from random import randint
from warband import Warband
from warband import get_random_minion
from minion import Minion
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


class OmegaBuster(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Omega Buster"
        self.tribe = TRIBE_MECH
        self.tier = 6
        self._set_attack_and_health(6, 6)
        self.death_rattles = [omegabuster_deathrattle]


class SpawnOfNZoth(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Spawn of N'Zoth"
        self.tier = 2
        self._set_attack_and_health(2, 2)
        self.death_rattles = [spawnofnzoth_deathrattle]


class UnstableGhoul(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Unstable Ghoul"
        self.tier = 2
        self._set_attack_and_health(1, 3)
        self.death_rattles = [unstableghoul_deathrattle]


class Ghastcoiler(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Ghastcoiler"
        self.tribe = TRIBE_BEAST
        self.tier = 6
        self._set_attack_and_health(7, 7)
        self.death_rattles = [ghastcoiler_deathrattle]


class MicroBot(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Microbot"
        self.tribe = TRIBE_MECH
        self._set_attack_and_health(1, 1)


class CracklingCyclone(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Crackling Cyclone"
        self.tier = 3
        self.tribe = TRIBE_ELEMENTAL
        self._set_attack_and_health(4, 1)
        self.windfury = 2
        self.divine_shield = True


class MoltenRock(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Molten Rock"
        self.tier = 2
        self.tribe = TRIBE_ELEMENTAL
        self._set_attack_and_health(2, 4)
        self.taunt = True


class Robosaur(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Robosaur"
        self.tribe = TRIBE_MECH
        self._set_attack_and_health(8, 8)


class Sellemental(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Sellemental"
        self.tribe = TRIBE_ELEMENTAL
        self._set_attack_and_health(2, 2)


class EvolvingChromawing(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Evolving Chromawing"
        self.tribe = TRIBE_DRAGON
        self._set_attack_and_health(1, 3)


class RazorgoretheUntamed(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Razorgore, the Untamed"
        self.tier = 5
        self.tribe = TRIBE_DRAGON
        self._set_attack_and_health(4, 6)


class Kalecgos(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Kalecgos"
        self.tier = 6
        self.tribe = TRIBE_DRAGON
        self._set_attack_and_health(4, 12)


class Amalgadon(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Amalgadon"
        self.tier = 6
        # TODO Fix tribe any
        # TODO deathrattle
        self.tribe = TRIBE_DRAGON
        self._set_attack_and_health(6, 6)


class Imp(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Imp"
        self.tribe = TRIBE_DEMON
        self._set_attack_and_health(1, 1)


class DeckSwabbie(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Deck Swabbie"
        self.tribe = TRIBE_PIRATE
        self._set_attack_and_health(2, 2)


class Voidwalker(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Voidwalker"
        self.tribe = TRIBE_DEMON
        self.taunt = True
        self._set_attack_and_health(1, 3)


class FieryImp(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Imp"
        self.tribe = TRIBE_DEMON
        self._set_attack_and_health(3, 2)


class IckyImp(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Icky Imp"
        self.tribe = TRIBE_DEMON
        self._set_attack_and_health(1, 1)
        self.death_rattles = [ickyimp_deathrattle]


class ImpulsiveTrickster(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Impulsive Trickster"
        self.tribe = TRIBE_DEMON
        self._set_attack_and_health(2, 2)
        self.max_health = self.health
        self.death_rattles = [impulsivetrickster_deathrattle]

    def _set_attack_and_health(self, atk, hp):
        self.max_health = hp
        return super()._set_attack_and_health(atk, hp)

    def add_health(self, incoming_health):
        super().add_health(incoming_health)
        self.max_health += incoming_health


class Imprisoner(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Imprisoner"
        self.tribe = TRIBE_DEMON
        self.tier = 2
        self._set_attack_and_health(3, 3)
        self.taunt = True
        self.death_rattles = [imprisoner_deathrattle]


class HarvestGolem(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Harvest Golem"
        self.tribe = TRIBE_MECH
        self.tier = 2
        self._set_attack_and_health(2, 3)
        self.death_rattles = [harvestgolem_deathrattle]


class DamagedGolem(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Damaged Golem"
        self.tribe = TRIBE_MECH
        self._set_attack_and_health(2, 1)


class KaboomBot(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Kaboom Bot"
        self.tribe = TRIBE_MECH
        self.tier = 2
        self._set_attack_and_health(2, 2)
        self.death_rattles = [kaboombot_deathrattle]


class SelflessHero(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Selfless Hero"
        self.tier = 2
        self._set_attack_and_health(2, 1)
        self.death_rattles = [selflesshero_deathrattle]


class HalfShell(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Half-Shell"
        self.tribe = TRIBE_BEAST
        self.taunt = True
        self._set_attack_and_health(2, 3)


class SewerRat(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Sewer Rat"
        self.tribe = TRIBE_BEAST
        self.tier = 2
        self._set_attack_and_health(3, 2)
        self.death_rattles = [sewerrat_deathrattle]


class Rat(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Rat"
        self.tribe = TRIBE_BEAST
        self._set_attack_and_health(1, 1)


class AnnoyoModule(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Annoy-o-Module"
        self.tier = 4
        self.tribe = TRIBE_MECH
        self._set_attack_and_health(2, 4)
        self.taunt = True
        self.divine_shield = True


class Hyena(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Hyena"
        self.tribe = TRIBE_BEAST
        self._set_attack_and_health(2, 2)


class Leapfrogger(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Leapfrogger"
        self.tribe = TRIBE_BEAST
        self.tier = 2
        self._set_attack_and_health(3, 3)
        self.death_rattles = [self.leapfrog_deathrattle]

    def leapfrog_deathrattle(
        self, deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
    ):
        beasts_alive = [
            x for x in own_warband.minions if x.tribe == TRIBE_BEAST and x.alive
        ]
        if len(beasts_alive) > 0:
            receiver = get_random_minion(beasts_alive)
            receiver._add_stats(self.golden, self.golden)
            receiver.death_rattles.append(self.leapfrog_deathrattle)


class DrakonidEnforcer(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Drakonid Enforcer"
        self.tribe = TRIBE_DRAGON
        self.tier = 4
        self._set_attack_and_health(3, 6)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion.divine_shield and self not in minion.divine_observers:
                minion.divine_observers.append(self)

    def notify(
        self,
        dealer_minion=None,
        receiver_minion=None,
        own_warband=None,
        opponent_warband=None,
    ):
        self.attack += 2 * self.golden
        self.health += 2 * self.golden


class MurlocWarleader(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Murloc Warleader"
        self.tribe = TRIBE_MURLOC
        self.tier = 2
        self._set_attack_and_health(3, 3)
        self.death_observer = [self]

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        if self not in own_warband.summon_observers:
            own_warband.summon_observers.append(self)

    # TODO add to summon part
    def execute_summon_effect(self, own_warband):
        for minion in own_warband.minions:
            if minion.tribe == TRIBE_MURLOC and minion is not self:
                minion.attack += 2

    def buff_summoned_minion(self, summoned_minion: Minion):
        if (
            summoned_minion.tribe == TRIBE_MURLOC
            and summoned_minion is not self
            and self.alive
        ):
            summoned_minion.attack += 2

    def notify(
        self,
        dealer_minion=None,
        receiver_minion=None,
        own_warband: Warband = None,
        opponent_warband=None,
    ):
        for minion in own_warband.minions:
            if minion.tribe == TRIBE_MURLOC and minion is not self:
                minion.attack -= 2 * self.golden


class HolyMecherel(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Holy Mecherel"
        self.tribe = TRIBE_MECH
        self.tier = 5
        self._set_attack_and_health(8, 4)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion.divine_shield and self not in minion.divine_observers:
                minion.divine_observers.append(self)

    def notify(
        self,
        dealer_minion=None,
        receiver_minion=None,
        own_warband=None,
        opponent_warband=None,
    ):
        self.gain_divine_shield(own_warband)


class GreaseBot(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "GreaseBot"
        self.tribe = TRIBE_MECH
        self.tier = 4
        self._set_attack_and_health(3, 6)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion.divine_shield and self not in minion.divine_observers:
                minion.divine_observers.append(self)

    def notify(
        self,
        dealer_minion=None,
        receiver_minion=None,
        own_warband=None,
        opponent_warband=None,
    ):
        dealer_minion._add_stats(2 * self.golden, self.golden)


class RipsnarlCaptain(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Ripsnarl Captain"
        self.tribe = TRIBE_PIRATE
        self.tier = 4
        self._set_attack_and_health(4, 5)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion.tribe == TRIBE_PIRATE and minion is not self:
                minion.pre_attack_observers.append(self)

    def notify(
        self,
        dealer_minion=None,
        receiver_minion=None,
        own_warband=None,
        opponent_warband=None,
    ):
        dealer_minion._add_stats(2 * self.golden, 2 * self.golden)


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
        dealer_minion=None,
        receiver_minion=None,
        own_warband=None,
        opponent_warband=None,
    ):
        receiver_minion.attack += 2 * self.golden


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
        dealer_minion=None,
        receiver_minion=None,
        own_warband=None,
        opponent_warband=None,
    ):
        self._add_stats(self.golden, self.golden)


class ImpMama(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Imp Mama"
        self.tribe = TRIBE_DEMON
        self.tier = 6
        self._set_attack_and_health(6, 10)
        self.post_damage_observers = [self]

    def notify(
        self,
        dealer_minion=None,
        receiver_minion=None,
        own_warband=None,
        opponent_warband=None,
    ):
        if own_warband._get_available_boardspace(self.golden) > 0:
            possible_minions = [
                IckyImp(),
                ImpulsiveTrickster(),
                Imprisoner(),
                # TODO:
                # NathrezimOverseer(),
                # Kathranatir(),
                # SoulDevourer(),
                # Bigfernal(),
                RingMatron(),
                # AnnihilanBattlemaster(),
                # InsatiableUrzul(),
                Voidlord(),
                Amalgadon(),
                # Famished Felbat(),
            ]
            chosen_minions = [
                deepcopy(possible_minions[randint(0, len(possible_minions) - 1)])
                for _ in range(self.golden)
            ]
            for chosen_minion in chosen_minions:
                chosen_minion.taunt = True
            own_warband.summon_minions(self, chosen_minions)


class GlyphGuadrdian(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Glyph Guadrdian"
        self.tribe = TRIBE_DRAGON
        self.tier = 2
        self._set_attack_and_health(2, 4)
        self.pre_attack_observers = [self]

    def notify(
        self,
        dealer_minion=None,
        receiver_minion=None,
        own_warband=None,
        opponent_warband=None,
    ):
        self.attack *= 1 + self.golden


class DreadAdmiralEliza(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Dread Admiral Eliza"
        self.tribe = TRIBE_PIRATE
        self.tier = 6
        self._set_attack_and_health(6, 7)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if (
                minion.tribe == TRIBE_PIRATE
                and minion not in minion.pre_attack_observers
            ):
                minion.pre_attack_observers.append(self)

    def notify(
        self,
        dealer_minion=None,
        receiver_minion=None,
        own_warband=None,
        opponent_warband=None,
    ):
        for minion in own_warband.minions:
            minion._add_stats(2 * self.golden, 1 * self.golden)


class ScavengingHyena(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Scavenging Hyena"
        self.tribe = TRIBE_BEAST
        self._set_attack_and_health(2, 2)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion.tribe == TRIBE_BEAST and minion is not self:
                minion.death_observers.append(self)

    def notify(
        self,
        dealer_minion=None,
        receiver_minion=None,
        own_warband=None,
        opponent_warband=None,
    ):
        self.attack += 2 * self.golden
        self.health += 1 * self.golden


class SoulJuggler(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Soul Juggler"
        self.tier = 3
        self._set_attack_and_health(3, 5)

    def register_observable(self, own_warband: Warband, opponent_warband: Warband):
        for minion in own_warband.minions:
            if minion.tribe == TRIBE_DEMON and self not in minion.death_observers:
                minion.death_observers.append(self)

    def notify(
        self,
        dealer_minion=None,
        receiver_minion=None,
        own_warband=None,
        opponent_warband=None,
    ):
        for _ in range(self.golden):
            opponent_warband.sniped(3)


class BristlebackKnight(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Bristleback Knight"
        self.tribe = TRIBE_QUILBOAR
        self.tier = 5
        self._set_attack_and_health(4, 8)
        self.windfury = 2
        self.divine_shield = True
        self.frenzy_ready = True

    def activate_frenzy(self, own_warband):
        if self.frenzy_ready:
            self.gain_divine_shield(own_warband)
            self.frenzy = False


class KangorsApprentice(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Kangor's Apprentice"
        self.tier = 5
        self._set_attack_and_health(3, 6)
        self.death_rattles = [kangor_deathrattle]


class RatPack(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Rat Pack"
        self.tribe = TRIBE_BEAST
        self.tier = 3
        self._set_attack_and_health(2, 2)
        self.death_rattles = [ratpack_deathrattle]


class ReplicatingMenace(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Replicating Menace"
        self.tribe = TRIBE_MECH
        self.tier = 3
        self._set_attack_and_health(3, 1)
        self.death_rattles = [replicatingmenace_deathrattle]


class MechanoEgg(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Mechano-Egg"
        self.tribe = TRIBE_MECH
        self.tier = 4
        self._set_attack_and_health(0, 5)
        self.death_rattles = [mechanoegg_deathrattle]


class RingMatron(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Ring Matron"
        self.tribe = TRIBE_DEMON
        self.tier = 4
        self.taunt = True
        self._set_attack_and_health(6, 4)
        self.death_rattles = [ringmatron_deathrattle]


class SavannahHighmane(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Savannah Highmane"
        self.tribe = TRIBE_BEAST
        self.tier = 4
        self._set_attack_and_health(6, 5)
        self.death_rattles = [savannahhighmane_deathrattle]


class Voidlord(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Voidlord"
        self.tribe = TRIBE_DEMON
        self.tier = 5
        self.taunt = True
        self._set_attack_and_health(3, 9)
        self.death_rattles = [voidlord_deathrattle]


class KingBagurgle(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "King Bagurgle"
        self.tribe = TRIBE_MURLOC
        self.tier = 5
        self._set_attack_and_health(6, 3)
        self.death_rattles = [kingbagurgle_deathrattle]


class PalescaleCrocolisk(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Palescale Crocolisk"
        self.tribe = TRIBE_BEAST
        self.tier = 5
        self._set_attack_and_health(4, 5)
        self.death_rattles = [palescalecrocolisk_deathrattle]


class NadinaTheRed(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Nadina the Red"
        self.tier = 6
        self._set_attack_and_health(7, 5)
        self.death_rattles = [nadinathered_deathrattle]


class GoldrintheGreatWolf(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Goldrinn, the Great Wolf"
        self.tribe = TRIBE_BEAST
        self.tier = 6
        self._set_attack_and_health(4, 4)
        self.death_rattles = [goldrinthegreatwolf_deathrattle]


class GentleDjinni(Minion):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Gentle Djinni"
        self.tribe = TRIBE_ELEMENTAL
        self.tier = 6
        self.taunt = True
        self._set_attack_and_health(4, 5)
        self.death_rattles = [gentledjinni_deathrattle]


# TIER 1
# TODO Scallywag
# TIER 2
# TODO Unstable Ghoul


def impulsivetrickster_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    health_to_transfer = deathrattle_owner.max_health
    # TODO Get more evidence
    if own_warband.can_do_battle():
        for _ in range(deathrattle_owner.golden):
            get_random_minion(own_warband.minions).add_health(health_to_transfer)


# def leapfrog_deathrattle(
#     deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
# ):
#     beasts_alive = [
#         x for x in own_warband.minions if x.tribe == TRIBE_BEAST and x.alive
#     ]
#     if len(beasts_alive) > 0:
#         receiver = get_random_minion(beasts_alive)
#         receiver._add_stats(deathrattle_owner.golden, deathrattle_owner.golden)
#         receiver.death_rattles.append(leapfrog_deathrattle)


def kangor_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    minions_to_summon = own_warband.dead_mechs[: 2 * deathrattle_owner.golden]
    if len(minions_to_summon) > 0:
        own_warband.summon_minions(deathrattle_owner, minions_to_summon)


def omegabuster_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    buff_size = (
        6 - own_warband._get_available_boardspace(6)
    ) * deathrattle_owner.golden
    _generic_summon_deathrattle(deathrattle_owner, 6, MicroBot(), own_warband)
    if buff_size > 0:
        for minion in own_warband.minions:
            if minion.tribe == TRIBE_MECH and minion is not deathrattle_owner:
                minion._add_stats(buff_size, buff_size)


def spawnofnzoth_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    for minion in own_warband.minions:
        if minion is not deathrattle_owner:
            minion._add_stats(deathrattle_owner.golden, deathrattle_owner.golden)


def ghastcoiler_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    possible_minions = [
        IckyImp(),
        HarvestGolem(),
        Imprisoner(),
        KaboomBot(),
        Leapfrogger(),
        SelflessHero(),
        SewerRat(),
        SpawnOfNZoth(),
        # UnstableGhoul(),
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
        for _ in range(2 * deathrattle_owner.golden)
    ]
    own_warband.summon_minions(deathrattle_owner, chosen_minions)


def _generic_summon_deathrattle(
    deathrattle_owner: Minion,
    number_of_minions: int,
    minion: Minion,
    own_warband: Warband,
):
    minions = deathrattle_owner._setup_minions_to_summon(number_of_minions, minion)
    own_warband.summon_minions(deathrattle_owner, minions)


def ickyimp_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    _generic_summon_deathrattle(deathrattle_owner, 2, Imp(), own_warband)


def imprisoner_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    _generic_summon_deathrattle(deathrattle_owner, 1, Imp(), own_warband)


def harvestgolem_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    _generic_summon_deathrattle(deathrattle_owner, 1, DamagedGolem(), own_warband)


def kaboombot_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    if len([x for x in opponent_warband.minions if x.alive]) > 0:
        for _ in range(deathrattle_owner.golden):
            opponent_warband.sniped(4)


def selflesshero_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    for _ in range(deathrattle_owner.golden):
        no_ds_minions = [
            x for x in own_warband.minions if not x.divine_shield and x.alive
        ]
        if no_ds_minions != []:
            get_random_minion(no_ds_minions).gain_divine_shield(own_warband)


def sewerrat_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    _generic_summon_deathrattle(deathrattle_owner, 1, HalfShell(), own_warband)


def ratpack_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    _generic_summon_deathrattle(
        deathrattle_owner, deathrattle_owner.attack, Rat(), own_warband
    )


def replicatingmenace_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    _generic_summon_deathrattle(deathrattle_owner, 3, MicroBot(), own_warband)


def mechanoegg_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    _generic_summon_deathrattle(deathrattle_owner, 1, Robosaur(), own_warband)


def ringmatron_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    _generic_summon_deathrattle(deathrattle_owner, 2, FieryImp(), own_warband)


def savannahhighmane_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    _generic_summon_deathrattle(deathrattle_owner, 2, Hyena(), own_warband)


def voidlord_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    _generic_summon_deathrattle(deathrattle_owner, 3, Voidwalker(), own_warband)


def kingbagurgle_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    for minion in own_warband.minions:
        if minion.tribe == TRIBE_MURLOC and minion is not deathrattle_owner:
            minion._add_stats(
                2 * deathrattle_owner.golden, 2 * deathrattle_owner.golden
            )


def palescalecrocolisk_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    beasts_alive = [
        x
        for x in own_warband.minions
        if x.tribe == TRIBE_BEAST and x is not deathrattle_owner
    ]
    if len(beasts_alive) > 0:
        get_random_minion(beasts_alive)._add_stats(
            6 * deathrattle_owner.golden, 6 * deathrattle_owner.golden
        )


def nadinathered_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    dragons_alive = [x for x in own_warband.minions if x.tribe == TRIBE_DRAGON]
    for dragon in dragons_alive:
        dragon.gain_divine_shield()


def goldrinthegreatwolf_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    beasts_alive = [
        x
        for x in own_warband.minions
        if x.tribe == TRIBE_BEAST and x is not deathrattle_owner
    ]
    for beast in beasts_alive:
        beast._add_stats(5 * deathrattle_owner.golden, 5 * deathrattle_owner.golden)


def gentledjinni_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    possible_elementals = [Sellemental(), MoltenRock(), CracklingCyclone()]
    chosen_elementals = [
        deepcopy(possible_elementals[randint(0, len(possible_elementals) - 1)])
        for _ in range(deathrattle_owner.golden)
    ]
    own_warband.summon_minions(deathrattle_owner, chosen_elementals)


def unstableghoul_deathrattle(
    deathrattle_owner: Minion, own_warband: Warband, opponent_warband: Warband
):
    minions_to_damage = [minion for minion in own_warband.minions if minion.alive] + [
        minion for minion in opponent_warband.minions if minion.alive
    ]
    for minion in minions_to_damage:
        if minion.divine_shield:
            minion.divine_shield = False
        else:
            minion.health -= deathrattle_owner.golden
    # TODO Hvornår er update af alive??
