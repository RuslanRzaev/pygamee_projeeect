import pygame.event

from config import *
from utils import load_image, PLAYER_HIT
from sprites import GameSprite

pygame.mixer.init()
crashed_sound = pygame.mixer.Sound('data/sound/звукудара.mp3')


class Player(GameSprite):
    obstacles_group = pygame.sprite.Group()
    fuel_group = pygame.sprite.Group()

    def __init__(self, x, y, width, height):
        self.IMAGE = pygame.transform.smoothscale(load_image('player2.png'), (width, height))
        super().__init__(x, y, width, height)
        self._lives = 10
        self.point = 0
        self._gasoline_level = 100
        self.speed_y = 0

    @property
    def gasoline_level(self):
        return self._gasoline_level

    @gasoline_level.setter
    def gasoline_level(self, value):
        self._gasoline_level = value
        if self._gasoline_level > 100:
            self._gasoline_level = 100
        elif self._gasoline_level < 0:
            self._gasoline_level = 0

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value):
        self._lives = value
        if self._lives < 0:
            self._lives = 0

    def update(self):
        if pygame.key.get_mods() & pygame.KMOD_SHIFT and self.gasoline_level:
            self.rect.x += 5
            self.gasoline_level -= 0.02
            if self.rect.x > 250:
                self.rect.x = 250
        else:
            self.rect.x -= 5
            if self.rect.x < PLAYER_SPAWN_X:
                self.rect.x = PLAYER_SPAWN_X

        self.rect.y += self.speed_y
        self.speed_y += GRAVITY
        self.speed_y = min(self.speed_y, MAX_FALL_SPEED)  # берем максимальное падение

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.jump()

        # Проверка на столкновения по пикселям(с препятствиями)
        for obstacle in self.obstacles_group:
            if not obstacle.passed_or_not and pygame.sprite.collide_mask(self, obstacle):
                self.lives -= 1

                # Эффект удара(звук)
                crashed_sound.set_volume(1)
                crashed_sound.play()
                pygame.event.post(pygame.event.Event(PLAYER_HIT))
                obstacle.passed_or_not = True
            if not obstacle.passed_or_not and self.rect.right > obstacle.rect.right:
                obstacle.passed_or_not = True
                self.point += 0.5

        # Проверка на столкновения по пикселям(с топливом)
        for fuel in self.fuel_group:
            if pygame.sprite.collide_mask(self, fuel):
                self.gasoline_level += 50
                fuel.kill()

    def jump(self):
        if self._gasoline_level:
            self.speed_y = POWER_JUMP
