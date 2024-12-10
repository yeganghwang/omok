from board import board
from iot_6789_student import iot_6789_student
from player import player
from stone import stone
from iot_12345_student import iot_12345_student
import time

class omokgame:
    def __init__(self, sz):
        self.__size = sz
        self.__bd = board(self.__size)

        #self.__black = player(-1)
        self.__white = iot_12345_student(1)

        #self.__white = player(1)
        self.__black = iot_6789_student(-1)


        self.__turns = 0
        self.__next = -1  # Black: 시작 차례
        self.__draw = 0
        self.__winner = 0
        self.__bd.display()

    def __del__(self):
        pass

    def game_start(self):
        while True:
            self.__turns += 1
            self.msg_display()

            if self.__next == -1:
                # Black turn
                print(" black Player: Turns = %5d" % self.__turns)
                time_b = 0
                time_delay = 0

                while True:
                    print(" black Player: time = %5d" % time_b)
                    start = time.time()
                    stn_b = self.__black.next(self.__bd.show(), self.__size)
                    end = time.time()
                    time_delay = end - start
                    time_b += 1
                    if (time_b >= 4) or (self.validCheck(stn_b) and (time_delay < 500)):
                        break

                if time_b < 4:
                    self.__bd.update(stn_b)
                else:
                    print("Too many wrong input or long time, black's turn is over")
                self.__next = self.__next * (-1)

            elif self.__next == 1:
                # White turn
                print(" white Player: Turns = %5d" % self.__turns)
                time_w = 0
                time_delay1 = 0

                while True:
                    print(" White Player: time = %5d" % time_w)
                    start1 = time.time()
                    stn_w = self.__white.next(self.__bd.show(), self.__size)
                    end1 = time.time()
                    time_delay1 = end1 - start1
                    time_w += 1
                    if (time_w >= 4) or (self.validCheck(stn_w) and (time_delay1 < 50)):
                        break

                if time_w < 4:
                    self.__bd.update(stn_w)
                else:
                    print("Too many wrong input or long time, white's turn is over")
                self.__next = self.__next * (-1)

            if self.endCheck():
                break

        self.__winner = self.__next * (-1)
        self.msg_display()

    def msg_display(self):
        if (self.__turns != 0 and self.__winner == 0):
            print("Turn ", self.__turns, ", ", end="")
            if self.__next == -1:
                print("Black")
            elif self.__next == 1:
                print("White")

        if self.__draw == 1:
            print("\n== No Winner : Game Result is draw ")
        elif self.__winner != 0:
            print("\nCongraturation!")
            print("The winner is ", end="")
            if self.__winner == -1:
                print("Black!!")
            elif self.__winner == 1:
                print("White!!")

    def endCheck(self):
        # horizontal omok
        for i in range(self.__size):
            for j in range(self.__size - 4):
                if self.__bd.get(i, j) != 0:
                    check = self.__bd.get(i, j) + self.__bd.get(i, j+1) + self.__bd.get(i, j+2) + self.__bd.get(i, j+3) + self.__bd.get(i, j+4)
                    if check == 5 * self.__bd.get(i, j):
                        return True

        # vertical omok
        for i in range(self.__size):
            for j in range(self.__size - 4):
                if self.__bd.get(j, i) != 0:
                    check = self.__bd.get(j, i) + self.__bd.get(j+1, i) + self.__bd.get(j+2, i) + self.__bd.get(j+3, i) + self.__bd.get(j+4, i)
                    if check == 5 * self.__bd.get(j, i):
                        return True

        # diagonal 1
        for i in range(self.__size - 4):
            for j in range(self.__size - 4):
                if self.__bd.get(i, j) != 0:
                    check = (self.__bd.get(i, j) + self.__bd.get(i+1, j+1) +
                             self.__bd.get(i+2, j+2) + self.__bd.get(i+3, j+3) + self.__bd.get(i+4, j+4))
                    if check == 5 * self.__bd.get(i, j):
                        return True

        # diagonal 2
        for i in range(self.__size - 4):
            for j in range(4, self.__size):
                if self.__bd.get(i, j) != 0:
                    check = (self.__bd.get(i, j) + self.__bd.get(i+1, j-1) +
                             self.__bd.get(i+2, j-2) + self.__bd.get(i+3, j-3) + self.__bd.get(i+4, j-4))
                    if check == 5 * self.__bd.get(i, j):
                        return True

        # draw check
        if self.drawCheck():
            return True

        return False

    def drawCheck(self):
        if self.__turns >= self.__size * self.__size - 2:
            self.__draw = 1
            return True
        else:
            self.__draw = 0
            return False

    def validCheck(self, stn):
        # overlapped check
        if self.__bd.get(stn.getX(), stn.getY()) != 0:
            return False
        return True
