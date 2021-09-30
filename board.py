from typing import List
from warband import Warband, calculate_damage, get_next_defender
from copy import deepcopy
from random import randint, shuffle
from minion import Minion, notify_observers, on_death


class Board(object):
    top_warband: Warband
    bottom_warband: Warband
    attacker: Warband
    defender: Warband

    def __init__(self, top_warband, bottom_warband) -> None:
        self.top_warband = deepcopy(top_warband)
        self.bottom_warband = deepcopy(bottom_warband)
        self.top_warband.name = "Top Warband"
        self.bottom_warband.name = "Bottom Warband"

        register_observers(self.top_warband, self.bottom_warband)
        register_observers(self.bottom_warband, self.top_warband)

    def battle(self):
        self._coin_flip()
        for minion in self.attacker.minions:
            minion.pre_combat_effect(self.attacker, self.defender)
        for minion in self.defender.minions:
            minion.pre_combat_effect(self.defender, self.attacker)
        turn = 0
        while self._can_battle():
            atk_minion: Minion = self.attacker.get_next_attacker()
            if atk_minion is None:
                if not self.defender.has_attackers():
                    break
                self._handover_initiative()
                continue
            for _ in range(
                atk_minion.windfury * atk_minion.golden
                if atk_minion.windfury > 1
                else 1
            ):
                def_minion = get_next_defender(self.defender.minions)

                # Printing board state:
                self._print_board_state(turn, atk_minion, def_minion)

                fight(
                    atk_minion,
                    def_minion,
                    self.attacker,
                    self.defender,
                )

                self._update_warbands()
                # TODO What if windfury minion is dead?
                if not self._can_battle() or not atk_minion.alive:
                    break

            turn += 1
            self._handover_initiative()

        winner = self._announce_winner()

        # Print outcome
        # self._print_outcome(winner)
        if winner is not None:
            if winner == self.top_warband:
                return [2, calculate_damage(winner.minions), turn]
            return [0, calculate_damage(winner.minions), turn]
        else:
            return [1, 0, turn]

    def _fight_outcome(
        self,
        dealer_minion: Minion,
        receiver_minion: Minion,
        opponent_warband: Warband,
        own_warband: Warband,
    ):
        # check if minion has frenzy and activate if
        alive = dealer_minion.update_life_status()
        if receiver_minion.attack > 0:
            notify_observers(
                dealer_minion.post_damage_observers,
                dealer_minion,
                receiver_minion,
                own_warband,
                opponent_warband,
            )
        if alive and receiver_minion.attack > 0:
            dealer_minion.activate_frenzy(own_warband)
        elif not alive:
            dealer_minion.update_death_observers()
            for death_observer in dealer_minion.death_observers:
                death_observer.notify(
                    dealer_minion, receiver_minion, own_warband, opponent_warband
                )
            for deathrattle in dealer_minion.death_rattles:
                deathrattle(own_warband, opponent_warband)
            register_observers(own_warband, opponent_warband)

    def _coin_flip(self):
        if len(self.top_warband.minions) == len(self.bottom_warband.minions):
            if randint(0, 1) == 0:
                self._top_first()
            else:
                self._bottom_first()
        elif len(self.top_warband.minions) > len(self.bottom_warband.minions):
            self._top_first()
        else:
            self._bottom_first()

    def _announce_winner(self):
        if (
            self.top_warband.minions_alive() > 0
            and self.bottom_warband.minions_alive() > 0
        ):
            return None
        if len(self.top_warband.minions) > 0:
            return self.top_warband
        elif len(self.bottom_warband.minions) > 0:
            return self.bottom_warband
        return None

    def _handover_initiative(self):
        temp = self.attacker
        self.attacker = self.defender
        self.defender = temp

    def _update_warbands(self):
        self.top_warband.update_warband()
        self.bottom_warband.update_warband()

    def _top_first(self):
        self.attacker = self.top_warband
        self.defender = self.bottom_warband

    def _bottom_first(self):
        self.attacker = self.bottom_warband
        self.defender = self.top_warband

    def _can_battle(self):
        if self.top_warband.can_do_battle() and self.bottom_warband.can_do_battle():
            return True
        return False

    def _print_board_state(self, turn, atk_minion, def_minion):
        print(f"----------- TURN {turn} -------------")

        print()
        print("Top:")
        print(self.top_warband)
        print()
        if atk_minion in self.top_warband.minions:
            print(f"Attacker: {atk_minion} {self.attacker.minions.index(atk_minion)}")
        else:
            print(f"Defender: {def_minion} {self.defender.minions.index(def_minion)}")
        print()
        print("Bottom:")
        print(self.bottom_warband)
        print()
        if atk_minion in self.bottom_warband.minions:
            print(f"Attacker: {atk_minion} {self.attacker.minions.index(atk_minion)}")
        else:
            print(f"Defender: {def_minion} {self.defender.minions.index(def_minion)}")
        print()
        print(f"------ END OF TURN {turn} -------------")

    def _print_outcome(self, winner):
        print(f"------------- OUTCOME ---------------")
        print(f"The winner is: {winner}")
        print(f"------------ GAME OVER --------------")


def register_observers(own_warband: Warband, opponent_warband: Warband):
    for minion in own_warband.minions:
        minion.register_observable(own_warband, opponent_warband)


# def notify_observers(
#     observers: List[Minion],
#     dealer_minion: Minion,
#     receiver_minion: Minion,
#     own_warband: Warband,
#     opponent_warband: Warband,
# ):
#     for observer in observers:
#         observer.notify(dealer_minion, receiver_minion, own_warband, opponent_warband)


def combat_sequence(
    atk_minion: Minion,
    def_minion: Minion,
    atk_warband: Warband,
    def_warband: Warband,
):
    notify_observers(
        atk_minion.pre_attack_observers,
        atk_minion,
        def_minion,
        atk_warband,
        def_warband,
    )
    if not def_minion.alive:
        # TODO needs to be handled differently, deathrattles need to trigger/reborn, more
        return

    notify_observers(
        def_minion.pre_defend_observers,
        def_minion,
        atk_minion,
        def_warband,
        atk_warband,
    )
    # Replaced by take_damage_2
    atk_minion.take_damage_2(
        def_minion.attack,
        def_minion,
        atk_warband,
        def_warband,
    )
    def_minion.take_damage_2(
        atk_minion.attack,
        atk_minion,
        def_warband,
        atk_warband,
    )


def fight(
    atk_minion: Minion,
    def_minion: Minion,
    atk_warband: Warband,
    def_warband: Warband,
):
    combat_sequence(atk_minion, def_minion, atk_warband, def_warband)

    already_handled = []
    deathrattle_handler = {}
    while dead_minions(atk_warband, def_warband, deathrattle_handler, already_handled):
        for minion in deathrattle_handler:
            own_warband, opponent_warband = deathrattle_handler[minion]
            on_death(minion, None, own_warband, opponent_warband)
            already_handled.append(minion)
        deathrattle_handler = {}

    if atk_minion.cleave:
        adj_minions = def_warband.get_adjacent_minions(def_minion)
        if len(adj_minions) > 0:
            for adj_minion in adj_minions:
                adj_minion.take_damage_2(
                    atk_minion.attack, atk_minion, def_warband, atk_warband
                )
    atk_minion.number_of_attacks += 1


def dead_minions(
    own_warband: Warband,
    opponent_warband: Warband,
    deathrattle_handler: dict,
    already_handled: List,
) -> bool:
    warbands = [own_warband, opponent_warband]
    shuffle(warbands)
    any_drs = add_deathrattles(
        warbands[0], warbands[1], deathrattle_handler, already_handled
    )
    any_drs2 = add_deathrattles(
        warbands[1], warbands[0], deathrattle_handler, already_handled
    )
    return any_drs or any_drs2


def add_deathrattles(
    own_warband: Warband,
    opponent_warband: Warband,
    deathrattle_handler: dict,
    already_handled: List,
) -> bool:
    return_value = False
    for minion in own_warband.minions:
        if (
            not minion.alive
            and minion not in deathrattle_handler
            and minion not in already_handled
        ):
            deathrattle_handler[minion] = [own_warband, opponent_warband]
            return_value = True
    return return_value
