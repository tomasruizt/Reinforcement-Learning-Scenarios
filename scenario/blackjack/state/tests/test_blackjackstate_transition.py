import unittest

from scenario.blackjack.cards_deck import Hand, Card
from scenario.blackjack.state import BlackjackState
from scenario.blackjack.state import Transition


class TransitionTest(unittest.TestCase):

    def test_target_draws_card_old_state_unchanged(self):
        initial_state = self._setup_initial_state()
        unchanged_initial_state = self._setup_initial_state()
        Transition(initial_state).dealer().draw(Card("10"))

        self.assertEqual(initial_state, unchanged_initial_state)

    def test_target_draws_card_player_gets_new_card(self):
        initial_state = self._setup_initial_state()
        new_card_name = "A"
        new_state = Transition(initial_state).player().draw(Card(new_card_name))

        self.assertFalse(new_card_name in initial_state.player_hand.card_names)
        self.assertTrue(new_card_name in new_state.player_hand.card_names)
        self.assertFalse(new_card_name in new_state.dealer_hand.card_names)
        self.assertTrue(self._states_are_equal_except_for_hands(
            initial_state, new_state))

    def test_target_draws_card_dealer_gets_new_card(self):
        initial_state = self._setup_initial_state()
        new_card_name = "A"
        new_state = Transition(initial_state).dealer().draw(Card(new_card_name))

        self.assertFalse(new_card_name in initial_state.dealer_hand.card_names)
        self.assertTrue(new_card_name in new_state.dealer_hand.card_names)
        self.assertFalse(new_card_name in new_state.player_hand.card_names)
        self.assertTrue(self._states_are_equal_except_for_hands(
            initial_state, new_state))

    def test_target_passes_old_state_unchanged(self):
        initial_state = self._setup_initial_state()
        unchanged_initial_state = self._setup_initial_state()
        Transition(initial_state).dealer().pass_turn()

        self.assertEqual(initial_state, unchanged_initial_state)

    def test_target_passes_player_passed(self):
        initial_state = self._setup_initial_state()
        new_state = Transition(initial_state).player().pass_turn()

        self.assertFalse(initial_state.player_has_passed)
        self.assertTrue(new_state.player_has_passed)
        self.assertFalse(new_state.dealer_has_passed)
        self.assertTrue(self._states_are_equal_except_for_has_passed_variables(
            initial_state, new_state))

    def test_target_passes_dealer_passed(self):
        initial_state = self._setup_initial_state()
        new_state = Transition(initial_state).dealer().pass_turn()

        self.assertFalse(initial_state.dealer_has_passed)
        self.assertTrue(new_state.dealer_has_passed)
        self.assertFalse(new_state.player_has_passed)
        self.assertTrue(self._states_are_equal_except_for_has_passed_variables(
            initial_state, new_state))

    @staticmethod
    def _setup_initial_state() -> BlackjackState:
        player_hand = Hand([Card("10"), Card("10")])
        dealer_hand = Hand([Card("10")])
        return BlackjackState.new_initial_state(player_hand, dealer_hand)

    @staticmethod
    def _states_are_equal_except_for_hands(
            state1: BlackjackState, state2: BlackjackState) -> bool:
        return (
            state1.dealer_has_passed == state2.dealer_has_passed
            and state1.player_has_passed == state2. player_has_passed
            and state1.current_bet == state2.current_bet
            and state1.action_space == state2.action_space
        )

    @staticmethod
    def _states_are_equal_except_for_has_passed_variables(
            state1: BlackjackState, state2: BlackjackState) -> bool:
        return (
            state1.player_hand == state2.player_hand
            and state1.dealer_hand == state2.dealer_hand
            and state1.current_bet == state2.current_bet
            and state1.action_space == state2.action_space
        )
