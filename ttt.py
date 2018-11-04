#!/usr/bin/env python2

import numpy as np
import sys

class TicTacToe:

    def __init__(self):
        self.board = np.array([[0,0,0], [0,0,0], [0,0,0]])

    def get_rowcol(self, n):
        row = n/3
        col = n%3
        return [row, col]

    def edit_board(self, n, s):
        if s not in [1, -1]:
            return -1
        rc = self.get_rowcol(n)
        self.board[rc[0]][rc[1]] = s

    def draw_board(self):
        s = ''
        count = 0
        for i in self.board.flatten():
            count += 1
            if i==0:
                s+=' - '
            elif i<0:
                s+=' o '
            elif i>0:
                s+=' x '
            if count%3==0:
                s+=('\n')

        print s

    def check_wins(self):
        a = self.board
        trace = np.sum(np.diag(a))
        antitrace = np.sum(np.diag(np.flipud(a)))
        all_sums = np.concatenate((np.sum(a, 0),np.sum(a, 1), [trace], [antitrace]))
        if 3 in all_sums:
            return 1
        elif -3 in all_sums:
            return -1
        else:
            return 0

    def check_entry(self, n):
        is_check = True
        if (n<0) | (n>8):
            print "Outside of board!"
            is_check = False
            return is_check
        rc = self.get_rowcol(n)
        if self.board[rc[0]][rc[1]] != 0:
            print "Position occupied!"
            is_check = False
            return is_check

    def step(self, s):
        is_check = False
        while is_check==False:
            var = raw_input("Turn for "+s+" - enter the position:\n")
            var = int(var)-1
            is_check = self.check_entry(var)
        return var

    def play(self):

        print "Welcome to tic-tac-toe. To play, enter a number for a position.\n"
        print "The array used has the folowing indexing:\n"
        print " 1  2  3 \n 4  5  6 \n 7  8  9\n"
        print "\nThe game begins!\n\n"

        self.draw_board()
        game_not_over = True
        while game_not_over:
            x = self.step("x")
            self.edit_board(x, 1)
            w = self.check_wins()
            self.draw_board()

            if np.abs(w) == 1:
                game_not_over = False
                break

            o = self.step("o")
            self.edit_board(o, -1)
            w = self.check_wins()
            self.draw_board()

            if np.abs(w) == 1:
                game_not_over = False
                break

        if w == 1:
            s = 'x'
        else:
            s = 'o'

        print "Game over. The winner is " + s
