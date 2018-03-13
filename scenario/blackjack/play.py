from pprint import pprint

from rl.game import SequentialGame

from scenario.blackjack.blackjack_environment import BlackjackEnvironment
from scenario.blackjack.episode_serializer import EpisodeSerializer
from scenario.blackjack.agent import RandomPlayer

agent = RandomPlayer()
environment = BlackjackEnvironment()

num_of_games = 10
all_games_episodes = []

for _ in range(num_of_games):
    single_game_episodes = SequentialGame(agent, environment).run_once()
    all_games_episodes.append(single_game_episodes)

# Print
serializer = EpisodeSerializer()
for single_game_episodes in all_games_episodes:
    for episode in single_game_episodes:
        pprint(serializer.to_human_friendly_json(episode))
