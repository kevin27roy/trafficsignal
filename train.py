from sim.traffic_env import TrafficEnvironment
from agents.qlearning_agent import QLearningAgent

import pandas as pd
import pickle

env = TrafficEnvironment()

agent = QLearningAgent()

results = []

episodes = 200

for episode in range(episodes):

    state = env.reset()

    total_reward = 0

    for step in range(100):

        action = agent.choose_action(state)

        next_state, reward = env.step(action)

        agent.learn(state, action, reward, next_state)

        state = next_state

        total_reward += reward

    avg_reward = total_reward / 100

    avg_wait_time = -avg_reward

    results.append({
        "episode": episode,
        "average_reward": avg_reward,
        "avg_wait_time": avg_wait_time,
        "epsilon": agent.epsilon
    })

    print(f"Episode {episode} Reward: {avg_reward}")

df = pd.DataFrame(results)

df.to_csv("experiments/results_1.csv", index=False)

pickle.dump(
    agent.q_table,
    open("policies/policy_v1.pkl", "wb")
)

print("Training Complete")