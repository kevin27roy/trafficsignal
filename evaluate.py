import pandas as pd
import matplotlib.pyplot as plt

# Load RL results
df = pd.read_csv("experiments/results_1.csv")

# RL metrics
rl_reward = df["average_reward"].mean()

rl_wait = df["avg_wait_time"].mean()

# Fixed baseline result
fixed_wait = 26.39

# Comparison table
comparison = pd.DataFrame({
    "Method": ["Fixed Timer", "RL Policy"],
    "Average Waiting Time": [fixed_wait, rl_wait]
})

print(comparison)

# Plot comparison
plt.figure(figsize=(8,5))

plt.bar(
    comparison["Method"],
    comparison["Average Waiting Time"]
)

plt.ylabel("Average Waiting Time")

plt.title("Fixed Timer vs RL Policy")

plt.grid(True)

plt.savefig("plots/comparison_plot.png")

plt.show()

print("Comparison plot saved.")