import os

import pygame

pygame.init()

SIZE = WIDTH, HEIGHT = 1000, 750
FPS = 60

LIVES = 15

BACKGROUND = pygame.Color('black')  # изначальный цвет окна(пока всё прогрузится
PLAYER_WIDTH = 100  # ширина игрока
PLAYER_HEIGHT = 100  # высота игрока
PLAYER_SPAWN_X = 100  # начальное место спавна по оси X
PLAYER_SPAWN_Y = HEIGHT // 2  # начальное место спавна по оси y
GASOLINE_WIDTH = 80
GASOLINE_HEIGHT = 50
FISH_WIDTH = 50
FISH_HEIGHT = 50
BIG_FISH_WIDTH = 150
BIG_FISH_HEIGHT = 150
OBSTACLE_WIDTH = 100  # ширина столбцов
OBSTACLE_SPEED = 4 / (FPS / 60)  # скорость игры(передвижения столбцов)
JUMP = -1.7 * (60 / FPS)  # сила прыжка
MAX_FALL_SPEED = 1  # максимальная скорость падения
DISTANCE_BETWEEN_COLUMN_TOP_BOTTOM = 200  # расстояние между двумя колоннами(пара)
DISTANCE_BETWEEN_COLUMN = 700  # расстояние между колоннами
MARGIN_COLON = 50  # Чтобы препятсвия не слипались с краями экрана
GRAVITY = 0.25  # гравитация
POWER_JUMP = -2  # сила прыжка

TIE_ADVANCED = pygame.image.load(os.path.join("data", "img", "tie_advanced.png"))
TIE_ASSAULT = pygame.image.load(os.path.join("data", "img", "tie_assault.png"))
TIE_INTERCEPTOR = pygame.image.load(os.path.join("data", "img", "tie_interceptor.png"))

YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("data", "img", "n1_ship.png"))

SPACE_STATION = pygame.image.load(os.path.join("data", "img", "space_station.png"))

ACHIEVEMENT_BG = pygame.image.load(os.path.join("data", "img", "achievement_bg.png"))

RED_LASER = pygame.image.load(os.path.join("data", "img", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("data", "img", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("data", "img", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("data", "img", "pixel_laser_yellow.png"))

ASTEROID_R1 = pygame.image.load(os.path.join("data", "img", "asteroid.png"))
ASTEROID_R2 = pygame.image.load(os.path.join("data", "img", "asteroid1.png"))
ASTEROID_R3 = pygame.image.load(os.path.join("data", "img", "asteroid2.png"))
ASTEROID_R4 = pygame.image.load(os.path.join("data", "img","asteroid3.png"))

BG = pygame.transform.scale(pygame.image.load(os.path.join("data", "img", "background-black.png")), (WIDTH, HEIGHT))

VICTORY_BG = pygame.image.load(os.path.join("data", "img", "victory_bg.png"))

CHECK_MARK = pygame.transform.scale(pygame.image.load(os.path.join("data", "img", "check_mark.png")), (50, 50))
CROSS = pygame.transform.scale(pygame.image.load(os.path.join("data", "img", "cross.png")), (50, 50))

KARASIKI = pygame.transform.scale(pygame.image.load(os.path.join("data", "img", "карасики.png")), (110, 100))

MAIN_FONT = pygame.font.SysFont("comicsans", 50)
REGULAR_FONT = pygame.font.SysFont("comicsans", 40)
BIG_FONT = pygame.font.SysFont("comicsans", 60)

TEXT_NEXT = BIG_FONT.render(f"Двигаемся далее?...", False, (255, 255, 255))

TIME_POINT = 3000

CHANNEL = pygame.mixer.find_channel()

PLAYER_LASER_SOUND = pygame.mixer.Sound(os.path.join("data", "sound", "laser_player.mp3"))
ENEMY_LASER_SOUND = pygame.mixer.Sound(os.path.join("data", "sound", "laser_enemy.mp3"))
ENEMY_BOOM_SOUND = pygame.mixer.Sound(os.path.join("data", "sound", "enemy_boom.mp3"))
ASTEROID_BOOM_SOUND = pygame.mixer.Sound(os.path.join("data", "sound", "asteroid_boom.mp3"))
VICTORY_SOUND = pygame.mixer.Sound(os.path.join("data", "sound", "victory.mp3"))
LOST_SOUND = pygame.mixer.Sound(os.path.join("data", "sound", "lost.mp3"))

START_TEXT_1 = pygame.image.load(os.path.join("data", "img", "start_1.png"))
START_TEXT_2 = pygame.image.load(os.path.join("data", "img", "start_2.png"))

BUTTON_NEXT = pygame.image.load(os.path.join("data", "img", "button_next.png"))
PAUSE = pygame.image.load(os.path.join("data", "img", "pause.png"))
RESUME = pygame.image.load(os.path.join("data", "img", "play-button.png"))

PRE_3_1 = pygame.image.load(os.path.join("data", "img", "pre_3_1.png"))
PRE_3_2 = pygame.image.load(os.path.join("data", "img", "pre_3_2.png"))
PRE_3_3 = pygame.image.load(os.path.join("data", "img", "pre_3_3.png"))

ACHIEVEMENT_3_1 = pygame.image.load(os.path.join("data", "img", "icon_3_1.png"))

BG_MUSIC_BATTLE = pygame.mixer.Sound(os.path.join("data", "sound", "bg_music_battle.mp3"))
BG_LEVEL1 = pygame.mixer.Sound(os.path.join("data", "sound", "game_sound.mp3"))
TEXT_MUSIC = pygame.mixer.Sound(os.path.join("data", "sound", "text_music.mp3"))
