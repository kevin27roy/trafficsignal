import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("experiments/results_1.csv")

plt.plot(df["episode"], df["average_reward"])

plt.xlabel("Episode")
plt.ylabel("Average Reward")
plt.title("Reward over Episodes")

plt.savefig("plots/reward_plot.png")

print("Plot Saved")