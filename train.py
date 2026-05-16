import numpy as np
import pandas as pd
import pickle
import os

from sim.traffic_env import TrafficEnvironment


# -----------------------------------
# Environment
# -----------------------------------

env = TrafficEnvironment()

# -----------------------------------
# Q-Table
# -----------------------------------

q_table = {}

# -----------------------------------
# Hyperparameters
# -----------------------------------

episodes = 500

alpha = 0.1

gamma = 0.95

epsilon = 1.0

# -----------------------------------
# Metrics
# -----------------------------------

reward_history = []

waiting_history = []

# -----------------------------------
# Create folders
# -----------------------------------

os.makedirs(
    "policies",
    exist_ok=True
)

os.makedirs(
    "experiments",
    exist_ok=True
)

# -----------------------------------
# Training Loop
# -----------------------------------

for episode in range(episodes):

    state = env.reset()

    total_reward = 0

    total_waiting = 0

    for step in range(50):

        # -----------------------------------
        # Initialize state
        # -----------------------------------

        if state not in q_table:

            q_table[state] = np.zeros(2)

        # -----------------------------------
        # Epsilon-Greedy
        # -----------------------------------

        if np.random.random() < epsilon:

            action = np.random.randint(0, 2)

        else:

            action = np.argmax(
                q_table[state]
            )

        # -----------------------------------
        # Environment Step
        # -----------------------------------

        next_state, reward = env.step(action)

        total_reward += reward

        total_waiting += sum(env.queues)

        # -----------------------------------
        # Initialize next state
        # -----------------------------------

        if next_state not in q_table:

            q_table[next_state] = np.zeros(2)

        # -----------------------------------
        # Q-Learning Update
        # -----------------------------------

        old_value = q_table[state][action]

        next_max = np.max(
            q_table[next_state]
        )

        new_value = old_value + alpha * (
            reward +
            gamma * next_max -
            old_value
        )

        q_table[state][action] = new_value

        state = next_state

    # -----------------------------------
    # Decay Exploration
    # -----------------------------------

    epsilon = max(
        0.01,
        epsilon * 0.995
    )

    # -----------------------------------
    # Metrics
    # -----------------------------------

    avg_waiting = total_waiting / 50

    reward_history.append(
        total_reward
    )

    waiting_history.append(
        avg_waiting
    )

    # -----------------------------------
    # Progress
    # -----------------------------------

    print(
        f"Episode {episode+1} | "
        f"Reward: {total_reward:.2f} | "
        f"Waiting: {avg_waiting:.2f} | "
        f"Epsilon: {epsilon:.3f}"
    )

# -----------------------------------
# Save Policy
# -----------------------------------

pickle.dump(
    q_table,
    open(
        "policies/policy_v1.pkl",
        "wb"
    )
)

# -----------------------------------
# Save Results
# -----------------------------------

results = pd.DataFrame({

    "episode": list(
        range(1, episodes + 1)
    ),

    "reward": reward_history,

    "avg_waiting_time":
        waiting_history
})

results.to_csv(

    "experiments/results_1.csv",

    index=False
)

print("\nTraining Complete.")

print(
    "Policy saved to "
    "policies/policy_v1.pkl"
)

print(
    "Results saved to "
    "experiments/results_1.csv"
)