import argparse
import time

import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

from scenario.tenTimesTen.ValueAnimation import load_matrices, load_results
from scenario.tenTimesTen.z_meshgrid_gen import z_meshgrid_gen


def visualize(folder):
    seconds_for_update = 0.5
    X, Y, Zs = load_matrices(folder, z_meshgrid_gen)
    dfs = load_results(folder)
    fig = plt.figure(figsize=(10, 7))
    ax = fig.gca(projection="3d")

    def update(i):
        time.sleep(seconds_for_update)
        ax.clear()
        surf = ax.plot_surface(
            X, Y, Zs[i], cmap=cm.coolwarm, linewidth=0, antialiased=False)
        run = dfs[i]
        x1s, x2s = zip(*run["STATE"].values)
        zs = [Zs[i][j, k] for k, j in zip(x1s, x2s)]
        ax.plot(x1s, x2s, zs, "--k")
        reward = dfs[i]["REWARD"].sum()
        ax.set_title("Iteration: " + str(i) + " Reward: " + str(reward))

    a = anim.FuncAnimation(fig, update, frames=len(Zs), repeat=True)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    args = parser.parse_args()
    folder = args.directory

    visualize(folder)

