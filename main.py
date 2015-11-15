#!/usr/bin/python

import maze
import cursesMS
import sdlMS
from random import randrange

def maze_random_algo(m, blind = True):
    while m.unvisited() > 0:
        m.turn(randrange(4))
        if blind or m.frontFree():
            m.move()

def maze_tremaux_algo(m):
    def step(i):
        if i == 1:
            m.turn(2)
        else:
            m.turn(-1)

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
        m.turn(2)
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
            m.turn()
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

try:
    screen = sdlMS.sdlMazeScreen()
    #screen = cursesMS.cursesMazeScreen()
    m = maze.Maze(screen)

    m.setPause(0.001)
    m.generate()

    key=''
    while key != 'q':
        key = screen.getkey()
        if key == 'KEY_LEFT':
            m.turn(-1)
            continue
        if key == 'KEY_RIGHT':
            m.turn()
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
        if key == 'b':
            maze_random_algo(m)
            continue
        if key == 'm':
            maze_random_algo(m, False)
            continue
finally:
    sdlMS.sdlMazeScreen.cleanup()
    #cursesMS.cursesMazeScreen.cleanup()
