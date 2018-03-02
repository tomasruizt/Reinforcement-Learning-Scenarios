import argparse

import os
from rl.estimator.TDLambda import TDLambda
from rl.policy.UCB import UCB

from scenario.tenTimesTen.rewardFunctions.LinearFunctions import plane, noise
from scenario.tenTimesTen.TenTimesTenEnvironment import TenTimesTenEnvironment
from scenario.tenTimesTen.GameSimulator import simulate
from scenario.tenTimesTen.dump_results import dump_results
from scenario.tenTimesTen.agent.ModularAgent import ModularAgent


def run_experiment(results_folder=os.path.join(os.getcwd(), "results")):
    runs, iterations_per_run = 50, 200
    env = TenTimesTenEnvironment(reward_function=noise(plane(inclination=5, final_reward=100)))
    # agent = ModularAgent(
    #     estimator=MonteCarlo(),
    #     value_update_rate="per_game",
    #     policy=EpsilonGreedy(exploration_rate=step_function(200*120))
    # )
    agent2 = ModularAgent(
        estimator=TDLambda(),
        value_update_rate="per_step",
        policy=UCB(),
    )
    results, information = simulate(
        agent=agent2, environment=env, runs=runs, iterations_per_run=iterations_per_run)
    columns = ["REWARD", "STATE", "ACTION", "ESTIMATE"]
    folder_generated = dump_results(results, information, results_folder, columns)
    return folder_generated


run_experiment()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    args = parser.parse_args()
    directory = args.directory

    run_experiment(directory)
