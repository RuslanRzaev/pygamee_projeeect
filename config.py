import pygame

SIZE = WIDTH, HEIGHT = 800, 600  # размеры окна
FPS = 60  # FPS

BACKGROUND = pygame.Color('black')  # изначальный цвет окна(пока всё прогрузится
PLAYER_WIDTH = 100  # ширина игрока
PLAYER_HEIGHT = 100  # высота игрока
PLAYER_SPAWN_X = 100  # начальное место спавна по оси X
PLAYER_SPAWN_Y = HEIGHT // 2  # начальное место спавна по оси y
GASOLINE_WIDTH = 80
GASOLINE_HEIGHT = 50
FISH_WIDTH = 80
FISH_HEIGHT = 80
BIG_FISH_WIDTH = 150
BIG_FISH_HEIGHT = 150
OBSTACLE_WIDTH = 100  # ширина столбцов
OBSTACLE_SPEED = 4 / (FPS / 60)  # скорость игры(передвижения столбцов)
JUMP = -1.7 * (60 / FPS)  # сила прыжка
MAX_FALL_SPEED = 1  # максимальная скорость падения
DISTANCE_BETWEEN_COLUMN_TOP_BOTTOM = 200  # расстояние между двумя колоннами(пара)
DISTANCE_BETWEEN_COLUMN = 700  # расстояние между колоннами
MARGIN_COLON = 50  # Чтобы препятсвия не слипались с краями экрана
ACHIEVEMENT_3_1 = 'data/img/icon_arch'
GRAVITY = 0.25  # гравитация
POWER_JUMP = -2  # сила прыжка
