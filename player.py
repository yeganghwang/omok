from stone import stone

class player:
    def __init__(self, clr):
        self._color = clr

    def __del__(self):
        pass

    def next(self, board, length):
        print(" **** Human player : My Turns **** ")
        stn = stone(self._color, length)
        pos = int(input("Input position x for new stone : "))
        while pos < 0 or pos >= length:
            pos = int(input("Wrong position, please input again : "))
        stn.setX(pos)

        pos = int(input("Input position y for new stone : "))
        while pos < 0 or pos >= length:
            pos = int(input("Wrong position, please input again : "))
        stn.setY(pos)

        print(" === Human player was completed ==== ")
        return stn
