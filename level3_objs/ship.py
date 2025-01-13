import pygame.sprite

from config import *
from laser import Laser


class Ship(pygame.sprite.Sprite):
    COOLDOWN = 30

    def __init__(self, x, y, health=100, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.health = health
        self.img = YELLOW_SPACE_SHIP
        self.laser_img = RED_LASER
        self.lasers = []
        self.cool_down_counter = 0
        self.max_health = 100
        self.rect = self.img.get_rect()

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        self.healthbar(window)
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 10, self.y, self.laser_img)
            laser2 = Laser(self.x - 50, self.y, self.laser_img)
            self.lasers.append(laser)
            self.lasers.append(laser2)
            self.cool_down_counter = 1

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.img.get_height() + 10, self.img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.img.get_height() + 10, self.img.get_width() * (self.health / self.max_health), 10))
