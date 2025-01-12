import os

import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 750
FPS = 60

LIVES = 1

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

TIME_POINT = 60

PLAYER_LASER_SOUND = pygame.mixer.Sound(os.path.join("data", "sound", "laser_player.mp3"))
ENEMY_LASER_SOUND = pygame.mixer.Sound(os.path.join("data", "sound", "laser_enemy.mp3"))
ENEMY_BOOM_SOUND = pygame.mixer.Sound(os.path.join("data", "sound", "enemy_boom.mp3"))
ASTEROID_BOOM_SOUND = pygame.mixer.Sound(os.path.join("data", "sound", "asteroid_boom.mp3"))
VICTORY_SOUND = pygame.mixer.Sound(os.path.join("data", "sound", "victory.mp3"))
LOST_SOUND = pygame.mixer.Sound(os.path.join("data", "sound", "lost.mp3"))

TEXT_1 =  pygame.image.load(os.path.join("data", "img", "text1.png"))
BUTTON_NEXT = pygame.image.load(os.path.join("data", "img", "button_next.png"))

PRE_3_1 = pygame.image.load(os.path.join("data", "img", "pre_3_1.png"))
PRE_3_2 = pygame.image.load(os.path.join("data", "img", "pre_3_2.png"))
PRE_3_3 = pygame.image.load(os.path.join("data", "img", "pre_3_3.png"))

ACHIEVEMENT_3_1 = pygame.image.load(os.path.join("data", "img", "icon_3_1.png"))

BG_MUSIC_BATTLE = pygame.mixer.Sound(os.path.join("data", "sound", "bg_music_battle.mp3"))
TEXT_MUSIC = pygame.mixer.Sound(os.path.join("data", "sound", "text_music.mp3"))
