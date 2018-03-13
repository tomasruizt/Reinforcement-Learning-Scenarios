from scenario.blackjack.cards_deck import Card
from scenario.blackjack.state import BlackjackState


class Transition:
    """Used to transition from one BlackjackState to the next"""

    def __init__(self, from_state: BlackjackState):
        """Initializes a Transition with a reference to the state is
        exiting."""
        self._from_state = from_state

        self._dealer_has_passed = None
        self._dealer_hand = None
        self._player_has_passed = None
        self._player_hand = None

        self._agent_is_player = None

    def player(self):
        """Selects the player as the agent who choose an action to trigger a
        state transition."""
        self._dealer_has_passed = self._from_state.dealer_has_passed
        self._dealer_hand = self._from_state.dealer_hand
        self._agent_is_player = True
        return TransitionActionSelection(transition=self)

    def dealer(self):
        """Selects the dealer as the agent who choose an action to trigger a
        state transition."""
        self._player_has_passed = self._from_state.player_has_passed
        self._player_hand = self._from_state.player_hand
        self._agent_is_player = False
        return TransitionActionSelection(transition=self)

    def _draw(self, new_card: Card) -> BlackjackState:
        """Private method used to set the action to draw card"""
        if self._agent_is_player:
            self._player_hand = self._from_state.player_hand.add_card(new_card)
            self._player_has_passed = self._from_state.player_has_passed
        else:
            self._dealer_hand = self._from_state.dealer_hand.add_card(new_card)
            self._dealer_has_passed = self._from_state.dealer_has_passed
        return self._build_new_state()

    def _pass(self) -> BlackjackState:
        """Private method used to set the action to pass turn"""
        if self._agent_is_player:
            self._player_hand = self._from_state.player_hand
            self._player_has_passed = True
        else:
            self._dealer_hand = self._from_state.dealer_hand
            self._dealer_has_passed = True
        return self._build_new_state()

    def _build_new_state(self) -> BlackjackState:
        """
        Builds the new state and sets default values for current_bet and
        action_space.
        """
        # TODO: Action space changes while transitioning.
        return BlackjackState(
            player_hand=self._player_hand,
            dealer_hand=self._dealer_hand,
            current_bet=self._from_state.current_bet,
            player_has_passed=self._player_has_passed,
            dealer_has_passed=self._dealer_has_passed,
            action_space=self._from_state.action_space
        )


class TransitionActionSelection:
    def __init__(self, transition: Transition):
        self._transition = transition

    def draw(self, new_card: Card) -> BlackjackState:
        """
        The set agent is dealt a card, which is added to their hand.
        Then return the new state the game is in.
        :param new_card: The new card the agent is dealt.
        :return: The new BlackjackState.
        """
        return self._transition._draw(new_card)

    def pass_turn(self):
        """
        Transitions to the state where the set player has passes and
        returns the new state the game is in.
        :return: The new BlackjackState.
        """
        return self._transition._pass()
