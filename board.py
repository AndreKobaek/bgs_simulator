from warband import Warband, get_next_defender
from copy import deepcopy
from random import randint
from minion import Minion


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

        self._register_observers(self.top_warband, self.bottom_warband)
        self._register_observers(self.bottom_warband, self.top_warband)

    def battle(self):
        self._coin_flip()

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
                # self._print_board_state(turn, atk_minion, def_minion)
                self._fight(atk_minion, def_minion)

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
            damage = winner.calculate_damage()
            if winner == self.top_warband:
                return [2, damage]
            return [0, damage]
        else:
            return [1, 0]

    def _fight(self, atk_minion: Minion, def_minion: Minion):

        for pre_attack_observer in atk_minion.pre_attack_observers:
            pre_attack_observer.notify(
                atk_minion, def_minion, self.attacker, self.defender
            )
            # TODO update if minion is dead

        for pre_defend_observer in def_minion.pre_defend_observers:
            pre_defend_observer.notify(
                atk_minion, def_minion, self.defender, self.attacker
            )
        self._combat_sequence(atk_minion, def_minion, self.attacker)
        self._combat_sequence(def_minion, atk_minion, self.defender)
        self._fight_outcome(atk_minion, def_minion, self.defender, self.attacker)
        self._fight_outcome(def_minion, atk_minion, self.attacker, self.defender)

        if atk_minion.cleave:
            adj_minions = self.defender.get_adjacent_minions(def_minion)
            if len(adj_minions) > 0:
                for adj_minion in adj_minions:
                    self._combat_sequence(adj_minion, atk_minion)
        atk_minion.number_of_attacks += 1

    def _combat_sequence(
        self, dealer_minion: Minion, receiver_minion: Minion, own_warband
    ):
        # Attacker health updates
        if dealer_minion.divine_shield and receiver_minion.attack > 0:
            dealer_minion.pop_divine_shield(own_warband)
        elif receiver_minion.poisonous and receiver_minion.attack > 0:
            dealer_minion.alive = False
        else:
            dealer_minion.health -= receiver_minion.attack

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
            for minion in dealer_minion.post_damage_observers:
                minion.notify(
                    dealer_minion, receiver_minion, own_warband, opponent_warband
                )
        if alive and receiver_minion.attack > 0:
            dealer_minion.activate_frenzy(own_warband)
        elif not alive:
            for death_observer in dealer_minion.death_observers:
                death_observer.notify(
                    dealer_minion, receiver_minion, own_warband, opponent_warband
                )
            for deathrattle in dealer_minion.death_rattles:
                deathrattle(dealer_minion, own_warband, opponent_warband)
            self._register_observers(own_warband, opponent_warband)

    def _get_observer_list(self, minion):
        if minion in self.top_warband.minions:
            return self.top_death_observers
        else:
            return self.bottom_death_observers

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

    def _register_observers(self, own_warband, opponent_warband):
        for minion in own_warband.minions:
            minion.register_observable(own_warband, opponent_warband)

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
