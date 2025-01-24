import random
import sqlite3
import sys
from datetime import datetime

from config import *
import pygame

from achievement import Achievement

con = sqlite3.connect("db/game.db")
cur = con.cursor()
screen = pygame.display.set_mode(SIZE)

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

def text_bg(label, col=(45, 131, 182)):
    text_bg = pygame.Surface(label.get_size())
    text_bg.fill(col)

    return text_bg

def add_to_db_sqlite(level, attempt, title, desc, img, date, achieved=0):
    con.execute(f"""INSERT INTO level{str(level)} (attempt, title, description, image, date, achieved)
                    VALUES ('{attempt}', '{title}', '{desc}', '{img}', '{date}', {achieved});""").fetchall()
    con.commit()


def delete_duplicates_sqlite(level):
    con.execute(f"""DELETE FROM level{str(level)}
                    WHERE ROWID NOT IN (
                    SELECT MAX(ROWID)
                    FROM level{str(level)}
                    GROUP BY attempt,
                    title,
                    description,
                    image,
                    achieved);""")
    con.commit()

def load_image(
        name: str,
        colorkey: pygame.Color | int | None = None) -> pygame.Surface:
    fullname = os.path.join('data', 'img', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден", file=sys.stderr)
        terminate()
    image = pygame.image.load(fullname).convert_alpha()
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate() -> None:
    pygame.quit()


def generate_obstacles(objtop, objbottom):
    top_obstacle_height = random.randint(MARGIN_COLON, HEIGHT - DISTANCE_BETWEEN_COLUMN_TOP_BOTTOM - MARGIN_COLON)
    bottom_obstacle_height = HEIGHT - DISTANCE_BETWEEN_COLUMN_TOP_BOTTOM - top_obstacle_height
    top_obstacle = objtop(WIDTH, 0, OBSTACLE_WIDTH, top_obstacle_height)
    bottom_obstacle = objbottom(WIDTH, top_obstacle_height + DISTANCE_BETWEEN_COLUMN_TOP_BOTTOM, OBSTACLE_WIDTH,
                                bottom_obstacle_height)
    return top_obstacle, bottom_obstacle


def shake(shakes_start_time, shakes_end_time, shake_intensity, TIME_GAME):
    if shakes_start_time <= TIME_GAME <= shakes_end_time:
        moved_x = random.randint(-shake_intensity, shake_intensity)
        moved_y = random.randint(-shake_intensity, shake_intensity)
    else:
        moved_x = 0
        moved_y = 0
    return moved_x, moved_y


def character_dialogue_func(screen, text, img):
    width, height = WIDTH - 300, HEIGHT // 5
    dialog_x = screen.get_width() - width
    dialog_y = screen.get_height() - height

    pygame.draw.rect(screen, BACKGROUND, (dialog_x, dialog_y, width, height))
    pygame.draw.rect(screen, BACKGROUND, (dialog_x, dialog_y, width, height))

    text_surface = pygame.font.Font(None, 32).render(text, True, pygame.Color('white'))
    text_x = dialog_x + 200
    text_y = dialog_y + 50
    screen.blit(text_surface, (text_x, text_y))

    img_x = dialog_x + 20
    img_y = dialog_y + 20
    screen.blit(img, (img_x, img_y))


def generate_fuel(time_game, number_fuel, player, Gasoline, fuel_group: pygame.sprite.Group):
    if time_game % 10 == 0 and time_game != 0:
        if len(fuel_group) < number_fuel:
            x = random.randint(PLAYER_SPAWN_X + 100, WIDTH)
            y = random.randint(100, HEIGHT - 100)
            fuel = Gasoline(x, y, GASOLINE_WIDTH, GASOLINE_HEIGHT)
            fuel_group.add(fuel)


def generate_obsracled(obstacles_group, TIME_GAME, ObstacleTop, ObstacleBottom, all_sprites):
    # Генерация препятствий
    if (not len(obstacles_group) or obstacles_group.sprites()[
        -1].rect.x < WIDTH - DISTANCE_BETWEEN_COLUMN) and TIME_GAME >= 7 and not (
            62 < TIME_GAME < 90) and not (TIME_GAME > 190):
        top, bottom = generate_obstacles(ObstacleTop, ObstacleBottom)
        obstacles_group.add(top, bottom)
        all_sprites.add(top, bottom)


def show_devices(screen, player, font):
    # Подсчет point
    time = font.render(f'Poins: {int(player.point)}', True, pygame.Color('black'))
    screen.blit(time, (50, 60))

    # Подсчет попыток
    time = font.render(f'LIVES: {int(player.lives)}', True, pygame.Color('red'))
    screen.blit(time, (50, 90))

    # Подсчет бензина
    time = font.render(f'Бензин: {int(player.gasoline_level)}', True, pygame.Color('black'))
    screen.blit(time, (50, 120))

    # Приборы
    time = font.render(f'Глубина: {int(player.rect.y)}', True, pygame.Color('black'))
    screen.blit(time, (WIDTH - 200, 60))

title1 = 'Рыбы дуреют с этой прикормки'
desc1 = 'Успешно сбежать от хищных рыб'

title2 = 'Крутой Джа-Джа'
desc2 = 'Не умереть на первом уровне'

achievement_fish = Achievement(1100, 100, ACHIEVEMENT_BG, title1, desc1, KARASIKI)

achievement_ja_ja = Achievement(1100, 100, ACHIEVEMENT_BG, title2, desc2, ACHIEVEMENT_3_1)

showed_a = False
showed_a_ja = False
len_db_level_1 = con.execute("SELECT COUNT (*) FROM level1").fetchone()
current_attempt = 1 if int(len_db_level_1[0]) < 1 else len_db_level_1[0]

def timings(screen, problem_sound, TIME_GAME, fish_group, big_fish_group, font, player):
    global showed_a, showed_a_ja
    if 55 < TIME_GAME < 60:
        text = font.render(f'РЫБА ГУБЕР СОВСЕМ БЛИЗКА', True, pygame.Color('RED'))
        text1 = font.render(f'ПРИГОТОВЬТЕСЬ К УСКОРЕНИЮ!(SHIFT)', True, pygame.Color('RED'))
        screen.blit(text, (WIDTH - 470, 90))
        screen.blit(text1, (WIDTH - 470, 120))
        problem_sound.set_volume(0.3)
        problem_sound.play()

    if 60 < TIME_GAME < 77:
        fish_group.draw(screen)
        fish_group.update()

    if 75 < TIME_GAME < 90:
        big_fish_group.draw(screen)
        big_fish_group.update()
        problem_sound.stop()


    if 80 < TIME_GAME < 120:
        if not showed_a:
            add_to_db_sqlite(1, current_attempt, title1, desc1, 'карасики.png',
                               str(datetime.now())[:-7],
                               1)
            showed_a = True
        achievement_fish.draw_n_move(screen, 10)


    if 140 < TIME_GAME < 165:
        font = pygame.font.Font(None, 32)
        time = font.render(f'Неисправный мотор!', True, pygame.Color('yellow'))
        screen.blit(time, (WIDTH - 250, 90))
        problem_sound.set_volume(0.3)
        problem_sound.play()

    if TIME_GAME > 165:
        problem_sound.stop()

    if TIME_GAME > 196: # 196
        player.gasoline_level = 0
        player.rect.x += 5
        player.rect.y -= 3
        if not showed_a_ja:
            add_to_db_sqlite(1, current_attempt, title2, desc2, 'icon_3_1.png',
                               str(datetime.now())[:-7],
                               1)
            showed_a_ja = True
        achievement_ja_ja.draw_n_move(screen, 10)

    if TIME_GAME > 199: # 199
        pygame.event.post(pygame.event.Event(GAME_STOP))


def shakes(shakes_start_time, shakes_end_time, shakes_intensity, TIME_GAME, screen, BACKGROUND_IMAGE):
    moved_x, moved_y = shake(shakes_start_time, shakes_end_time, shakes_intensity,
                             TIME_GAME)
    screen.blit(BACKGROUND_IMAGE, (0 + moved_x, 0 + moved_y))


def get_achievements(attempt=None):
    achievements = []
    for i in range(1, 3):
        if attempt is not None:
            cur.execute(f'SELECT * FROM level{i} WHERE attempt = {attempt}')
        else:
            cur.execute(f'SELECT * FROM level{i}')
        achievements.extend([achievement + (i,) for achievement in cur.fetchall()])
    return achievements

def get_number_of_achievements_per_level(level: int) -> int:
    try:
        count = cur.execute(f'SELECT count(*) FROM level{level}').fetchall()
        if count:
            return int(count[0][0])
    except sqlite3.OperationalError:
        pass

def get_count_achievement(level, name_achievement: str) -> int:
    count = cur.execute(f'SELECT count(*) FROM level{level} WHERE title == "{name_achievement}"').fetchall()
    return int(count[0][0])


PLAYER_HIT = pygame.event.custom_type()
GAME_STOP = pygame.event.custom_type()
