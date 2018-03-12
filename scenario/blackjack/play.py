from pprint import pprint

from rl.game import SequentialGame

from scenario.blackjack.blackjack_environment import BlackjackEnvironment
from scenario.blackjack.episode_serializer import EpisodeSerializer
from scenario.blackjack.agent import RandomPlayer

agent = RandomPlayer()
environment = BlackjackEnvironment()
results = SequentialGame(agent, environment).run_once()
serializer = EpisodeSerializer()

for episode in results:
    pprint(serializer.to_json(episode))
