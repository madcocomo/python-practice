from argparse import ArgumentParser
from collections import Counter, namedtuple
import curses
import time
import random
import sys
import threading

class Point(namedtuple('P', 'y x')):
    __slots__ = ()
    def adjoint(self, other):
        return not(other == self) \
            and -1 <= other.x - self.x <= 1 \
            and -1 <= other.y -self.y <= 1
    def left(self, i=1):
        return Point(self.y, self.x-i)
    def right(self, i=1):
        return Point(self.y, self.x+i)
    def up(self, i=1):
        return Point(self.y-i, self.x)
    def down(self, i=1):
        return Point(self.y+i, self.x)
    def getNeighbors(self):
        left = self.left()
        right = self.right()
        up = self.up()
        down = self.down()
        result = [left.up(), left, left.down(), up, down, right.up(), right, right.down()]
        return result

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
    def __init__(self, world, waitFun):
        self.world = world
        self.waitFun = waitFun
    def runInContext(self, fun):
        self.fun = fun
        curses.wrapper(self.__run)
    def __run(self, stdscr):
        self.leftTop = Point(0,0)
        self.__initScr(stdscr)
        self.thread = InputThread(self)
        self.thread.start()
        try:
            self.fun(self)
        except (KeyboardInterrupt):
            pass
        self.closeKeyListener(self.thread)
    def closeKeyListener(self, thread): 
        while thread.isAlive():
            try:
                curses.ungetch('q')
                if thread.isAlive(): time.sleep(0.1)
            finally:
                pass

    def __initScr(self, stdscr):
        #stdscr.nodelay(not(self.waitFun.stepMode))
        stdscr.timeout(0)
        stdscr.notimeout(1)
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
        #self.reactInput()
        self.waitFun()
        self.world = self.world.nextGen()
    def reactInput(self):
        updated = True
        c = self.stdscr.getch()
        if c == ord('q'): sys.exit()
        elif c in [curses.KEY_LEFT, ord('h')]: self.leftTop = self.leftTop.left(10)
        elif c in [curses.KEY_RIGHT, ord('l')]: self.leftTop = self.leftTop.right(10)
        elif c in [curses.KEY_UP, ord('k')]: self.leftTop = self.leftTop.up(10)
        elif c in [curses.KEY_DOWN, ord('j')]: self.leftTop = self.leftTop.down(10)
        elif c == ord('H'): self.leftTop = self.leftTop.left(50)
        elif c == ord('L'): self.leftTop = self.leftTop.right(50)
        elif c == ord('K'): self.leftTop = self.leftTop.up(50)
        elif c == ord('J'): self.leftTop = self.leftTop.down(50)
        elif c == ord('0'): self.leftTop = Point(0,0)
        else: updated = False
        #if updated: curses.flushinp()
        return updated
    def show(self):
        self.updateViewSize()
        self.stdscr.addstr(0, 0, self.world.output(self.leftTop, self.bottomRight), curses.color_pair(1) |curses.A_DIM)
        self.stdscr.refresh()

class InputThread(threading.Thread):
    def __init__(self, screen):
        threading.Thread.__init__(self)
        self.screen = screen
    def run(self):
        while self.isAlive():
            updated = self.screen.reactInput()
            if not(self.isAlive()): return
            if updated: self.screen.show()

class Print:
    def __init__(self, world, waitFun):
        self.world = world
        self.waitFun = waitFun
    def runInContext(self, fun):
        fun(self)
    def trigger(self):
        if self.waitFun.stepMode:
            a = input('press enter to next generation...')
            if a == 'q': sys.exit()
        else:
            self.waitFun()
        self.world = self.world.nextGen()
    def show(self):
        print('='*(size+1),'\n'+self.world.output(Point(0,0), Point(size,size)))

def initWorld():
    World.lifeSignal = args.lifeSignal
    World.emptySignal = args.emptySignal
    world = World()
    for initLife in range(int(size * size * args.density / 100)):
        y = random.randint(0,size)
        x = random.randint(0,size)
        world.putLifeAt(Point(y,x))
    return world

def run(runner):
    runner.show()
    i = 0
    while i != args.times:
        i += 1
        runner.trigger()
        runner.show()

def defineArgs():
    parser = ArgumentParser()
    parser.add_argument('-s', dest='size', help='output window size', type=int, default=30)
    parser.add_argument('-i', dest='interval', help='refresh interval, negative to run in step mode', type=float, default=1)
    parser.add_argument('-t', dest='times', help='generation time, -1 run forever', type=int, default=30)
    parser.add_argument('-d', dest='density', help='initial life numbers, size relative', type=int, default=10)
    parser.add_argument('-ls', dest='lifeSignal', help='char to present a life', type=str, default='o')
    parser.add_argument('-es', dest='emptySignal', help='char to present an empty cell', type=str, default=' ')
    parser.add_argument('--print', dest='runner', help='output mode', const=Print, action='store_const', default=Screen)
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
    runner = args.runner(initWorld(), waitFun)
    runner.runInContext(run)

