from config import *

class GameSprite(pygame.sprite.Sprite):
    IMAGE: pygame.Surface
    _groups: list[pygame.sprite.Group] = []

    @classmethod
    def init_groups(cls, groups: list[pygame.sprite.Group]) -> None:
        cls._groups = groups

    def __init__(self, x, y, width, height):
        super().__init__(*self._groups)
        self.image = self.IMAGE
        self.mask = pygame.mask.from_surface(self.IMAGE)
        tile_rect = pygame.Rect(x, y, width, height)
        self.rect = self.image.get_rect()
        self.rect.center = tile_rect.center