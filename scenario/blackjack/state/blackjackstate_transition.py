from enum import Enum, auto

from scenario.blackjack.cards_deck import Card
from scenario.blackjack.state import BlackjackState


class Transition:
    """Used to transition from one BlackjackState to the next"""

    # TODO: Action space changes while transitioning.

    class Target(Enum):
        PLAYER = auto()
        DEALER = auto()

    def target_draws_card(self, from_state: BlackjackState,
                          new_card: Card, target: Target) -> BlackjackState:
        """
        From the current state, transition to a new state where either
        the player or the dealer are dealt the input new card.
        :param from_state: The current state.
        :param new_card: The new card that is dealt.
        :param target: Whom to deal the card to. Either Target.PLAYER or
        Target.DEALER.
        :return: The new BlackjackState.
        """
        assert target in (self.Target.PLAYER, self.Target.DEALER)

        if target == self.Target.PLAYER:
            player_hand = from_state.player_hand.add_card(new_card)
            dealer_hand = from_state.dealer_hand
        else:
            player_hand = from_state.player_hand
            dealer_hand = from_state.dealer_hand.add_card(new_card)

        return BlackjackState(
            player_hand=player_hand,
            dealer_hand=dealer_hand,
            player_has_passed=from_state.player_has_passed,
            dealer_has_passed=from_state.dealer_has_passed,
            current_bet=from_state.current_bet,
            action_space=from_state.action_space
        )

    def target_passes(self, from_state: BlackjackState, target: Target) \
            -> BlackjackState:
        """
        Transition from the current state to a new one, where the player
        has passed.
        :param from_state: The current state.
        :param target: Who decided to pass. Either Target.PLAYER or
        Target.DEALER.
        :return: The new BlackjackState.
        """
        assert target in (self.Target.PLAYER, self.Target.DEALER)

        if target == self.Target.PLAYER:
            player_has_passed = True
            dealer_has_passed = from_state.dealer_has_passed
        else:
            player_has_passed = from_state.player_has_passed
            dealer_has_passed = True

        return BlackjackState(
            player_hand=from_state.player_hand,
            dealer_hand=from_state.dealer_hand,
            current_bet=from_state.current_bet,
            player_has_passed=player_has_passed,
            dealer_has_passed=dealer_has_passed,
            action_space=from_state.action_space
        )
