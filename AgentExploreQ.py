from Agent import Agent
import numpy as np
import pickle


class AgentExploreQ(Agent):

    def __init__(self, policy_file=None, train_prefix=None, exp_rate=0.3, learning_rate=0.9, decay_gamma=0.95):
        Agent.__init__(self)
        self.states = []
        self.exp_rate = exp_rate
        self.lr = learning_rate
        self.decay_gamma = decay_gamma
        self.states_value = {}
        self.train_prefix = train_prefix

        if policy_file is not None:
            self.load_policy(policy_file)

    def add_state(self, state):
        self.states.append(state)

    def reset_state(self):
        self.states = []

    def get_hash(self, board):
        boardHash = str(board.flatten())
        return boardHash

    def move(self, board, positions):
        """
        Choose whether to choose an action at random or from history based on
        exploitation rate. Store the hash of the board state in a state-value
        dictionary and choose the action that returns the maximum value of the
        next state.
        """
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -np.inf
            for p in positions:
                next_board = board.copy().flatten()
                next_board[p] = self.pval
                next_boardHash = self.get_hash(next_board)
                if self.states_value.get(next_boardHash) is None:
                    value = 0
                else:
                    value = self.states_value.get(next_boardHash)
                if value >= value_max:
                    value_max = value
                    action = p
        return action

    def feed_reward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0.0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]
        self.reset_state()

    def save_policy(self):
        name = 'policy_' + self.train_prefix + '_' + str(self.player)
        fw = open(name, 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def load_policy(self, filename):
        try:
            fr = open(filename, 'rb')
            self.states_value = pickle.load(fr)
            fr.close()
        except IOError:
            print("File not available. Starting from the beginning.")