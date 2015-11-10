#!/usr/bin/python

from random import randrange, shuffle, random
from time import sleep
import curses
import sys

class Maze:

    __directions = ('N', 'E', 'S', 'W')

    __leftDirection = {
        'N': 'W',
        'E': 'N',
        'S': 'E',
        'W': 'S',
    }

    __rightDirection = {
        'N': 'E',
        'E': 'S',
        'S': 'W',
        'W': 'N',
    }

    __dirToChar = {
        'N': '^',
        'E': '>',
        'S': '.',
        'W': '<',
    }

    __dirToDelta = {
        'N': ( 0, -1),
        'E': ( 1,  0),
        'S': ( 0,  1),
        'W': (-1,  0),
    }

    def __init__(self, width, height, stdscr):
        self.__width = width
        self.__height = height
        self.__maze = [['w' for x in range(height)] for x in range(width)]
        self.__walls = height*width - 1
        self.__moves = 0
        self.__stdscr = stdscr
        self.__pause = 0
        self.__direction = 'N'
        self.__x, self.__y = randrange(self.__width), randrange(self.__height)

        self.__btToColor = {
            'w': curses.color_pair(0),
            'e': curses.color_pair(1),
            'v': curses.color_pair(2),
            '2': curses.color_pair(3),
        }
        self.__maze[self.__x][self.__y] = 'v'
        self.__visited = 1
        self.__visited2 = 0
        self.__unvisited = 0
        self.__bumps = 0
        self.draw_player()
        self.stats()


    def width(self):
        return self.__width

    def height(self):
        return self.__height

    def turn(self, n = 1):
        n %= 4
        if n == 3:
            self.__direction = self.__leftDirection[self.__direction]
            self.draw_player()
        else:
            for i in range(n):
                self.__direction = self.__rightDirection[self.__direction]
                self.draw_player()

    def turnLeft(self):
        self.turn(-1)

    def turnRight(self):
        self.turn()

    def free_block(self, x, y):
        stdscr = self.__stdscr
        self.__maze[x][y] = 'e'
        stdscr.addstr(y+1, x+1, ' ', self.__btToColor['e'])

    def in_bounds(self, coord):
        x, y = coord[0], coord[1]
        return ( x >= 0 and x < self.__width and
            y >= 0 and y < self.__height)

    def block_free(self, coord):
        x, y = coord[0], coord[1]
        return self.__maze[x][y] != 'w'

    def visited(self, coord):
        x, y = coord[0], coord[1]
        return self.__maze[x][y] in ('v', '2')

    def block_removeable(self, coord):
        if self.block_free(coord):
            return False

        x, y = coord[0], coord[1]
        bl = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        n = 0
        for i in bl:
            if self.in_bounds(i) and self.block_free(i):
                n += 1
        return n <= 1 or random() < self.__loop_prob

    def walled_neigbour_blocks(self, coord):
        x, y = coord[0], coord[1]
        bl = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        shuffle(bl)
        rbl = []
        for i in bl:
            if self.in_bounds(i) and not self.block_free(i):
                rbl.append(i)
        return rbl

    def draw_player(self):
        x, y = self.__x, self.__y
        stdscr.addstr(y+1, x+1, self.__dirToChar[self.__direction],
            self.__btToColor[self.__maze[x][y]])

        if self.__pause > 0:
            self.__stdscr.refresh()
            sleep(self.__pause)


    def undraw_player(self):
        x, y = self.__x, self.__y
        stdscr.addstr(y+1, x+1, ' ',
            self.__btToColor[self.__maze[x][y]])

    def move(self):
        x, y = self.__x, self.__y
        nx = x + self.__dirToDelta[self.__direction][0]
        ny = y + self.__dirToDelta[self.__direction][1]

        if self.in_bounds((nx, ny)) and self.block_free((nx, ny)):
            if self.__maze[nx][ny] == 'e':
                self.__maze[nx][ny] = 'v'
                self.__visited += 1
                self.__unvisited -= 1
            elif self.__maze[nx][ny] == 'v':
                self.__maze[nx][ny] = '2'
                self.__visited2 += 1
            self.undraw_player()
            self.__x, self.__y = nx, ny
            self.__moves += 1
            self.draw_player()
        else:
            self.__bumps += 1
            curses.beep()

        self.stats()

    def generate(self, deep=True, loop_prob = 0.05):
        self.__loop_prob = loop_prob
        x, y = self.__x, self.__y
        ends = self.walled_neigbour_blocks((x, y))
        while ends:
            if deep:
                x, y = ends.pop()
            else:
                x, y = ends.pop(randrange(len(ends)))
            if self.block_removeable((x, y)):
                self.free_block(x, y)
                self.__walls -= 1
                self.__unvisited += 1
                self.stats()
                ends += self.walled_neigbour_blocks((x, y))
                if self.__pause > 0:
                    stdscr.refresh()
                    sleep(self.__pause)
        self.__ends = 0
        self.stats()


    def stats(self):
        x = self.__width + 2
        stdscr.addstr(0, x, 'Maze')
        stdscr.addstr(2, x, 'Dimension')
        stdscr.addstr(3, x, " {} x {}".format(self.__width, self.__height))
        stdscr.addstr(5, x, 'Walls')
        stdscr.addstr(6, x, "{:9}".format(self.__walls))
        stdscr.addstr(8, x, 'Unvisited')
        stdscr.addstr(9, x, "{:9}".format(self.__unvisited))
        stdscr.addstr(11, x, 'Visited')
        stdscr.addstr(12, x, "{:9}".format(self.__visited))
        stdscr.addstr(14, x, '2nd Vis.')
        stdscr.addstr(15, x, "{:9}".format(self.__visited2))
        stdscr.addstr(17, x, 'Bumps')
        stdscr.addstr(18, x, "{:9}".format(self.__bumps))
        stdscr.addstr(20, x, 'Moves')
        stdscr.addstr(21, x, "{:9}".format(self.__moves))
        stdscr.refresh()

    def unvisited(self):
        return self.__unvisited

    def setPause(self, pause):
        self.__pause = pause

    def frontFree(self):
        x, y = self.__x, self.__y
        nx = x + self.__dirToDelta[self.__direction][0]
        ny = y + self.__dirToDelta[self.__direction][1]

        return self.in_bounds((nx, ny)) and self.block_free((nx, ny))

    def frontUnVisited(self):
        x, y = self.__x, self.__y
        nx = x + self.__dirToDelta[self.__direction][0]
        ny = y + self.__dirToDelta[self.__direction][1]

        return self.__maze[nx][ny] == 'e'

    def frontOnceVisited(self):
        x, y = self.__x, self.__y
        nx = x + self.__dirToDelta[self.__direction][0]
        ny = y + self.__dirToDelta[self.__direction][1]

        return self.__maze[nx][ny] == 'v'

    def markTwiceVisited(self):
        x, y = self.__x, self.__y
        self.__maze[x][y] = '2'
        self.__visited2 += 1
        self.draw_player()


def maze_random_algo(m, blind = True):
    while m.unvisited() > 0:
        for i in range(randrange(4)):
            if random() > 0.5:
                m.turnLeft()
            else:
                m.turnRight()
        if blind or m.frontFree():
            m.move()

def maze_tremaux_algo(m):
    def step(i):
        if i == 1:
            m.turnRight()
            m.turnRight()
        else:
            m.turnLeft()

    def findUnVistedDir():
        for i in range(3):
            if m.frontFree() and m.frontUnVisited():
                return True
            step(i)
        return False

    def findOnceVistedDir():
        for i in range(3):
            if m.frontFree() and m.frontOnceVisited():
                return True
            step(i)
        return False

    def findOnlyDir():
        n = 0
        for i in range(3):
            if m.frontFree():
                n += 1
            step(i)
        if n != 1:
            return False

        for i in range(3):
            if m.frontFree():
                return True
            step(i)

    def goDeep():
        while findUnVistedDir():
            m.move()

    def turnAround():
        m.turnLeft()
        m.turnLeft()
        m.markTwiceVisited()

    def goBack():
        while True:
            if findUnVistedDir():
                return True
            if findOnceVistedDir():
                m.move()
            elif findOnlyDir():
                m.move()
            else:
                return False
    while True:
        goDeep()
        turnAround()
        if not goBack():
            m.turnRight()
            if m.frontFree():
                m.move()
                if not goBack():
                    break
            else:
                break

def maze_backtrack_algo_rec(m, first=True):

    if first:
        n = 4
    else:
        n = 3

    for i in range(n):
        m.turn(i)
        if m.frontFree() and m.frontUnVisited():
            m.move()
            maze_backtrack_algo_rec(m, False)

    if not first:
        m.turn(-1)
        m.move()
        m.turn(2)

def maze_backtrack_algo_it(m):
    stack = [[3, 2, 1, 0]]
    while stack:
        job = stack.pop()
        if job:
            i = job.pop()
            stack.append(job)
            m.turn(i)
            if m.frontFree() and m.frontUnVisited():
                m.move()
                stack.append([2, 1, 0])
        elif stack:
            m.turn(-1)
            m.move()
            m.turn(2)

def main(stdscr):
    stdscr.clear()
    stdscr.keypad(True)
    curses.curs_set(False)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
    m = Maze(curses.COLS-12, curses.LINES-2, stdscr)

    m.generate(False, 0)
    m.setPause(0.0001)

    stdscr.refresh()
    key=''
    while key != 'q':
        key = stdscr.getkey()
        if key == 'KEY_LEFT':
            m.turnLeft()
            continue
        if key == 'KEY_RIGHT':
            m.turnRight()
            continue
        if key == 'KEY_UP':
            m.move()
            continue
        if key == 'i':
            maze_backtrack_algo_it(m)
            continue
        if key == 'r':
            maze_backtrack_algo_rec(m)
            continue
        if key == 't':
            maze_tremaux_algo(m)
            continue


stdscr = curses.initscr()
curses.wrapper(main)
