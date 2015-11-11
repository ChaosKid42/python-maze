from random import randrange, shuffle, random
from time import sleep

class Maze:
    __dirToDelta = {
        0: ( 0, -1),
        1: ( 1,  0),
        2: ( 0,  1),
        3: (-1,  0),
    }

    def __init__(self, screen):
        width = screen.width()
        height = screen.height()
        self.__screen = screen
        self.__width = width
        self.__height = height
        self.__maze = [[-1 for x in range(height)] for x in range(width)]
        self.__walls = height*width - 1
        self.__moves = 0
        self.__pause = 0
        self.__direction = 0
        self.__x, self.__y = randrange(self.__width), randrange(self.__height)

        self.__maze[self.__x][self.__y] = 1
        self.__screen.draw_player(self.__x, self.__y, self.__direction, 1)
        self.__visited = 1
        self.__visited2 = 0
        self.__unvisited = 0
        self.__bumps = 0
        self.draw_player()
        self.draw_stats()

    def turn(self, n = 1):
        self.__direction += n
        self.__direction %= 4
        self.draw_player()
        self.__screen.play_turn_sound()

    def free_block(self, x, y):
        self.__maze[x][y] = 0
        self.__screen.draw_empty(x, y, self.__maze[x][y])

    def in_bounds(self, coord):
        x, y = coord[0], coord[1]
        return ( x >= 0 and x < self.__width and
            y >= 0 and y < self.__height)

    def block_free(self, coord):
        x, y = coord[0], coord[1]
        return self.__maze[x][y] != -1

    def visited(self, coord):
        x, y = coord[0], coord[1]
        return self.__maze[x][y] > 0

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

    def draw_stats(self):
        screen = self.__screen
        screen.draw_walls_stats(self.__walls)
        screen.draw_unvisited_stats(self.__unvisited)
        screen.draw_visited_stats(self.__visited)
        screen.draw_visited2_stats(self.__visited2)
        screen.draw_bumps_stats(self.__bumps)
        screen.draw_moves_stats(self.__moves)

    def draw_player(self):
        x, y = self.__x, self.__y
        self.__screen.draw_player(x, y, self.__direction, self.__maze[x][y])

        if self.__pause > 0:
            self.__screen.refresh()
            sleep(self.__pause)

    def undraw_player(self):
        x, y = self.__x, self.__y
        self.__screen.draw_empty(x, y, self.__maze[x][y])

    def move(self):
        x, y = self.__x, self.__y
        nx = x + self.__dirToDelta[self.__direction][0]
        ny = y + self.__dirToDelta[self.__direction][1]

        if self.in_bounds((nx, ny)) and self.block_free((nx, ny)):
            if self.__maze[nx][ny] == 0:
                self.__maze[nx][ny] = 1
                self.__visited += 1
                self.__unvisited -= 1
            elif self.__maze[nx][ny] == 1:
                self.__maze[nx][ny] = 2
                self.__visited2 += 1
            self.undraw_player()
            self.__x, self.__y = nx, ny
            self.__moves += 1
            self.draw_player()
            self.__screen.play_move_sound()
        else:
            self.__bumps += 1
            self.__screen.play_bump_sound()

        self.draw_stats()

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
                self.draw_stats()
                ends += self.walled_neigbour_blocks((x, y))
                if self.__pause > 0:
                    self.__screen.refresh()
                    sleep(self.__pause)
        self.__ends = 0
        self.draw_stats()

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

        return self.__maze[nx][ny] == 0

    def frontOnceVisited(self):
        x, y = self.__x, self.__y
        nx = x + self.__dirToDelta[self.__direction][0]
        ny = y + self.__dirToDelta[self.__direction][1]

        return self.__maze[nx][ny] == 1

    def markTwiceVisited(self):
        x, y = self.__x, self.__y
        self.__maze[x][y] = 2
        self.__visited2 += 1
        self.draw_player()
