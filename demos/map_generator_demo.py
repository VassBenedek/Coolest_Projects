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
SPEED = 1

Point = namedtuple("Point", "x, y")


class PacManGame:
    def __init__(self, w=1600, h=900):
        self.h = h
        self.w = w
        self._generate_map()

        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Path finder")
        self.clock = pygame.time.Clock()

        self.start = Point(16, 8)

        self.available = set()
        self.to_check = [self.start]

        self.map[self.start.x, self.start.y] = False
        self.loops = 0

    def controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def play_step(self):
        self.controls()

        if self.loops < 31:
            self._path_finding()
            self.loops += 1
        elif self.loops == 31:
            self._fill_map()
            self.loops += 1

        self._update_ui()
        self.clock.tick(SPEED)

    def draw_map(self):
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                if self.map[i, j]:
                    pygame.draw.rect(self.screen, BLUE, (i * BLOCK_SIZE, j * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        for i in self.available:
            pygame.draw.rect(self.screen, YELLOW, (i.x * BLOCK_SIZE, i.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        for i in self.to_check:
            pygame.draw.rect(self.screen, RED, (i.x * BLOCK_SIZE, i.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def _update_ui(self):
        self.screen.fill(WHITE)
        self.draw_map()
        pygame.draw.rect(self.screen, GREEN, (self.start.x * BLOCK_SIZE,
                                              self.start.y * BLOCK_SIZE,
                                              BLOCK_SIZE,
                                              BLOCK_SIZE))
        pygame.display.flip()

    def _generate_map(self):
        # self.map = np.random.randint(0, 1, (int(self.w / BLOCK_SIZE), int(self.h / BLOCK_SIZE)), dtype=int)
        self.map = np.random.choice(a=[True, False],
                                    size=(int(self.w / BLOCK_SIZE), int(self.h / BLOCK_SIZE)),
                                    p=(0.25, 0.75))

    def _path_finding(self):
        available = []
        for i in self.to_check:
            neighbours = set()
            for j in range(-1, 2):
                if j == 0:
                    for k in range(1, -2, -1):
                        if 0 <= i.x - k < self.map.shape[0] and 0 <= i.y < self.map.shape[1]:
                            neighbours.add(Point(i.x - k, i.y))
                elif 0 <= i.x < self.map.shape[0] and 0 <= i.y - j < self.map.shape[1]:
                    neighbours.add(Point(i.x, i.y - j))

            for i in neighbours:
                if not self.map[i.x, i.y] and i not in self.available:
                    available.append(Point(i.x, i.y))

        self.to_check = set(available)

        for i in available:
            self.available.add(i)

    def _fill_map(self):
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                if Point(i, j) not in self.available:
                    self.map[i, j] = True


pygame.init()
font = pygame.font.Font(None, 40)

game = PacManGame()

while True:
    game.play_step()












