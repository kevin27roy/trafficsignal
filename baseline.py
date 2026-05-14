from sim.traffic_env import TrafficEnvironment

env = TrafficEnvironment()

total_reward = 0

state = env.reset()

for step in range(100):

    if (step // 10) % 2 == 0:
        action = 0
    else:
        action = 1

    next_state, reward = env.step(action)

    total_reward += reward

avg_reward = total_reward / 100

avg_wait_time = -avg_reward

print("Fixed Timer Results")
print("Average Reward:", avg_reward)
print("Average Waiting Time:", avg_wait_time)