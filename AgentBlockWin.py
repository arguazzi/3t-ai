from Agent import Agent
import numpy as np


class AgentBlockWin(Agent):
    def __init__(self):
        """
        Deterministic, one-move ahead player. Checks for wins or losses in the
        next move, and if none available chooses a random move.
        """
        super().__init__()

    def compute_entry(self, r, c):
        return (r * self.win_len) + c

    def check_move(self, board, val):
        """
        Check for sum totals in the columns, rows, and diagonals. For a next-
        move win, need to check for twice the value of the symbol (naught or
        cross). Also note that if the winning length is smaller than the board
        size, this is not performing an exhaustive search of the diagonals.
        """
        rsum = np.sum(board, 0)
        csum = np.sum(board, 1)
        diag = np.diag(board)
        adiag = np.diag(np.flipud(board))
        tsum = np.sum(diag)
        asum = np.sum(adiag)

        e = 0

        if val in rsum:
            cx = np.where(rsum == val)[0]
            rx = np.where(board[:, cx].flatten() == 0)[0]
            e = self.compute_entry(rx, cx)[0]

        elif val in csum:
            rx = np.where(csum == val)[0]
            cx = np.where(board[rx, :].flatten() == 0)[0]
            e = self.compute_entry(rx, cx)[0]

        elif tsum == val:
            dx = np.where(diag == 0)[0]
            e = self.compute_entry(dx, dx)[0]

        elif asum == val:
            dy = np.where(adiag == 0)[0]
            dx = len(board) - dy - 1
            e = self.compute_entry(dx, dy)[0]

        return e

    def move(self, board, positions):
        # Check for possible next-move wins - win by moving there
        e = self.check_move(board, self.pval * (self.win_len - 1))

        # Check for possible next-move losses - block by going there
        if e == 0:
            e = self.check_move(board, self.oval * (self.win_len - 1))

        # Randomly select for next move
        if e == 0:
            idx = np.random.choice(len(positions))
            e = positions[idx]

        return e