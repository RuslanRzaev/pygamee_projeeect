from config import *
from sprites import GameSprite
from utils import load_image


class Gasoline(GameSprite):

    def __init__(self, x, y, width, height):
        self.IMAGE = pygame.transform.smoothscale(load_image('gasoline.png'), (width, height))
        super().__init__(x, y, width, height)

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()
