import random

class Dice:
    def __init__(self):
        self.__last__ = []

    def roll(self):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        if d1 == d2:
            # Si los dados son iguales, se multiplica x2 y podes mover hasta 4 fichas
            self.__last__ = [d1, d1, d1, d1]
        else:
            self.__last__ = [d1, d2]
        return list(self.__last__)

    def last(self):
        return list(self.__last__)
