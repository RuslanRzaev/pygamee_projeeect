import pygame.sprite

from config import *
from level1_sprites import GameSprite
from utils import load_image
from level1_sprites.animated_sprite import AnimatedSprite


class Fish(GameSprite, AnimatedSprite):
    SHEET = load_image("fish.png")
    COLUMNS = 6
    ROWS = 1
    MARGIN_RIGHT = 150
    MARGIN_BOTTOM = 0
    COUNT_FRAMES = 1 * 6
    SPF = 1
    player = pygame.sprite.Sprite

    def __init__(self, x, y, width, height):
        self.IMAGE = pygame.transform.smoothscale(load_image('fish.png'), (width, height))
        super().__init__(x, y, width, height)
        self.FRAMES = [pygame.transform.smoothscale(frame, (width, height)) for frame in self.FRAMES]
        self.cur_frame = 0
        self.frame_duration = self.SPF
        self.image = self.FRAMES[0]
        self.rect = self.IMAGE.get_rect()

    def update(self):
        target_x, target_y = self.player.rect.center
        self.rect.y = target_y
        self.rect.x += 0.5 if self.rect.x < 150 else 0

        if self.rect.x > self.player.rect.x:
            self.rect.x = self.player.rect.x

        if pygame.sprite.collide_mask(self, self.player):
            self.player.lives -= 0.01
        self.frame_duration -= 1
        if not self.frame_duration:
            self.frame_duration = self.SPF
            self.cur_frame = (self.cur_frame + 1) % self.COUNT_FRAMES
            self.image = self.FRAMES[self.cur_frame]


class BigFish(Fish):
    target_fish = pygame.sprite.Sprite

    def __init__(self, x, y, width, height):
        self.IMAGE = pygame.transform.smoothscale(load_image('fish.png'), (width, height))
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
