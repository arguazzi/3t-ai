#!/usr/bin/env python2

import numpy as np
import sys
import random

class TicTacToe:

    def __init__(self):
        self.board = np.array([[0,0,0], [0,0,0], [0,0,0]])

    def get_rowcol(self, n):
        row = n/3
        col = n%3
        return [row, col]

    def edit_board(self, n, s):
        if s not in [1, 4]:
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
            elif i==1:
                s+=' x '
            elif i==4:
                s+=' o '
            if count%3==0:
                s+=('\n')

        print s

    def check_wins(self):
        a = self.board
        trace = np.sum(np.diag(a))
        antitrace = np.sum(np.diag(np.flipud(a)))
        all_sums = np.concatenate((np.sum(a, 0),np.sum(a, 1), [trace], [antitrace]))
        print "Product is: "+str(np.prod(a))
        if 3 in all_sums:
            return 1
        elif 12 in all_sums:
            return -1
        elif np.prod(a)!=0:
            return -2
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

        ai = tAtIt(self.board)

        print "Welcome to tic-tac-toe. To play, enter a number for a position.\n"
        print "The array used has the folowing indexing:\n"
        print " 1  2  3 \n 4  5  6 \n 7  8  9\n"
        print "\nThe game begins!\n\n"

        self.draw_board()
        game_not_over = True
        while game_not_over:
            '''
            x = self.step("x")
            '''
            o = self.step("o")
            self.edit_board(o, 4)
            w = self.check_wins()
            self.draw_board()

            if np.abs(w) > 0:
                game_not_over = False
                break

            print "Turn for x: \n"
            ai.update_board(self.board)
            x = ai.move()
            self.edit_board(x, 1)
            w = self.check_wins()
            self.draw_board()

            if np.abs(w) > 0:
                game_not_over = False
                break

        if w == -2:
            print "Game over, draw."

        else:
            if w == 1:
                s = 'x'
            elif w==-1:
                s = 'o'
            print "Game over. The winner is " + s


class tAtIt:
    def __init__(self, board):
        self.board = board

    def compute_entry(self, r,c):
        return (r*3)+c

    def update_board(self, board):
        self.board = board

    def move(self):
        rsum = np.sum(self.board, 0)
        csum = np.sum(self.board, 1)
        diag = np.diag(self.board)
        adiag = np.diag(np.flipud(self.board))
        tsum = np.sum(diag)
        asum = np.sum(adiag)

        all = [rsum, csum, asum, tsum]

        # Blocking case
        if 8 in rsum:
            cx = np.where(rsum==8)[0]
            rx = np.where(self.board[:,cx].flatten()==0)[0]
            e = self.compute_entry(rx, cx)
            print self.board[:,cx].flatten()
            print "R Computing row: "+str(rx)+" col: "+str(cx)+" out:"+str(e)

        elif 8 in csum:
            rx = np.where(csum==8)[0]
            cx = np.where(self.board[rx,:].flatten()==0)[0]
            e = self.compute_entry(rx, cx)
            print self.board[rx,:].flatten()
            print "C Computing row: "+str(rx)+" col: "+str(cx)+" out:"+str(e)

        elif tsum==8:
            dx = np.where(diag==0)[0]
            e = self.compute_entry(dx, dx)

        elif asum==8:
            dx = np.where(adiag==0)[0]
            if dx == 0:
                e = self.compute_entry(2,0)
            elif dx==1:
                e = self.compute_entry(1,1)
            elif dx==2:
                e = self.compute_entry(0,2)

        else:
            while True:
                ix = [random.randint(0,2), random.randint(0,2)]
                if self.board[ix[0]][ix[1]] == 0:
                    break
            e = self.compute_entry(ix[0], ix[1])

        return int(e)
