from config import *
from utils import load_image


class AchievementFinal:
    def __init__(self, attempt, title, description, icon_path, date, achieved, level):
        self.attempt = attempt
        self.title = title
        self.description_date_lev = f"{description}   {date}   (Уровень {level})"
        self.icon = load_image(icon_path)
        self.bg = pygame.transform.scale(ACHIEVEMENT_BG, (900, 100))
        self.date = date
        self.achieved = achieved
        self.level = level

    def draw(self, screen, x, y):
        screen.blit(self.bg, (x, y))
        title = pygame.font.SysFont("comicsans", 35).render(self.title, True, (255, 255, 255))
        desc = pygame.font.SysFont("comicsans", 22).render(self.description_date_lev, True, (255, 255, 255))

        screen.blit(title, (x, y + 10))
        screen.blit(desc, (x, y + 55))

        screen.blit(pygame.transform.scale(self.icon, (100, 100)), (x + self.bg.get_width() - 150, y))
        if self.achieved == 1:
            screen.blit(CHECK_MARK, (x + 850, y + CHECK_MARK.get_height() / 2))
        else:
            screen.blit(CROSS, (x + 850, y + CHECK_MARK.get_height() / 2))
