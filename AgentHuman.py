from Agent import Agent


class AgentHuman(Agent):

    def __init__(self):
        Agent.__init__(self)

    def move(self, board, positions):
        while True:
            action = int(input("Input your move: "))
            if action in positions:
                return action
            else:
                print("Move not available.\n")