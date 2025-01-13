from datetime import datetime

from config import *
from utils import *


class Achievement:
    def __init__(self, x, y, image_bg, title, desc, icon=ACHIEVEMENT_3_1):
        self.x = x
        self.y = y
        self.img_bg = image_bg
        self.title = title
        self.desc = desc
        self.icon = icon
        self.rect = self.img_bg.get_rect()
        self.time_count = 0

    def draw_n_move(self, window, vel):
        if self.time_count >= 360:
            if self.x < 1000:
                self.x += vel * 2
        else:
            if self.x > WIDTH - self.img_bg.get_width():
                self.x -= vel
            self.time_count += 1
        if self.x < 1000:
            window.blit(self.img_bg, (self.x, self.y))
            window.blit(self.icon, (self.x, self.y))
            title = pygame.font.SysFont("comicsans", 35).render(f"{self.title}", True, (255, 255, 255))
            window.blit(title, (self.x + self.icon.get_width(), self.y))
            f_size = 20
            description = pygame.font.SysFont("comicsans", f_size).render(f"{self.desc}", True, (255, 255, 255))
            window.blit(description, (self.x + self.icon.get_width(), self.y + title.get_height()))