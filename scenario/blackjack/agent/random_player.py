import random

from rl.agent import DiscreteAgent
from rl.agent_choice import DiscreteAgentChoice
from rl.experience_tuple import ExperienceTuple
from rl.state import DiscreteState

from scenario.blackjack.action import BlackjackAction


class RandomPlayer(DiscreteAgent):
    """
    This player has a specific probability to select to draw a card.
    That draw probability is a parameter.
    """

    def __init__(self, draw_probability=0.5):
        """Initializes the player with the draw probability as a
        parameter."""
        self._draw_probability = draw_probability

    def choose_action(self, state: DiscreteState) -> DiscreteAgentChoice:
        """Chooses to draw a card with the set probability"""
        if random.random() < self._draw_probability:
            action = BlackjackAction.DRAW
        else:
            action = BlackjackAction.PASS
        return DiscreteAgentChoice(state, action)

    def observe_experience_tuple(self, experience_tuple: ExperienceTuple):
        """This player does not update his decision making."""
        pass
