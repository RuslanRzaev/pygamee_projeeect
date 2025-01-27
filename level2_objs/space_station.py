from config import *


class SpaceStation:

    def __init__(self, x, y, health=300):
        self.x = x
        self.y = y
        self.health = health
        self.img = SPACE_STATION
        self.max_health = 300
        self.mask = pygame.mask.from_surface(self.img)
        self.alive = True
        self.rect = self.img.get_rect()
        self.rect_red = None
        self.rect_green = None

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        if not self.alive:
            self.healthbar(window, True)
        else:
            self.healthbar(window)

    def move(self, vel):
        if self.y <= -250:
            self.y += vel

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

    def healthbar(self, window, gone=False):
        if gone:
            coor = (0, 0, 0, 0)
        else:
            coor = (self.x, self.y + self.img.get_height() + 10, self.img.get_width(), 10)
        self.rect_red = pygame.draw.rect(window, (255, 0, 0), coor)
        self.rect_green = pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.img.get_height() + 10,
                                                                 (self.x + 0.5 * self.img.get_width()) * (
                                                                             self.health / self.max_health), 10))
