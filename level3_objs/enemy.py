from config import *
from laser import Laser
from ship import Ship


class Enemy(Ship):
    COLOR_MAP = {
                "advanced": (TIE_ADVANCED, RED_LASER),
                "assault": (TIE_ASSAULT, GREEN_LASER),
                "interceptor": (TIE_INTERCEPTOR, BLUE_LASER)
                }

    def __init__(self, x, y, color, health=50):
        super().__init__(x, y, health)
        self.img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.img)
        self.max_health = health
        self.rect = self.img.get_rect()
        self.offset = 135
        if color == 'advanced':
            self.offset = 40
        elif color == 'interceptor':
            self.offset = 100

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 20, self.y, self.laser_img)
            laser2 = Laser(self.x - 25, self.y, self.laser_img)
            self.lasers.append(laser)
            self.lasers.append(laser2)
            self.cool_down_counter = 1

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y - self.img.get_height() + self.offset, self.img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y - self.img.get_height() + self.offset, self.img.get_width() * (self.health / self.max_health), 10))
