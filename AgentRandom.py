from Agent import Agent
import numpy as np


class AgentRandom(Agent):
    def __init__(self):
        Agent.__init__(self)

    def move(self, board, positions):
        idx = np.random.choice(len(positions))
        e = positions[idx]
        return e