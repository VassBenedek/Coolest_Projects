import pygame
import numpy as np
from collections import namedtuple

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SIZE = (800, 600)
AQUA_MARINE = (127, 255, 212)
CRIMSON = (220, 20, 60)
SNOW = (255, 250, 250)
GHOST_WHITE = (248, 248, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 0, 255)
BROWN = (255, 255, 0)
ORANGE = (255, 140, 0)
ORANGERED = (255, 69, 0)

BLOCK_SIZE = 50
SPEED = 2

Point = namedtuple("Point", "x, y")


class Tile:
    def __init__(self, pos, parent):
        self.parent = parent
        self.pos = pos

    def __repr__(self):
        return f"{self.pos} {self.parent}"


def _true_check(a, b, get_value=False):
    for i in a:
        if i.pos == b.pos:
            if get_value:
                return i
            return True
    return False


def list_check(a):
    b = []
    for i in a:
        if not _true_check(b, i):
            b.append(i)

    return b


def _get_parent(lista, target):
    for i in lista:
        if i.pos == target.parent:
            return i


class PacManGame:
    def __init__(self, font, w=1900, h=900):
        self.h = h
        self.w = w
        self.font = font
        self._generate_map()

        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Path finder")
        self.clock = pygame.time.Clock()

        # self.start = Point(np.random.randint(0, self.map.shape[0]),
        #                    np.random.randint(0, self.map.shape[1]))
        # self.end = Point(np.random.randint(0, self.map.shape[0]),
        #                    np.random.randint(0, self.map.shape[1]))
        self.start = Point(self.map.shape[0] - 1, self.map.shape[1] - 1)
        self.end = Point(0, 0)
        self.map[self.end.x, self.end.y] = False
        self.route = None

        self.available = []
        self.to_check = [Tile(self.start, self.start)]

        self.map[self.start.x, self.start.y] = False
        self.loops = 0

    def controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def play_step(self):
        self.controls()

        if self.loops < 700 and type(self.route) != list:
            self._path_finding()
            self.loops += 1

        self._update_ui()
        self.clock.tick(SPEED)

    def draw_map(self):
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                if self.map[i, j]:
                    pygame.draw.rect(self.screen, BLUE, (i * BLOCK_SIZE, j * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        for i in self.available:
            pygame.draw.rect(self.screen, YELLOW, (i.pos.x * BLOCK_SIZE, i.pos.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            # text = self.font.render(f"{i.pos.x} {i.pos.y}", True, BLACK, YELLOW)
            # self.screen.blit(text, (i.pos.x * BLOCK_SIZE, i.pos.y * BLOCK_SIZE))

        for i in self.to_check:
            pygame.draw.rect(self.screen, ORANGE, (i.pos.x * BLOCK_SIZE, i.pos.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        if type(self.route) == list:
            for i in self.route:
                pygame.draw.rect(self.screen, BLACK, (i.pos.x * BLOCK_SIZE, i.pos.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def _update_ui(self):
        self.screen.fill(WHITE)
        self.draw_map()
        pygame.draw.rect(self.screen, GREEN, (self.start.x * BLOCK_SIZE,
                                              self.start.y * BLOCK_SIZE,
                                              BLOCK_SIZE,
                                              BLOCK_SIZE))
        pygame.draw.rect(self.screen, RED, (self.end.x * BLOCK_SIZE,
                                            self.end.y * BLOCK_SIZE,
                                            BLOCK_SIZE,
                                            BLOCK_SIZE))
        pygame.display.flip()

    def _generate_map(self):
        # self.map = np.random.randint(0, 1, (int(self.w / BLOCK_SIZE), int(self.h / BLOCK_SIZE)), dtype=int)
        self.map = np.random.choice(a=[True, False],
                                    size=(int(self.w / BLOCK_SIZE), int(self.h / BLOCK_SIZE)),
                                    p=(0.3, 0.7))

    def _path_finding(self):
        available = []
        for i in self.to_check:
            neighbours = []
            for j in range(-1, 2):
                if j == 0:
                    for k in range(1, -2, -1):
                        if 0 <= i.pos.x - k < self.map.shape[0] and 0 <= i.pos.y < self.map.shape[1]:
                            neighbours.append(Tile(Point(i.pos.x - k, i.pos.y), i.pos))
                elif 0 <= i.pos.x < self.map.shape[0] and 0 <= i.pos.y - j < self.map.shape[1]:
                    neighbours.append(Tile(Point(i.pos.x, i.pos.y - j), i.pos))

            for i in neighbours:
                if not self.map[i.pos.x, i.pos.y] and not _true_check(self.available, i):
                    available.append(i)

        self.to_check = list_check(available)
        if _true_check(self.to_check, Tile(self.end, self.end)):
            end_tile = _true_check(self.to_check, Tile(self.end, self.end), get_value=True)
            route = [end_tile]
            while not _true_check(route, Tile(self.start, self.start)):
                the_list = self.to_check
                the_list.extend(self.available)
                route.append(_get_parent(the_list, route[-1]))
                self.route = route
            self.available = self.to_check
            self.to_check = []

        for i in available:
            if not _true_check(self.available, i):
                self.available.append(i)

pygame.init()
font = pygame.font.Font(None, 20)

game = PacManGame(font)

while True:
    game.play_step()












