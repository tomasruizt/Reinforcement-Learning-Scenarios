import os
from rl.game import SequentialGame

from scenario.blackjack.blackjack_environment import BlackjackEnvironment
from scenario.blackjack.episode_serializer import EpisodeSerializer
from scenario.blackjack.agent import RandomPlayer

from datasets.write import save_to_json_file

agent = RandomPlayer()
environment = BlackjackEnvironment()

num_of_games = 10
game = SequentialGame(agent, environment)
games_results = game.play_multiple_times(times=num_of_games)

serialized_episodes = []
for game_result in games_results:
    for episode in game_result.episodes:
        json = EpisodeSerializer(episode).to_human_friendly_json()
        serialized_episodes.append(json)

basedir = os.path.join("results", "blackjack")
save_to_json_file(serialized_episodes, basedir, overwrite=True)
