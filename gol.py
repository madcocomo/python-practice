import curses
from argparse import ArgumentParser
from collections import Counter
import time
import random
import sys

class Point:
    def __init__(self, y, x):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    def __str__(self):
        return '({},{})'.format(self.y, self.x)
    __repr__ = __str__
    def __hash__(self):
        return hash((self.y,self.x))
    def adjoint(self, other):
        return -1 <= other.x - self.x <= 1 \
            and -1 <= other.y -self.y <= 1 \
            and not(other.x == self.x and other.y == self.y)
    def getNeighbors(self):
        left = self.left()
        right = self.right()
        up = self.up()
        down = self.down()
        result = [left.up(), left, left.down(), up, down, right.up(), right, right.down()]
        return result
    def left(self, i=1):
        return Point(self.y, self.x-i)
    def right(self, i=1):
        return Point(self.y, self.x+i)
    def up(self, i=1):
        return Point(self.y-i, self.x)
    def down(self, i=1):
        return Point(self.y+i, self.x)

class World:
    lifeSignal = 'o'
    emptySignal = '_'
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
        for y in range(topLeft.y, bottomRight.y+1):
            for x in range(topLeft.x, bottomRight.x+1):
                result += self.lifeSignal if self.isAlive(Point(y,x)) else self.emptySignal
            if y < bottomRight.y: result += '\n'
        return result

class Screen:
    def __init__(self, waitFun):
        self.waitFun = waitFun
    def runInContext(self, fun):
        self.fun = fun
        curses.wrapper(self.__run)
    def __run(self, stdscr):
        self.leftTop = Point(0,0)
        self.__initScr(stdscr)
        self.fun(self)
    def __initScr(self, stdscr):
        stdscr.nodelay(not(self.waitFun.stepMode))
        curses.curs_set(False)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        stdscr.clear()
        self.stdscr = stdscr
    def updateViewSize(self):
        curses.update_lines_cols()
        bottom = curses.LINES-2 + self.leftTop.y
        right = curses.COLS-2 + self.leftTop.x
        self.bottomRight = Point(bottom, right)
    def trigger(self):
        self.reactInput()
        self.waitFun()
    def reactInput(self):
        c = self.stdscr.getch()
        if c == ord('q'):
             sys.exit()
        if c == curses.KEY_LEFT:
            self.leftTop = self.leftTop.left(10)
        if c == ord('H'):
            self.leftTop = self.leftTop.left(50)
        if c == curses.KEY_RIGHT:
            self.leftTop = self.leftTop.right(10)
        if c == ord('L'):
            self.leftTop = self.leftTop.right(50)
        if c == curses.KEY_UP:
            self.leftTop = self.leftTop.up(10)
        if c == ord('K'):
            self.leftTop = self.leftTop.up(50)
        if c == curses.KEY_DOWN:
            self.leftTop = self.leftTop.down(10)
        if c == ord('J'):
            self.leftTop = self.leftTop.down(50)
        if c == ord('0'):
            self.leftTop = Point(0,0)
        curses.flushinp()
    def show(self, world):
        self.updateViewSize()
        self.stdscr.addstr(0, 0, world.output(self.leftTop, self.bottomRight), curses.color_pair(1) |curses.A_DIM)
        self.stdscr.refresh()
        return world

class Print:
    def __init__(self, waitFun):
        self.waitFun = waitFun
    def runInContext(self, fun):
        fun(self)
    def trigger(self):
        if self.waitFun.stepMode:
            a = input('press enter to next generation...')
            if a == 'q': sys.exit()
        else:
            self.waitFun()
    def show(self, world):
        print('='*(size+1),'\n'+world.output(Point(0,0), Point(size,size)))
        return world

def initWorld():
    World.lifeSignal = args.lifeSignal
    World.emptySignal = args.emptySignal
    world = World()
    for initLife in range(size * int(args.density)):
        y = random.randint(0,size)
        x = random.randint(0,size)
        world.putLifeAt(Point(y,x))
    return world

def run(output):
    world = output.show(initWorld())
    i = 0
    while i != args.times:
        i += 1
        output.trigger()
        world = output.show(world.nextGen())

def defineArgs():
    parser = ArgumentParser()
    parser.add_argument('-s', dest='size', help='output window size', type=int, default=10)
    parser.add_argument('-i', dest='interval', help='refresh interval, negative to run in step mode', type=float, default=1)
    parser.add_argument('-t', dest='times', help='generation time, -1 run forever', type=int, default=30)
    parser.add_argument('-d', dest='density', help='initial life numbers, size relative', type=int, default=2)
    parser.add_argument('-ls', dest='lifeSignal', help='char to present a life', type=str, default='o')
    parser.add_argument('-es', dest='emptySignal', help='char to present an empty cell', type=str, default=' ')
    parser.add_argument('--print', dest='output', help='output mode', const=Print, action='store_const', default=Screen)
    return parser.parse_args()


if __name__ == '__main__':
    args = defineArgs()
    size = args.size
    if args.interval < 0:
        waitFun = lambda : None
        waitFun.stepMode = True
    else:
        waitFun = lambda : time.sleep(args.interval)
        waitFun.stepMode = False
    output = args.output(waitFun)
    output.runInContext(run)

