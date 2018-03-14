import unittest

from scenario.blackjack.cards_deck import Hand, Card
from scenario.blackjack.featurizer import BlackjackFeaturizer
from scenario.blackjack.state import BlackjackState


class BlackjackFeaturizerTest(unittest.TestCase):

    featurizer = BlackjackFeaturizer()  # No need to reset
    IDX_OF_PLAYERS_SCORE = 0
    """The player's score will be located in the features vector's 
    first entry, because the class is coded that way."""
    IDX_OF_ACTION = 1

    def test_featurize_reject_None_input(self):
        with self.assertRaisesRegex(
                AssertionError, "Input should not be None."):
            self.featurizer.featurize(None)

    def test_featurize_hand_with_min_score(self):
        """
        The player has minimal score, so we expect the featurizer to
        put a 0 for the player's score in the features vector of every
        action.
        """
        min_score_state = self._init_min_score_state()
        expected_vector_entry = 0

        action_features_vectors = \
            self.featurizer.featurize(min_score_state).features
        for features_vector in action_features_vectors:  # Each of the two
            # actions has its features vector
            self.assertEqual(features_vector[self.IDX_OF_PLAYERS_SCORE],
                             expected_vector_entry)

    def test_featurize_hand_with_max_score(self):
        """
        The player has maximum score, so we expect the featurizer to
        put a 1 for the player's score in the features vector of every
        action.
        """
        max_score_state = self._init_max_score_state()
        expected_vector_entry = 1

        action_features_vectors = \
            self.featurizer.featurize(max_score_state).features
        for features_vector in action_features_vectors :
            self.assertEqual(features_vector[self.IDX_OF_PLAYERS_SCORE],
                             expected_vector_entry)

    def test_featurize_actions_are_one_hot_encoded(self):
        """
        The features vector for each action should differ in the
        entry that represents the one-hot encoded action.
        """
        any_state = self._init_min_score_state()
        action_features_vectors = self.featurizer.featurize(any_state).features

        first_action_encoding = action_features_vectors[0][self.IDX_OF_ACTION]
        second_action_encoding = action_features_vectors[1][self.IDX_OF_ACTION]
        """It doesnt matter whether the first action is pass or draw.
        It only matters that both action's encodings are different."""

        self.assertNotEqual(first_action_encoding, second_action_encoding)
        self.assertIn(first_action_encoding, [0, 1])
        self.assertIn(second_action_encoding, [0, 1])

    def test_featurize_action_space_gets_passed_on(self):
        any_state = self._init_min_score_state()
        expected_actions = any_state.action_space

        actual_actions = self.featurizer.featurize(any_state).actions
        self.assertEqual(expected_actions, actual_actions)

    @staticmethod
    def _init_min_score_state() -> BlackjackState:
        return BlackjackState.new_initial_state(
            player_hand=Hand([Card("2"), Card("2")]),
            dealer_hand=Hand([Card("2")])
        )

    @staticmethod
    def _init_max_score_state() -> BlackjackState:
        return BlackjackState.new_initial_state(
            player_hand=Hand([Card("A"), Card("K")]),
            dealer_hand=Hand([Card("2")])
        )
