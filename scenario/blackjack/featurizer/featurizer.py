import numpy as np

from rl.action import DiscreteActionFeatures
from rl.featurizer.featurizer import DiscreteFeaturizer

from scenario.blackjack.action import BlackjackAction
from scenario.blackjack.state import BlackjackState


class BlackjackFeaturizer(DiscreteFeaturizer):
    """
    Simple featurizer that looks only at the player's hand score. Since
    the score where the agent would take any decision ranges from 4 to
    21, this Featurizer will normalize transform that range to [0,1]

    It encodes the the two actions in a one-hot encoding, to the
    Regressor can learn to tell the actions apart.
    """

    def __init__(self):
        self._action_one_hot_encoding = {
            BlackjackAction.DRAW: 0,
            BlackjackAction.PASS: 1
        }

    def featurize(self, state: BlackjackState) -> DiscreteActionFeatures:
        assert state is not None, "Input should not be None."
        features = []
        player_score = self._normalize_max_min(state.player_hand.score)
        for action in state.action_space:
            action_encoding = self._action_one_hot_encoding[action]
            features.append([player_score, action_encoding])
        return DiscreteActionFeatures(state.action_space, np.array(features))

    @staticmethod
    def _normalize_max_min(x):
        max_val = 21
        min_val = 4
        return (x-min_val) / (max_val-min_val)
