from datasets.write import save_to_json_file
from rl.episode import EpisodeSerializer
from rl.game import SequentialGame

from scenario.blackjack.experiment_configuration import ExperimentConfiguration


class Experiment:
    def __init__(self, configuration: ExperimentConfiguration):
        assert configuration is not None
        self._configuration = configuration
        self._played_episodes = []
        self._serialized_episodes = []

    def run(self):
        self._reset_episodes()
        self._play_episodes()
        self._serialize_episodes()
        self._save_episodes_to_disk()

    def _play_episodes(self):
        num_of_episodes = self._configuration.num_of_episodes
        game = self._init_game()
        self._played_episodes = game.play_multiple_episodes(num_of_episodes)

    def _serialize_episodes(self):
        experience_tuple_serializer = \
            self._configuration.experience_tuple_serializer
        serializer = EpisodeSerializer(experience_tuple_serializer)
        self._serialized_episodes = \
            [serializer.serialize(episode) for episode in self._played_episodes]

    def _save_episodes_to_disk(self):
        basedir = self._configuration.results_directory
        save_to_json_file(self._serialized_episodes, basedir)

    def _init_game(self):
        agent = self._configuration.agent
        environment = self._configuration.environment
        return SequentialGame(agent, environment)

    def _reset_episodes(self):
        self._played_episodes = []
        self._serialized_episodes = []
