from typing import Iterable

from rl.state import DiscreteState

from scenario.blackjack.action import BlackjackAction
from scenario.blackjack.cards_deck.hand import Hand


class BlackjackState(DiscreteState):
    """
    An object containing all the state information for a single player
    Blackjack game against one opponent.
    """

    DEFAULT_BET = 1
    DEFAULT_ACTION_SPACE = (BlackjackAction.DRAW, BlackjackAction.PASS)

    def __init__(self, player_hand: Hand, dealer_hand: Hand,
                 player_has_passed: bool, dealer_has_passed: bool,
                 current_bet: int, action_space: Iterable[BlackjackAction]):
        """Private constructor used to create new states."""
        self._assert_input(player_hand, dealer_hand, current_bet,
                           player_has_passed, dealer_has_passed, action_space)
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

    @classmethod
    def new_initial_state(cls, player_hand: Hand, dealer_hand: Hand):
        """
        Creates a new BlackjackState with the minimum information needed.
        :param player_hand: The initial player hand.
        :param dealer_hand: The initial dealer hand.
        :return: The new BlackjackState object.
        """
        assert sum(player_hand.quantities) is 2
        assert sum(dealer_hand.quantities) is 1

        return BlackjackState(
            player_hand=player_hand,
            dealer_hand=dealer_hand,
            player_has_passed=False,
            dealer_has_passed=False,
            current_bet=cls.DEFAULT_BET,
            action_space=cls.DEFAULT_ACTION_SPACE
        )

    def __eq__(self, other):
        return (self.player_hand == other.player_hand
                and self.dealer_hand == other.dealer_hand
                and self.dealer_has_passed == other.dealer_has_passed
                and self.player_has_passed == other.player_has_passed
                and self.current_bet == other.current_bet
                and self.action_space == other.action_space)

    @staticmethod
    def _assert_input(player_hand, dealer_hand, current_bet,
                      player_passed, dealer_passed, action_space):
        """Assert that no input is None"""
        assert (
            player_hand is not None
            and dealer_hand is not None
            and current_bet is not None
            and player_passed is not None
            and dealer_passed is not None
            and action_space is not None
        )
