from rl.agent import DiscreteAgent
from rl.agent_choice import DiscreteAgentChoice
from rl.episode import DiscreteEpisode
from rl.explorator import DiscreteExplorator
from rl.featurizer.featurizer import DiscreteFeaturizer
from rl.learning_algorithm import LearningAlgorithm
from rl.regressor import Regressor
from rl.state import DiscreteState


class LearningAgent(DiscreteAgent):
    """This agent learns from experience."""

    def __init__(self, featurizer: DiscreteFeaturizer, regressor: Regressor,
                 explorator: DiscreteExplorator,
                 learning_algorithm: LearningAlgorithm):
        self._featurizer = featurizer
        self._regressor = regressor
        self._explorator = explorator
        self._learning_algorithm = learning_algorithm

    def choose_action(self, state: DiscreteState) -> DiscreteAgentChoice:
        action_features = self._featurizer.featurize(state)
        action_scores = self._regressor.predict(action_features)
        action = self._explorator.choose_action(action_scores)
        return DiscreteAgentChoice(from_state=state, action_chosen=action)

    def observe_episode(self, episode: DiscreteEpisode):
        fitting_data_optional = self._learning_algorithm.observe(episode)
        if fitting_data_optional is not None:
            self._regressor.fit(fitting_data=fitting_data_optional)