
import pygame.sprite

from config import *
from sprites import GameSprite
from utils import load_image


class Fish(GameSprite):
    player = pygame.sprite.Sprite

    def __init__(self, x, y, width, height):
        self.IMAGE = pygame.transform.smoothscale(load_image('DOS-Killerfish.jpg'), (width, height))
        self.IMAGE = pygame.transform.flip(self.IMAGE, True, False)
        super().__init__(x, y, width, height)

    def update(self):
        target_x, target_y = self.player.rect.center
        self.rect.y = target_y
        self.rect.x += 0.5 if self.rect.x < 150 else 0

        if self.rect.x > self.player.rect.x:
            self.rect.x = self.player.rect.x

        if pygame.sprite.collide_mask(self, self.player):
            self.player.lives -= 0.01


class BigFish(Fish):
    target_fish = pygame.sprite.Sprite
    def __init__(self, x, y, width, height):
        self.IMAGE = pygame.transform.smoothscale(load_image('DOS-Killerfish.jpg'), (width, height))
        self.IMAGE = pygame.transform.flip(self.IMAGE, True, False)
        super().__init__(x, y, width, height)


    def update(self):
        if self.target_fish.alive():
            self.rect.x += 0.5
            self.rect.y = self.target_fish.rect.y
        else:
            self.rect.x += 1

        if pygame.sprite.collide_mask(self, self.target_fish):
            if self.target_fish.alive():
                self.target_fish.kill()

        if self.rect.x > WIDTH:
            self.kill()