class Agent:

    def __init__(self):
        self.player = None
        self.pval = None
        self.oval = None
        self.win_len = None

    def set_player(self, player, pval, oval, win_len):
        self.player = player
        self.pval = pval
        self.oval = oval
        self.win_len = win_len

    def move(self, board, positions):
        pass

    def add_state(self, state):
        pass

    def feed_reward(self, reward):
        pass

    def save_policy(self):
        pass