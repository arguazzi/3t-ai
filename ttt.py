#!/usr/bin/env python3

import numpy as np
import pickle


class TicTacToe:

    def __init__(self, board_size=3, win_len=3):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size))
        self.win_len = win_len
        self.naughts = win_len + 1  # representation of the naughts
        self.crosses = 1  # representation of the crosses
        self.blanks = 0  # representation of the empty states
        self.boardHash = None  # unique hash representation
        self.available_positions = [i for i in range(0, board_size * board_size)]  # list of available empty places
        self.aio = None  # naughts player, plays first
        self.aix = None  # crosses player, plays second

    def reset_board(self):
        self.board = np.zeros((self.board_size, self.board_size))

    def get_rowcol(self, n):
        row = n // self.board_size
        col = n % self.board_size
        return [row, col]

    def edit_board(self, n, s):
        if s not in [self.crosses, self.naughts]:
            return -1
        rc = self.get_rowcol(n)
        self.board[rc[0]][rc[1]] = s
        self.available_positions.remove(n)

    def draw_board(self, gui_on):
        if gui_on:
            s = ''
            count = 0
            for i in self.board.flatten():
                count += 1
                if i == self.blanks:
                    s += ' - '
                elif i == self.crosses:
                    s += ' x '
                elif i == self.naughts:
                    s += ' o '
                if count % self.board_size == 0:
                    s += ('\n')
            print(s)

    def check_wins(self):
        """
        Check diagonals and horizontal and vertical sums for wins. If the whole
        board is occupied - it's a draw.
        """
        trace = np.sum(np.diag(self.board))
        antitrace = np.sum(np.diag(np.flipud(self.board)))
        all_sums = np.concatenate((np.sum(self.board, 0), np.sum(self.board, 1), [trace], [antitrace]))
        if self.crosses * self.win_len in all_sums:
            return 1
        elif self.naughts * self.win_len in all_sums:
            return -1
        elif np.prod(self.board) != 0:
            return -2
        else:
            return 0

    def check_entry(self, n):
        is_check = True
        if (n < 0) | (n > (self.board_size * self.board_size - 1)):
            print("Outside of board!")
            is_check = False
            return is_check
        if n not in self.available_positions:
            print("Position occupied!")
            is_check = False
            return is_check

    def human_step(self, s):
        is_check = False
        while is_check == False:
            var = input("Turn for " + s + " - enter the position:\n")
            var = int(var) - 1
            is_check = self.check_entry(var)
        return var

    def get_hash(self):
        self.boardHash = str(self.board.flatten())
        return self.boardHash

    def printer(self, text, gui_on):
        if gui_on:
            print(text)

    def play(self, aio, aix, gui_on=True):

        self.reset_board()

        self.aio = aio
        self.aix = aix
        self.aio.set_player('o', pval=self.naughts, oval=self.crosses, win_len=self.win_len)
        self.aix.set_player('x', pval=self.crosses, oval=self.naughts, win_len=self.win_len)

        if gui_on:
            print("Welcome to tic-tac-toe. To play, enter a number for a position.\n")
            print("The array used has the folowing indexing:\n")
            element = 0
            array_str = ''
            for i in range(self.board_size):
                for j in range(self.board_size):
                    array_str += ' ' + str(element)
                    element += 1
                print(array_str + '\n')
                array_str = ''
            print("\nThe game begins!\n\n")

        self.draw_board(gui_on)

        while True:
            self.printer("Turn for AI o: \n", gui_on)
            move_o = self.aio.move(self.board, self.available_positions)
            self.edit_board(move_o, self.naughts)
            board_hash = self.get_hash()
            self.aio.add_state(board_hash)
            w = self.check_wins()
            self.draw_board(gui_on)

            if np.abs(w) > 0:
                break

            self.printer("Turn for AI x: \n", gui_on)
            move_x = self.aix.move(self.board, self.available_positions)
            self.edit_board(move_x, self.crosses)
            board_hash = self.get_hash()
            self.aix.add_state(board_hash)
            w = self.check_wins()
            self.draw_board(gui_on)

            if np.abs(w) > 0:
                break

        if w == -2:
            self.printer("Game over, draw.", gui_on)
            self.give_reward(w)
        else:
            if w == 1:
                s = 'x'
            elif w == -1:
                s = 'o'
            self.printer("Game over. The winner is " + s, gui_on)
            self.give_reward(w)

    def give_reward(self, w):
        if w == 1:
            self.aix.feed_reward(1)
            self.aio.feed_reward(0)
        elif w == -1:
            self.aio.feed_reward(1)
            self.aix.feed_reward(0)
        else:
            self.aio.feed_reward(0.1)
            self.aix.feed_reward(0.5)


class Human:

    def __init__(self):
        self.player = None

    def set_player(self, player, pval, oval, win_len):
        self.player = player

    def move(self, board, positions):
        while True:
            action = int(input("Input your move: "))
            if action in positions:
                return action
            else:
                print("Move not available.")

    def feed_reward(self, reward):
        pass

    def add_state(self, state):
        pass

    def reset(self):
        pass


class RLttt:

    def __init__(self, exp_rate=0.3, learning_rate=0.2, decay_gamma=0.9):
        self.player = None
        self.pval = None
        self.oval = None
        self.states = []
        self.exp_rate = exp_rate
        self.lr = learning_rate
        self.decay_gamma = decay_gamma
        self.states_value = {}

    def set_player(self, player, pval, oval, win_len):
        self.player = player
        self.pval = pval
        self.oval = oval
        self.win_len = win_len

    def add_state(self, state):
        self.states.append(state)

    def reset_state(self):
        self.states = []

    @staticmethod
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
            value_max = -999
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
                self.states_value[st] = 0
                self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
                reward = self.states_value[st]

    def save_policy(self):
        name = 'policy_' + str(self.player)
        fw = open(name, 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def load_policy(self, filename):
        fr = open(filename, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()


class tAtIt:
    def __init__(self):
        """
        Deterministic, one-move ahead player. Checks for wins or losses in the
        next move, and if none available chooses a random move.
        """
        self.player = None
        self.pval = None
        self.oval = None
        self.win_len = None

    def set_player(self, player, pval, oval, win_len):
        self.player = player
        self.pval = pval
        self.oval = oval
        self.win_len = win_len

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

    def feed_reward(self, reward):
        pass

    def add_state(self, state):
        pass

    def reset(self):
        pass


if __name__ == '__main__':
    tictactoe = TicTacToe(board_size=3, win_len=3)
    aix = tAtIt()
    aio = tAtIt()
    tictactoe.play(aio=aio, aix=aix, gui_on=False)