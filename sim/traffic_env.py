import random


class TrafficEnvironment:

    def __init__(self):

        self.reset()

    # -----------------------------------
    # Reset Environment
    # -----------------------------------

    def reset(self):

        # North, South, East, West
        self.queues = [0, 0, 0, 0]

        # 0 = North-South
        # 1 = East-West
        self.phase = 0

        return self.get_state()

    # -----------------------------------
    # Current State
    # -----------------------------------

    def get_state(self):

        return (
            min(self.queues[0], 10),
            min(self.queues[1], 10),
            min(self.queues[2], 10),
            min(self.queues[3], 10),
            self.phase
        )

    # -----------------------------------
    # Environment Step
    # -----------------------------------

    def step(self, action):

        # Update signal phase
        self.phase = action

        # -----------------------------------
        # Vehicles leaving
        # -----------------------------------

        if action == 0:

            # North-South Green
            self.queues[0] = max(0, self.queues[0] - 3)
            self.queues[1] = max(0, self.queues[1] - 3)

        else:

            # East-West Green
            self.queues[2] = max(0, self.queues[2] - 3)
            self.queues[3] = max(0, self.queues[3] - 3)

        # -----------------------------------
        # Random incoming traffic
        # -----------------------------------

        for i in range(4):

            incoming = random.randint(0, 1)

            self.queues[i] += incoming

        # -----------------------------------
        # Prevent infinite growth
        # -----------------------------------

        for i in range(4):

            self.queues[i] = min(self.queues[i], 10)

        # -----------------------------------
        # Reward Engineering
        # -----------------------------------

        total_queue = sum(self.queues)

        north_south = (
            self.queues[0] +
            self.queues[1]
        )

        east_west = (
            self.queues[2] +
            self.queues[3]
        )

        imbalance = abs(
            north_south - east_west
        )

        # -----------------------------------
        # Base Reward
        # -----------------------------------

        reward = 30 - total_queue

        # -----------------------------------
        # Encourage fairness
        # -----------------------------------

        reward -= imbalance * 2

        # -----------------------------------
        # Bonus for low traffic
        # -----------------------------------

        if total_queue <= 8:

            reward += 15

        # -----------------------------------
        # Congestion penalty
        # -----------------------------------

        if total_queue >= 20:

            reward -= 25

        # -----------------------------------
        # Strong imbalance penalty
        # -----------------------------------

        if imbalance >= 8:

            reward -= 20

        next_state = self.get_state()

        return next_state, reward