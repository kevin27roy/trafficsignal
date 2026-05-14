import random
import numpy as np

class QLearningAgent:

    def __init__(self):

        self.q_table = {}

        self.alpha = 0.1
        self.gamma = 0.9

        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.min_epsilon = 0.1

    def get_q_values(self, state):

        if state not in self.q_table:
            self.q_table[state] = np.zeros(2)

        return self.q_table[state]

    def choose_action(self, state):

        if random.uniform(0,1) < self.epsilon:
            return random.randint(0,1)

        return np.argmax(self.get_q_values(state))

    def learn(self, state, action, reward, next_state):

        q_values = self.get_q_values(state)

        next_q_values = self.get_q_values(next_state)

        q_values[action] += self.alpha * (
            reward
            + self.gamma * np.max(next_q_values)
            - q_values[action]
        )

        self.epsilon = max(
            self.min_epsilon,
            self.epsilon * self.epsilon_decay
        )