from Agent import Agent
import numpy as np


class AgentRandom(Agent):
    def __init__(self):
        super().__init__()

    def move(self, board, positions):
        idx = np.random.choice(len(positions))
        e = positions[idx]
        return e