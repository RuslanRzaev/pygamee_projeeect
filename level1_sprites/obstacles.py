import pygame.transform

from level1_sprites import GameSprite
from config import *
from utils import load_image


class Obstacle(GameSprite):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.passed_or_not = False

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()


class ObstacleTop(Obstacle):
    def __init__(self, x, y, width, height):
        self.IMAGE = pygame.transform.smoothscale(load_image('obstacle.jpg'), (width, height))
        self.IMAGE = pygame.transform.flip(self.IMAGE, False, True)
        super().__init__(x, y, width, height)


class ObstacleBottom(Obstacle):
    def __init__(self, x, y, width, height):
        self.IMAGE = pygame.transform.smoothscale(load_image('obstacle.jpg'), (width, height))
        super().__init__(x, y, width, height)
