import os
import random
import sys
from config import *


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
    sys.exit()


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


def generate_fuel(number_fuel, player, Gasoline, fuel_group: pygame.sprite.Group):
    if player.time_game % 10 == 0 and player.time_game != 0:
        if len(fuel_group) < number_fuel:
            x = random.randint(PLAYER_SPAWN_X + 100, WIDTH)
            y = random.randint(100, HEIGHT - 100)
            fuel = Gasoline(x, y, GASOLINE_WIDTH, GASOLINE_HEIGHT)
            fuel_group.add(fuel)