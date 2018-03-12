from scenario.blackjack.cards_deck import Card
from scenario.blackjack.state import BlackjackState


class Transition:
    """Used to transition from one BlackjackState to the next"""
    # TODO: Action space changes while transitioning.

    @staticmethod
    def player_draws_card(from_state: BlackjackState, new_card: Card) -> \
            BlackjackState:
        return BlackjackState(
            player_hand=from_state.player_hand.add_card(new_card),
            dealer_hand=from_state.dealer_hand,
            player_has_passed=from_state.player_has_passed,
            dealer_has_passed=from_state.dealer_has_passed,
            current_bet=from_state.current_bet,
            action_space=from_state.action_space
        )

    @staticmethod
    def player_passes(from_state: BlackjackState) -> BlackjackState:
        return BlackjackState(
            player_hand=from_state.player_hand,
            dealer_hand=from_state.dealer_hand,
            current_bet=from_state.current_bet,
            player_has_passed=True,
            dealer_has_passed=from_state.dealer_has_passed,
            action_space=from_state.action_space
        )

    @staticmethod
    def dealer_draws_card(from_state: BlackjackState, new_card: Card) -> \
            BlackjackState:
        return BlackjackState(
            player_hand=from_state.player_hand,
            dealer_hand=from_state.dealer_hand.add_card(new_card),
            current_bet=from_state.current_bet,
            player_has_passed=from_state.player_has_passed,
            dealer_has_passed=from_state.dealer_has_passed,
            action_space=from_state.action_space
        )

    @staticmethod
    def dealer_passes(from_state: BlackjackState) -> BlackjackState:
        return BlackjackState(
            player_hand=from_state.player_hand,
            dealer_hand=from_state.dealer_hand,
            current_bet=from_state.current_bet,
            player_has_passed=from_state.player_has_passed,
            dealer_has_passed=True,
            action_space=from_state.action_space
        )
