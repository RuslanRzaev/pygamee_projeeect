import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    SHEET: pygame.Surface = None
    COLUMNS: int = 1
    ROWS: int = 1
    FRAMES: list[pygame.Surface] = []
    RECT: pygame.Rect = None
    MARGIN_LEFT: int = 0
    MARGIN_RIGHT: int = 0
    MARGIN_TOP: int = 0
    MARGIN_BOTTOM: int = 0
    COUNT_FRAMES: int | None = None
    SPF: int = 1

    def __new__(cls, *args, **kwargs):
        if 'FRAMES' not in cls.__dict__:
            cls.FRAMES = []
            if cls.COUNT_FRAMES is None:
                cls.COUNT_FRAMES = cls.COLUMNS * cls.ROWS
            cls.cut_sheet(cls.SHEET, cls.COLUMNS, cls.ROWS)
        return super().__new__(cls)

    @classmethod
    def cut_sheet(
            cls,
            sheet: pygame.Surface,
            columns: int,
            rows: int
    ) -> None:
        cls.RECT = pygame.Rect(0, 0, (sheet.get_width() - cls.MARGIN_LEFT - cls.MARGIN_RIGHT) // columns,
                               (sheet.get_height() - cls.MARGIN_TOP - cls.MARGIN_BOTTOM) // rows)
        for row in range(rows):
            for col in range(columns):
                top_left = (cls.RECT.w * col + cls.MARGIN_LEFT, cls.RECT.h * row + cls.MARGIN_TOP)
                cls.FRAMES.append(sheet.subsurface(
                    pygame.Rect(top_left, cls.RECT.size)))
                if len(cls.FRAMES) == cls.COUNT_FRAMES:
                    return
