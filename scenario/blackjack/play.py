from pprint import pprint

from rl.game import SequentialGame

from scenario.blackjack.BlackjackEnvironment import BlackjackEnvironment
from scenario.blackjack.EpisodeSerializer import EpisodeSerializer
from scenario.blackjack.agent import RandomPlayer

agent = RandomPlayer()
environment = BlackjackEnvironment()
results = SequentialGame(agent, environment).run_once()
serializer = EpisodeSerializer()

for episode in results:
    pprint(serializer.to_json(episode))
