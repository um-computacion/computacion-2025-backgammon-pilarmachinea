from Checker import Checker

class Board:
    def __init__(self):
        self.__points__ = [[] for _ in range(24)]
        self._setup()

    def _put(self, idx, color, n):
        for _ in range(n):
            self.__points__[idx].append(Checker(color))

    def _setup(self):
        
        self._put(23, 'B', 2)  
        self._put(12, 'B', 5)   
        self._put(7,  'B', 3)   
        self._put(5,  'B', 5)   
        
        self._put(0,  'N', 2)   
        self._put(11, 'N', 5)   
        self._put(16, 'N', 3)   
        self._put(18, 'N', 5)   

    def point_owner_count(self, idx):
        stack = self.__points__[idx]
        if not stack:
            return None, 0
        return stack[0].color(), len(stack)

    def points(self):
        return self.__points_