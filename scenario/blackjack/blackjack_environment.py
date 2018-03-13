from rl.agent_choice import DiscreteAgentChoice
from rl.environment import DiscreteEnvironment
from rl.episode import DiscreteEpisode

from scenario.blackjack.action import BlackjackAction
from scenario.blackjack.agent import Dealer
from scenario.blackjack.cards_deck import Hand, PokerCardsDeck
from scenario.blackjack.state import BlackjackState, Transition


class BlackjackEnvironment(DiscreteEnvironment):
    """
    An implementation of Environment that simulates the BlackJack game.
    """

    def __init__(self, dealer: Dealer = Dealer(),
                 shuffled_deck=PokerCardsDeck(), transition=Transition()):
        """
        Initializes the Blackjack environment with input deck
        :param dealer: The Dealer instance that will be part of the
        Blackjack environment.
        :param shuffled_deck: The deck to draw cards from.
        :param transition: The class that manages Blackjack
        state transitions.
        """
        self._dealer = dealer
        self._shuffled_deck = shuffled_deck
        self._transition = transition

    def get_initial_state(self) -> BlackjackState:
        """
        Returns an initial state formed by drawing two cards from the
        deck for the player and one card for the dealer.
        :return: The initial state.
        """
        initial_player_hand = Hand([self._shuffled_deck.draw_card(),
                                    self._shuffled_deck.draw_card()])
        dealer_hand = Hand([self._shuffled_deck.draw_card()])
        return BlackjackState.new_initial_state(
            player_hand=initial_player_hand,
            dealer_hand=dealer_hand)

    def evaluate_agent_choice(
            self, agent_choice: DiscreteAgentChoice) -> DiscreteEpisode:
        """
        Evaluates whether the player wants a new card or not, and changes his
        hand accordingly. Also, in case the player busted or passed, it will
        pass the turn on to the dealer.
        :param agent_choice: The agent choice containing whether the wants
        to draw a new card or passes.
        :return: A full episode with the player's old hand, his decision and
        the new hand he has.
        """
        new_state = self._get_new_state_from(agent_choice)
        reward = self._calculate_reward(new_state)
        return DiscreteEpisode(
            start_state=agent_choice.from_state,
            agent_action=agent_choice.action_chosen,
            reward=reward,
            end_state=new_state
        )

    # PRIVATE FUNCTIONS

    @staticmethod
    def _player_has_no_more_choices(state: BlackjackState) -> bool:
        """Evaluates whether the player can still make choices."""
        return state.player_has_passed or state.player_hand.score > 21

    def _get_new_state_from(self, choice: DiscreteAgentChoice) -> \
            BlackjackState:
        """
        Takes the initial state in the input choice and uses the chosen
        action to transition to a new state.
        :param choice: The choice that describes from what state what
        action the Agent chose.
        :return: The new state.
        """
        state = choice.from_state
        player_action_name = choice.action_chosen
        self._validate_action(player_action_name)

        if player_action_name is BlackjackAction.DRAW:
            new_card = self._shuffled_deck.draw_card()
            new_state = self._transition.player_draws_card(
                from_state=state, new_card=new_card)
        else:
            new_state = self._transition.player_passes(from_state=state)

        if self._player_has_no_more_choices(new_state):
            return self._complete_state_with_dealer_play(new_state)
        else:
            return new_state

    @staticmethod
    def _calculate_reward(state: BlackjackState) -> int:
        if not state.is_final():
            return 0

        player_score = state.player_hand.score
        dealer_score = state.dealer_hand.score

        if player_score > 21:
            return -state.current_bet
        elif dealer_score > 21:
            return state.current_bet
        else:
            player_wins = dealer_score < player_score
            return state.current_bet if player_wins else -state.current_bet

    def _complete_state_with_dealer_play(self, from_state: BlackjackState) -> \
            BlackjackState:
        """Let the dealer play, and update his hand."""
        current_state = from_state
        while not current_state.is_final():
            current_state = self._dealer_takes_single_choice(current_state)
        return current_state

    def _dealer_takes_single_choice(self, from_state: BlackjackState) -> \
            BlackjackState:
        """The dealer makes a single choice and returns the new state."""
        dealer_choice = self._dealer.choose_action(from_state)
        dealer_action_name = dealer_choice.action_chosen
        self._validate_action(dealer_action_name)

        if dealer_action_name is BlackjackAction.DRAW:
            new_card = self._shuffled_deck.draw_card()
            return self._transition.dealer_draws_card(from_state, new_card)
        else:
            return self._transition.dealer_passes(from_state=from_state)

    @staticmethod
    def _validate_action(action: BlackjackAction):
        """Validate that the action is in the action space."""
        # TODO: Should in the action space of the state it was taken from!
        assert action in BlackjackState.DEFAULT_ACTION_SPACE, (
                "The input 'choice.action_chosen.name': '%s', is neither '%s' "
                "nor '%s'." % (action, BlackjackAction.DRAW,
                               BlackjackAction.PASS))
