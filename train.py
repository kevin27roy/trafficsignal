from sim.traffic_env import TrafficEnvironment
from agents.qlearning_agent import QLearningAgent

import pandas as pd
import pickle
import matplotlib.pyplot as plt
import os

# Create folders if they do not exist
os.makedirs("experiments", exist_ok=True)
os.makedirs("policies", exist_ok=True)
os.makedirs("plots", exist_ok=True)

# Initialize environment and agent
env = TrafficEnvironment()

agent = QLearningAgent()

results = []

queue_history = []

episodes = 200

steps_per_episode = 100

# Training Loop
for episode in range(episodes):

    state = env.reset()

    total_reward = 0

    total_queue = 0

    for step in range(steps_per_episode):

        # Choose action
        action = agent.choose_action(state)

        # Take action in environment
        next_state, reward = env.step(action)

        # Learn from experience
        agent.learn(state, action, reward, next_state)

        # Update state
        state = next_state

        # Store reward
        total_reward += reward

        # Track queue length
        current_queue = sum(env.queues)

        total_queue += current_queue

        queue_history.append(current_queue)

    # Metrics
    avg_reward = total_reward / steps_per_episode

    avg_wait_time = -avg_reward

    avg_queue_length = total_queue / steps_per_episode

    # Save results
    results.append({
        "episode": episode,
        "average_reward": avg_reward,
        "avg_wait_time": avg_wait_time,
        "avg_queue_length": avg_queue_length,
        "epsilon": agent.epsilon,
        "learning_rate": agent.alpha,
        "gamma": agent.gamma
    })

    print(
        f"Episode {episode} | "
        f"Reward: {avg_reward:.2f} | "
        f"Wait: {avg_wait_time:.2f} | "
        f"Queue: {avg_queue_length:.2f} | "
        f"Epsilon: {agent.epsilon:.3f}"
    )

# Save experiment results
df = pd.DataFrame(results)

df.to_csv("experiments/results_1.csv", index=False)

# Save policies
pickle.dump(
    agent.q_table,
    open("policies/policy_v1.pkl", "wb")
)

pickle.dump(
    agent.q_table,
    open("policies/policy_v2_explored.pkl", "wb")
)

# -----------------------------
# Reward Plot
# -----------------------------

plt.figure(figsize=(10, 5))

plt.plot(df["episode"], df["average_reward"])

plt.xlabel("Episode")

plt.ylabel("Average Reward")

plt.title("Reward over Episodes")

plt.grid(True)

plt.savefig("plots/reward_plot.png")

plt.close()

# -----------------------------
# Queue Length Plot
# -----------------------------

plt.figure(figsize=(10, 5))

plt.plot(queue_history)

plt.xlabel("Time Step")

plt.ylabel("Queue Length")

plt.title("Queue Length over Time")

plt.grid(True)

plt.savefig("plots/queue_plot.png")

plt.close()

# -----------------------------
# Waiting Time Plot
# -----------------------------

plt.figure(figsize=(10, 5))

plt.plot(df["episode"], df["avg_wait_time"])

plt.xlabel("Episode")

plt.ylabel("Average Waiting Time")

plt.title("Average Waiting Time over Episodes")

plt.grid(True)

plt.savefig("plots/wait_time_plot.png")

plt.close()

print("\nTraining Complete")

print("Results saved to experiments/results_1.csv")

print("Policies saved in policies/")

print("Plots saved in plots/")