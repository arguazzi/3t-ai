#!/usr/bin/env python3

import numpy as np
from AgentHuman import AgentHuman
from AgentRandom import AgentRandom
from AgentBlockWin import AgentBlockWin
from AgentExploreQ import AgentExploreQ


class TicTacToe:

    def __init__(self, board_size=3, win_len=3):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size))
        self.available_positions = [i for i in range(0, board_size * board_size)]  # list of available empty places

        self.win_len = win_len
        self.naughts = win_len + 1  # representation of the naughts
        self.crosses = 1  # representation of the crosses
        self.blanks = 0  # representation of the empty states
        self.boardHash = None  # unique hash representation
        self.aio = None  # naughts player, plays first
        self.aix = None  # crosses player, plays second

    def reset_board(self):
        self.board = np.zeros((self.board_size, self.board_size))
        self.available_positions = [i for i in range(0, self.board_size * self.board_size)]  # list of available empty places

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

    def train(self, aio, aix, turns):
        for i in range(turns):
            self.play(aio, aix, gui_on=False)
        aio.save_policy()
        aix.save_policy()

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
            self.printer("Game over, draw."+"\n", gui_on)
            self.give_reward(w)
            return w
        else:
            if w == 1:
                s = 'x'
            elif w == -1:
                s = 'o'
            self.printer("Game over. The winner is " + s+"\n", gui_on)
            self.give_reward(w)
            return w

    def give_reward(self, w):
        if w == 1:
            self.aix.feed_reward(1.0)
            self.aio.feed_reward(0.0)
        elif w == -1:
            self.aio.feed_reward(1.0)
            self.aix.feed_reward(0.0)
        else:
            self.aio.feed_reward(0.5)
            self.aix.feed_reward(0.5)


class Game:

    def __init__(self):
        self.debut_str = "If you want to: " \
                    "\n-train the RL-AI [1], " \
                    "\n-play RL-AI vs Markov-AI [2], " \
                    "\n-play RL-AI vs RL-AI [3], " \
                    "\n-play RL-AI vs Human [4], " \
                    "\n-play Human vs Human [5], " \
                    "\n-exit [0]\n"
        self.debut_possibilities = [1, 2, 3, 4, 5, 0]
        self.max_training = 100000

    def intro(self):
        while True:
            debut_choice = int(input(self.debut_str))
            if debut_choice in self.debut_possibilities:
                return debut_choice
            else:
                print("Move not available.\n")

    def training_len(self):
        text = 'How many turns should it train for?\n'
        choice = int(input(text))
        if (choice>0) and (choice<self.max_training):
            return choice
        else:
            print("Please enter a positive number up to "+str(self.max_training)+"\n")

    def rl_ai_position(self):
        text = 'RL-AI as player 1 [1] or 2 [2]?\n'
        choice = int(input(text))
        if (choice == 1) or (choice == 2):
            return choice
        else:
            print("Please input a number 1 or 2\n")

    def end_game(self):
        text = 'The game is over. Exit [1] or go back to main menu [2].\n'
        choice = int(input(text))
        if (choice == 1) or (choice == 2):
            return choice
        else:
            print("Please input a number 1 or 2")

    def run(self):
        while True:
            aio = None
            aix = None
            choice = self.intro()

            if choice == 1:
                train_len = self.training_len()
                tictactoe = TicTacToe(board_size=3, win_len=3)
                aio = AgentExploreQ(policy_file="policy_o", train_prefix='vanilla')
                aix = AgentExploreQ(policy_file="policy_x", train_prefix='vanilla')
                tictactoe.train(aio=aio, aix=aix, turns=train_len)

            elif choice == 2:
                rl_ai_pos = self.rl_ai_position()
                if rl_ai_pos == 1:
                    aio = AgentExploreQ(policy_file="policy_o", train_prefix='vanilla')
                    aix = AgentBlockWin()
                elif rl_ai_pos == 2:
                    aio = AgentBlockWin()
                    aix = AgentExploreQ(policy_file="policy_x", train_prefix='vanilla')
                tictactoe = TicTacToe(board_size=3, win_len=3)
                _ = tictactoe.play(aio=aio, aix=aix, gui_on=True)

            elif choice == 3:
                tictactoe = TicTacToe(board_size=3, win_len=3)
                aio = AgentExploreQ(policy_file="policy_o", train_prefix='vanilla')
                aix = AgentExploreQ(policy_file="policy_x", train_prefix='vanilla')
                _ = tictactoe.play(aio=aio, aix=aix, gui_on=True)

            elif choice == 4:
                rl_ai_pos = self.rl_ai_position()
                if rl_ai_pos == 1:
                    aio = AgentExploreQ(policy_file="policy_o", train_prefix='vanilla')
                    aix = AgentHuman()
                elif rl_ai_pos == 2:
                    aio = AgentHuman()
                    aix = AgentExploreQ(policy_file="policy_x", train_prefix='vanilla')
                tictactoe = TicTacToe(board_size=3, win_len=3)
                _ = tictactoe.play(aio=aio, aix=aix, gui_on=True)

            elif choice == 5:
                tictactoe = TicTacToe(board_size=3, win_len=3)
                aio = AgentHuman()
                aix = AgentHuman()
                _ = tictactoe.play(aio=aio, aix=aix, gui_on=True)

            elif choice == 6:
                break

            choice = self.end_game()
            if choice == 1:
                break


if __name__ == '__main__':
    game = Game()
    game.run()
    print('OK. Bye then!')
