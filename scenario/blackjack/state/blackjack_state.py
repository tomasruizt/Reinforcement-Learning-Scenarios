from typing import Iterable

from rl.state import DiscreteState

from scenario.blackjack.action import BlackjackAction
from scenario.blackjack.cards_deck.hand import Hand


class BlackjackState(DiscreteState):
    """
    An object containing all the state information for a single player
    Blackjack game against one opponent.
    """

    def __init__(self, player_hand: Hand, dealer_hand: Hand,
                 player_has_passed: bool, dealer_has_passed: bool,
                 current_bet: int, action_space: Iterable[BlackjackAction]):
        """Private constructor used to create new states."""
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.current_bet = current_bet
        self.player_has_passed = player_has_passed
        self.dealer_has_passed = dealer_has_passed
        super().__init__(action_space)

    def is_final(self) -> bool:
        """
        Tells whether this state is final. The necessary condition for
        a state to be final is for the dealer to be done with his play.
        Be it either because he busted, or because he decided to pass.
        """
        return self.dealer_hand.score > 21 or self.dealer_has_passed

    @staticmethod
    def new_initial_state(player_hand: Hand, dealer_hand: Hand,
            current_bet: int, action_space:Iterable[BlackjackAction]):
        """
        Creates a new BlackjackState with the minimum information needed.
        :param action_space: The initial action space.
        :param player_hand: The initial player hand.
        :param dealer_hand: The initial dealer hand.
        :param current_bet: The bet of the player.
        :return: The new BlackjackState object.
        """
        assert sum(player_hand.quantities) is 2
        assert sum(dealer_hand.quantities) is 1

        return BlackjackState(
            player_hand=player_hand,
            dealer_hand=dealer_hand,
            current_bet=current_bet,
            player_has_passed=False,
            dealer_has_passed=False,
            action_space=action_space
        )
