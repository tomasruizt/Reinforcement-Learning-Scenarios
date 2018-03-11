from numpy.random.mtrand import choice
from rl.action import DiscreteAction
from rl.agent import DiscreteAgent
from rl.agent_choice import DiscreteAgentChoice
from rl.episode import DiscreteEpisode
from rl.state import DiscreteState


class RandomPlayer(DiscreteAgent):
    """
    This player decides between drawing a card or passing at random every time.
    """

    def __init__(self, draw_probability=0.5):
        self._probabilities = (draw_probability, 1 - draw_probability)

    def choose_action(self, state: DiscreteState) -> DiscreteAgentChoice:
        action_name = choice(state.action_space, p=self._probabilities).name
        return DiscreteAgentChoice(state, DiscreteAction(action_name))

    def observe_episode(self, episode: DiscreteEpisode):
        pass
