import os

from scenario.blackjack.blackjack_environment import BlackjackEnvironment
from scenario.blackjack.experience_tuple_serializer import \
    HumanFriendlyBlackjackExperienceTupleSerializer
from scenario.blackjack.agent import RandomPlayer
from scenario.blackjack.experiment import Experiment

from scenario.blackjack.experiment_configuration import ExperimentConfiguration

basedir = os.path.join("results", "blackjack")
experience_tuple_serializer = HumanFriendlyBlackjackExperienceTupleSerializer()
configuration = ExperimentConfiguration(
    agent=RandomPlayer(),
    environment=BlackjackEnvironment(),
    num_of_episodes=10,
    results_directory=basedir,
    experience_tuple_serializer=experience_tuple_serializer
)

Experiment(configuration).run()


