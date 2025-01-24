from random import randrange

from config import *


class Asteroid:
    def __init__(self, x, y, health=10):
        self.img = ASTEROID_R1
        self.mask = pygame.mask.from_surface(self.img)
        self.max_health = health
        self.rotation = 0
        self.x = x
        self.y = y
        self.rect = self.img.get_rect()
        self.rotation_speed = randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        self.health = health

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > 300:
            self.last_update = time_now
            if self.img == ASTEROID_R1:
                self.img = ASTEROID_R2
            elif self.img == ASTEROID_R2:
                self.img = ASTEROID_R3
            elif self.img == ASTEROID_R3:
                self.img = ASTEROID_R4
            elif self.img == ASTEROID_R4:
                self.img = ASTEROID_R1
