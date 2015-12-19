import pygame

class sdlMazeScreen:

    __screen_size = (1024, 768)
    __sprite_size = (32, 32)
    __window_name = "Maze in Python"
    __font_color = (255, 255, 255)
    __font_bgcolor = (0, 0, 0)

    __keymap = {
        pygame.K_q: 'q',
        pygame.K_ESCAPE: 'q',
        pygame.K_i: 'i',
        pygame.K_r: 'r',
        pygame.K_t: 't',
        pygame.K_b: 'b',
        pygame.K_b: 'm',
        pygame.K_LEFT: 'KEY_LEFT',
        pygame.K_RIGHT: 'KEY_RIGHT',
        pygame.K_UP: 'KEY_UP',
        }

    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode(self.__screen_size)

        self.__player = []
        self.__player.append(pygame.image.load("player_up.png").convert())
        self.__player.append(pygame.image.load("player_right.png").convert())
        self.__player.append(pygame.image.load("player_down.png").convert())
        self.__player.append(pygame.image.load("player_left.png").convert())
        self.__floor = []
        self.__floor.append(pygame.image.load("floor0.png").convert())
        self.__floor.append(pygame.image.load("floor1.png").convert())
        self.__floor.append(pygame.image.load("floor2.png").convert())
        self.__wall = pygame.image.load("wall.png").convert()

        self.__move_sound = pygame.mixer.Sound('move_sound.wav')
        self.__turn_sound = pygame.mixer.Sound('turn_sound.wav')
        self.__bump_sound = pygame.mixer.Sound('bump_sound.wav')

        self.__font = pygame.font.Font(None, 24)
        self.__font_height = self.__font.size('')[1]
        self.__font_xpos = (self.width() + 2) * self.__sprite_size[1]
        self.__font_width = self.__screen_size[0]  - self.__font_xpos

        pygame.display.set_caption(self.__window_name)
        pygame.event.set_allowed(None)
        pygame.event.set_allowed((pygame.QUIT, pygame.KEYDOWN))
        for y in range(-1, self.height()+1):
            self.draw_wall(-1, y)
            self.draw_wall(self.width(), y)
        for x in range(-1, self.width()+1):
            self.draw_wall(x, -1)
            self.draw_wall(x, self.height())
        self.draw_stats_table()

    def render_stats_text(self, text, y):
        text = self.__font.render(text, 1, self.__font_color)
        textpos = text.get_rect()
        textpos.move_ip(self.__font_xpos, y * self.__font_height)
        textpos.width = self.__font_width
        textpos.right
        self.__screen.fill(self.__font_bgcolor, textpos)
        self.__screen.blit(text, textpos)
        return textpos

    def draw_stats_table(self):
        textrect = self.render_stats_text("Maze", 0)
        self.render_stats_text("Dimensions", 2)
        self.render_stats_text("{} x {}".format(self.width(),
            self.height()), 3)
        self.render_stats_text("Walls", 5)
        self.render_stats_text("Unvisited", 8)
        self.render_stats_text("Visited", 11)
        self.render_stats_text("2nd Vis.", 14)
        self.render_stats_text("Bumps", 17)
        textrect1 = self.render_stats_text("Moves", 20)
        textrect1.union_ip(textrect)
        pygame.display.update(textrect1)

    def draw_walls_stats(self, n):
        textrect = self.render_stats_text("{}".format(n), 6)
        pygame.display.update(textrect)

    def draw_unvisited_stats(self, n):
        textrect = self.render_stats_text("{}".format(n), 9)
        pygame.display.update(textrect)

    def draw_visited_stats(self, n):
        textrect = self.render_stats_text("{}".format(n), 12)
        pygame.display.update(textrect)

    def draw_visited2_stats(self, n):
        textrect = self.render_stats_text("{}".format(n), 15)
        pygame.display.update(textrect)

    def draw_bumps_stats(self, n):
        textrect = self.render_stats_text("{}".format(n), 18)
        pygame.display.update(textrect)

    def draw_moves_stats(self, n):
        textrect = self.render_stats_text("{}".format(n), 21)
        pygame.display.update(textrect)

    def width(self):
        return int(self.__screen_size[0]/self.__sprite_size[0])-8

    def height(self):
        return int(self.__screen_size[1]/self.__sprite_size[1])-2

    def draw_wall(self, x, y):
        rect = (((x+1)*self.__sprite_size[0], (y+1)*self.__sprite_size[1]), (self.__sprite_size))
        self.__screen.blit(self.__wall, rect)
        pygame.display.update(rect)

    def draw_empty(self, x, y, visited):
        rect = (((x+1)*self.__sprite_size[0], (y+1)*self.__sprite_size[1]), (self.__sprite_size))
        self.__screen.blit(self.__floor[visited], rect)
        pygame.display.update(rect)

    def draw_player(self, x, y, direction, visited):
        rect = (((x+1)*self.__sprite_size[0], (y+1)*self.__sprite_size[1]), (self.__sprite_size))
        self.__screen.blit(self.__player[direction], rect)
        pygame.display.update(rect)

    def play_bump_sound(self):
        self.__bump_sound.play()

    def play_move_sound(self):
        self.__move_sound.play()

    def play_turn_sound(self):
        self.__turn_sound.play()

    def refresh(self):
        pass

    def getkey(self):
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            return 'q'
        if event.type == pygame.KEYDOWN:
            if event.key in self.__keymap:
                return self.__keymap[event.key]
            if event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()

    @staticmethod
    def cleanup():
        pass
