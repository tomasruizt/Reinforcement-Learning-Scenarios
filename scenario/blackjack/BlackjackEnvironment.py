from collections import Counter

from rl.action import DiscreteAction
from rl.agent_choice import DiscreteAgentChoice
from rl.environment import DiscreteEnvironment
from rl.episode import DiscreteEpisode
from rl.state import DiscreteState

from scenario.blackjack.state_representation import BlackjackStateRepresentation
from scenario.blackjack.state_representation import BlackjackStateRepresentationBuilder as RepresentationBuilder
from scenario.blackjack.Card import Card
from scenario.blackjack.PokerCardsDeck import PokerCardsDeck


class BlackjackEnvironment(DiscreteEnvironment):
    """
    An implementation of Environment that simulates the BlackJack game.
    """

    PASS = "pass"
    _DRAW = "draw"
    _ACTION_SPACE = (DiscreteAction(_DRAW), DiscreteAction(PASS))
    _DEFAULT_BET = 1

    def __init__(self, shuffled_deck=PokerCardsDeck()):
        """
        Initializes the Blackjack environment with input deck
        :param shuffled_deck: The deck to draw cards from.
        """
        self._shuffled_deck = shuffled_deck

    def get_initial_state(self) -> DiscreteState:
        """
        Returns an initial state formed by drawing two cards from the deck.
        :return: The initial state.
        """
        player_two_cards = [self._shuffled_deck.draw_card(), self._shuffled_deck.draw_card()]
        dealer_cards = [self._shuffled_deck.draw_card()]
        state_representation = BlackjackStateRepresentation(
            player_cards=Counter(player_two_cards),
            opponent_cards=Counter(dealer_cards),
            current_bet=self._DEFAULT_BET,
            passed=False
        )
        return DiscreteState(state_representation, self._ACTION_SPACE)

    def is_state_final(self, state: DiscreteState) -> bool:
        """
        Evaluates whether the input state qualifies as a final state. Final states are those whose cards values are
        over 21, as well as those where the Agent has decided to pass.
        :param state: The state to determine whether its final.
        :return: True if the state is a final one.
        """
        return state.representation.passed or self._cards_value_over_21(state.representation)

    def evaluate_agent_choice(self, agent_choice: DiscreteAgentChoice) -> DiscreteEpisode:
        new_state = self._get_new_state_from(agent_choice)
        return DiscreteEpisode(
            start_state=agent_choice.from_state,
            action_chosen=agent_choice.action_chosen,
            reward=None,        # The reward is many times dependent on what the dealer plays.
            end_state=new_state
        )

    # PRIVATE FUNCTIONS

    @staticmethod
    def _cards_value_over_21(representation: BlackjackStateRepresentation) -> bool:
        cards_value = 0
        for card, quantity in representation.player_cards.items():
            cards_value += min(card.possible_values) * quantity
        return cards_value > 21

    def _get_new_state_from(self, choice: DiscreteAgentChoice):
        """
        Takes the initial state in the input choice and uses the taken action to transition to a new state.
        :param choice: The choice that describes from what state what action the Agent chose.
        :return: The new state.
        """
        action_name = choice.action_chosen.name
        old_state_representation = choice.from_state.representation
        if action_name is self._DRAW:
            new_card = self._shuffled_deck.draw_card()
            new_state_representation = RepresentationBuilder.from_old_state_plus_new_card(
                old_state_representation, new_card)
        elif action_name is self.PASS:
            new_state_representation = RepresentationBuilder.from_old_state_with_action_pass(old_state_representation)
        else:
            raise ValueError("The input 'choice.action_chosen.name': '%s', is neither '%s' nor '%s'." % (
                action_name, self._DRAW, self.PASS))
        return DiscreteState(new_state_representation, self._ACTION_SPACE)

