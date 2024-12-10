from board import board

class stone:
    def __init__(self, stn=None, sz=19):
        self.__size = sz
        if stn is None:
            self.__x = (self.__size - 1) // 2
            self.__y = (self.__size - 1) // 2
            self.__bw = 0
        else:
            self.__x = (self.__size - 1) // 2
            self.__y = (self.__size - 1) // 2
            self.__bw = stn

    def __del__(self):
        pass

    def set(self, posX, posY, stn):
        self.__x = posX % self.__size
        self.__y = posY % self.__size
        self.__bw = stn

    def setStone(self, stn):
        self.__bw = stn

    def setX(self, posX):
        self.__x = posX % self.__size

    def setY(self, posY):
        self.__y = posY % self.__size

    def get(self):
        ret = stone()
        ret.set(self.__x, self.__y, self.__bw)
        return ret

    def getStone(self):
        return self.__bw

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y
