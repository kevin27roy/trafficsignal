import random

class TrafficEnvironment:

    def __init__(self):
        self.reset()

    def reset(self):

        self.queues = [0, 0, 0, 0]

        self.phase = 0

        return self.get_state()

    def get_state(self):

        return tuple(self.queues + [self.phase])

    def step(self, action):

        self.phase = action

        for i in range(4):
            self.queues[i] += random.randint(0, 2)

        if action == 0:

            self.queues[0] = max(0, self.queues[0] - 2)
            self.queues[1] = max(0, self.queues[1] - 2)

        else:

            self.queues[2] = max(0, self.queues[2] - 2)
            self.queues[3] = max(0, self.queues[3] - 2)

        reward = -sum(self.queues)

        next_state = self.get_state()

        return next_state, reward