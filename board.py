# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 11:04:16 2020
Maker : bychoi@deu.ac.kr
@author: Com
"""

from os import system, name
import copy

class board:
    def __init__(self, size=19):
        self.__size = size
        self.__game_board = [[0 for i in range(self.__size)] for j in range(self.__size)]

    def __del__(self):
        pass

    def update(self, st):
        x = st.getX()
        y = st.getY()
        stone = st.getStone()
        print(x, ",", y, ":", stone)
        self.__game_board[x][y] = stone
        self.display()

    def show(self):
        temp = copy.deepcopy(self.__game_board)
        return temp

    def get(self, x, y):
        return self.__game_board[x][y]

    def display(self):
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

        print("{0:^3}".format(" "), end="")
        for i in range(self.__size):
            print("{0:^3}".format(i), end="")
        print()

        for i in range(self.__size-1, -1, -1):
            print("{0:^3}".format(i), end="")
            for j in range(self.__size):
                val = self.write_char(self.__game_board[i][j])
                print("{0:^3}".format(val), end="")
            print()

    def write_char(self, stn):
        if stn == 1:
            return 'X'
        elif stn == -1:
            return '●'
        elif stn == 0:
            return '.'
        else:
            return '.'
