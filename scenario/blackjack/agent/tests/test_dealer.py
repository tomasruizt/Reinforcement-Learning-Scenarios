import unittest

from scenario.blackjack.action import BlackjackAction
from scenario.blackjack.agent import Dealer
from scenario.blackjack.cards_deck import Hand, Card
from scenario.blackjack.state import BlackjackState, Transition


class DealerTest(unittest.TestCase):
    DEALER = Dealer()  # Dealer doesnt need a restart
    _transition = Transition()

    def test_choose_action_pass_if_player_busted(self):
        bust_player_state = self._setup_bust_player_state()
        expected_dealer_action = BlackjackAction.PASS

        agent_choice = self.DEALER.choose_action(bust_player_state)
        self.assertEqual(expected_dealer_action, agent_choice.action_chosen)

    def test_choose_action_pass_if_score_equal_than_player(self):
        equal_scores_state = self._setup_equal_scores_state()
        expected_dealer_action = BlackjackAction.PASS

        agent_choice = self.DEALER.choose_action(equal_scores_state)
        self.assertEqual(expected_dealer_action, agent_choice.action_chosen)

    def test_choose_action_pass_if_score_greater_than_player(self):
        winning_state_for_dealer = self._setup_winning_state_for(
            Transition.Target.DEALER)
        expected_dealer_action = BlackjackAction.PASS

        agent_choice = self.DEALER.choose_action(winning_state_for_dealer)
        self.assertEqual(expected_dealer_action, agent_choice.action_chosen)

    def test_choose_action_draw_if_lower_score_than_opponent_and_under_21(self):
        winning_state_for_player = self._setup_winning_state_for(
            Transition.Target.PLAYER)
        expected_dealer_action = BlackjackAction.DRAW

        agent_choice = self.DEALER.choose_action(winning_state_for_player)
        self.assertEqual(expected_dealer_action, agent_choice.action_chosen)

    def test_choose_action_agent_choice_contains_state_unchanged(self):
        equal_scores_state = self._setup_equal_scores_state()
        expected_agent_choice_state = self._setup_equal_scores_state()

        agent_choice = self.DEALER.choose_action(equal_scores_state)
        self.assertEqual(agent_choice.from_state, expected_agent_choice_state)

    # Auxiliary methods

    def _setup_bust_player_state(self) -> BlackjackState:
        """In this state the player is bust while the dealer is not."""
        initial_state = BlackjackState.new_initial_state(
            player_hand=Hand(cards_list=[Card("K"), Card("K")]),
            dealer_hand=Hand(cards_list=[Card("K")]),
        )
        bust_player_state = self._transition.target_draws_card(
            from_state=initial_state, new_card=Card("K"),
            target=Transition.Target.PLAYER)
        return bust_player_state

    def _setup_equal_scores_state(self) -> BlackjackState:
        """Both dealer and player have the same score in this state."""
        initial_state = BlackjackState.new_initial_state(
            player_hand=Hand(cards_list=[Card("10"), Card("10")]),
            dealer_hand=Hand(cards_list=[Card("10")])
        )
        equal_scores_state = self._transition.target_draws_card(
            initial_state, Card("10"), Transition.Target.DEALER)
        return equal_scores_state

    def _setup_winning_state_for(self, target: Transition.Target):
        """The target is for whom the state is advantageous: either
        Target.PLAYER or Target.DEALER"""
        equal_scores_state = self._setup_equal_scores_state()
        winning_state_for_target = self._transition.target_draws_card(
            from_state=equal_scores_state, new_card=Card("A"),
            target=target)  # Target gets to 21 score
        return winning_state_for_target
