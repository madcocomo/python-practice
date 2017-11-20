import time
import sys
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    def __str__(self):
        return '({},{})'.format(self.x, self.y)
    def __hash__(self):
        return hash(self.__str__())
    def adjoint(self, other):
        return other in self.getNeighbors()
    def getNeighbors(self):
        result = set()
        for xd in [-1, 0, 1]:
            for yd in [-1, 0, 1]:
                if not(xd==0 and yd==0):
                    result.add(Point(self.x+xd, self.y+yd))
        return result

class World:
    def __init__(self):
        self.__alives = set()
    def isAlive(self, point):
        return point in self.__alives
    def putLifeAt(self, point):
        self.__alives.add(point)
    def nextGen(self):
        newWorld = World()
        for point in filter (self.willBeAlive, self.mayChangeCells()):
            newWorld.putLifeAt(point)
        return newWorld
    def mayChangeCells(self):
        cells = set(self.__alives)
        for point in self.__alives:
            cells = cells | point.getNeighbors()
        return cells
    def willBeAlive(self, point):
        aroundNum = self.around(point)
        if aroundNum == 2: return self.isAlive(point)
        return aroundNum == 3
    def around(self, point):
        arounds = list(filter(point.adjoint, self.__alives))
        return len(arounds)
    def output(self, topLeft, bottomRight):
        result = ''
        for x in range(topLeft.x, bottomRight.x+1):
            result += '\n'
            for y in range(topLeft.y, bottomRight.y+1):
                result += 'O' if self.isAlive(Point(x,y)) else '.'
        return result

def output(world):
    print(chr(27) + '[2J')
    print(world.output(Point(0,0), Point(size,size)))

if __name__ == '__main__':
    size = 10
    world = World()
    for initLife in range(size*2):
        x = random.randint(0,size)
        y = random.randint(0,size)
        world.putLifeAt(Point(x,y))
    output(world)
    for i in range(30):
        time.sleep(1)
        world = world.nextGen()
        output(world)
