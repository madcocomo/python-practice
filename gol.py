from curses import wrapper
import curses
from argparse import ArgumentParser
from collections import Counter
import time
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    def __str__(self):
        return '({},{})'.format(self.x, self.y)
    __repr__ = __str__
    def __hash__(self):
        return hash(self.__str__())
    def adjoint(self, other):
        return -1 <= other.x - self.x <= 1 \
            and -1 <= other.y -self.y <= 1 \
            and not(other.x == self.x and other.y == self.y)
    def getNeighbors(self):
        result = []
        for xd in [-1, 0, 1]:
            for yd in [-1, 0, 1]:
                if not(xd==0 and yd==0):
                    result.append(Point(self.x+xd, self.y+yd))
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
        for point, count in self.countNeighbors():
            if self.willBeAlive(point, count):
                newWorld.putLifeAt(point)
        return newWorld
    def countNeighbors(self):
        counts = Counter()
        for cell in self.__alives:
            for neighbor in cell.getNeighbors():
                counts[neighbor] += 1
        return counts.items()
    def mayChangeCells(self):
        cells = set(self.__alives)
        for point in self.__alives:
            cells = cells | set(point.getNeighbors())
        return cells
    def willBeAlive(self, point, neighborsCount):
        if neighborsCount == 2: return self.isAlive(point)
        return neighborsCount == 3
    def output(self, topLeft, bottomRight):
        result = ''
        for x in range(topLeft.x, bottomRight.x+1):
            result += '\n'
            for y in range(topLeft.y, bottomRight.y+1):
                result += 'O' if self.isAlive(Point(x,y)) else '_'
        return result

class Screen:
    def runInContext(self, fun):
        self.fun = fun
        wrapper(self.__run)
    def __run(self, stdscr):
        self.stdscr = stdscr
        stdscr.clear()
        self.__initViewSize()
        self.fun(self)
    def __initViewSize(self):
        self.leftTop = Point(0,0)
        bottom = min(curses.LINES-2, size)
        right = min(curses.COLS-2, size)
        self.bottomRight = Point(bottom, right)
    def trigger(self):
        self.stdscr.getkey()
    def show(self, world):
        self.stdscr.addstr(0, 0, world.output(self.leftTop, self.bottomRight))
        self.stdscr.refresh()
        return world

class Print:
    def runInContext(self, fun):
        fun(self)
    def trigger(self):
        a = input('press enter to next generation...')
    def show(self, world):
        print( world.output(Point(0,0), Point(size,size)))
        return world

def initWorld():
    world = World()
    for initLife in range(size * int(args.density)):
        x = random.randint(0,size)
        y = random.randint(0,size)
        world.putLifeAt(Point(x,y))
    return world

def run(output):
    world = output.show(initWorld())
    i = 0
    while i != args.times:
        i += 1
        output.trigger()
        world = output.show(world.nextGen())

def definArgs():
    parser = ArgumentParser()
    parser.add_argument('-s', dest='size', help='output window size', type=int, default=10)
    parser.add_argument('-i', dest='interval', help='refresh interval, 0 to run in step mode', type=float, default=1)
    parser.add_argument('-t', dest='times', help='generation time, -1 run forever', type=int, default=30)
    parser.add_argument('-d', dest='density', help='initial life numbers, size relative', type=int, default=2)
    parser.add_argument('--print', dest='output', help='output mode', const=Print, action='store_const', default=Screen)
    return parser.parse_args()
 

if __name__ == '__main__':
    args = definArgs()
    size = args.size
    output = args.output()
    if args.interval > 0:
        output.trigger = lambda : time.sleep(args.interval)
    output.runInContext(run)

