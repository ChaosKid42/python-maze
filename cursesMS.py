import curses

class cursesMazeScreen:
    __dirToChar = {
        0: '^',
        1: '>',
        2: '.',
        3: '<',
    }

    def __init__(self):
        self.__stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        self.__stdscr.clear()
        self.__stdscr.keypad(True)
        self.__height = curses.LINES-2
        self.__width = curses.COLS-12
        curses.curs_set(False)
        self.draw_stats_table()

    def draw_stats_table(self):
        stdscr = self.__stdscr
        x = self.__width + 2
        stdscr.addstr(0, x, 'Maze')
        stdscr.addstr(2, x, 'Dimension')
        stdscr.addstr(3, x, " {} x {}".format(self.__width, self.__height))
        stdscr.addstr(5, x, 'Walls')
        stdscr.addstr(8, x, 'Unvisited')
        stdscr.addstr(11, x, 'Visited')
        stdscr.addstr(14, x, '2nd Vis.')
        stdscr.addstr(17, x, 'Bumps')
        stdscr.addstr(20, x, 'Moves')

    def draw_walls_stats(self, n):
        self.__stdscr.addstr(6, self.__width + 2, "{:9}".format(n))

    def draw_unvisited_stats(self, n):
        self.__stdscr.addstr(9, self.__width + 2, "{:9}".format(n))

    def draw_visited_stats(self, n):
        self.__stdscr.addstr(12, self.__width + 2, "{:9}".format(n))

    def draw_visited2_stats(self, n):
        self.__stdscr.addstr(15, self.__width + 2, "{:9}".format(n))

    def draw_bumps_stats(self, n):
        self.__stdscr.addstr(18, self.__width + 2, "{:9}".format(n))

    def draw_moves_stats(self, n):
        self.__stdscr.addstr(21, self.__width + 2, "{:9}".format(n))

    def width(self):
        return self.__width

    def height(self):
        return self.__height

    def draw_wall(self, x, y):
        self.__stdscr.addstr(y+1, x+1, ' ', curses.color_pair(0))

    def draw_empty(self, x, y, visited):
        self.__stdscr.addstr(y+1, x+1, ' ', curses.color_pair(visited+1))

    def draw_player(self, x, y, direction, visited):
        self.__stdscr.addstr(y+1, x+1, self.__dirToChar[direction],
            curses.color_pair(visited+1))

    def play_bump_sound(self):
        curses.beep()

    def play_move_sound(self):
        pass

    def play_turn_sound(self):
        pass

    def refresh(self):
        self.__stdscr.refresh()

    def getkey(self):
        return self.__stdscr.getkey()

    @staticmethod
    def cleanup():
        curses.curs_set(True)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
