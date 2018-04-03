from rl.agent import DiscreteAgent
from rl.agent_choice import DiscreteAgentChoice
from rl.experience_tuple import ExperienceTuple

from scenario.blackjack.action import BlackjackAction
from scenario.blackjack.state import BlackjackState


class Dealer(DiscreteAgent):
    """The dealer in the Blackjack game."""

    def choose_action(self, state: BlackjackState) -> DiscreteAgentChoice:
        """
        The dealer goes last in the game, so he has a simple decision to take:
        In case the opponent's cards are greater than 21, pass. Else, if the
        dealer has a lower score than the opponent, draw a card."""
        player_score = state.player_hand.score
        dealer_score = state.dealer_hand.score

        dealer_in_disadvantage = dealer_score < player_score <= 21

        action = (BlackjackAction.DRAW if dealer_in_disadvantage else
                  BlackjackAction.PASS)
        return DiscreteAgentChoice(
            from_state=state,
            action_chosen=action
        )

    def observe_experience_tuple(self, experience_tuple: ExperienceTuple):
        """The dealer learns nothing from experience"""
        pass
