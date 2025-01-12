import textwrap
from datetime import datetime
from config import *
from utils import terminate, load_image, generate_obstacles, shake, generate_fuel

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("data/sound/game_sound.mp3")
problem_sound = pygame.mixer.Sound('data/sound/звуктревоги.mp3')

screen = pygame.display.set_mode(SIZE)
from sprites import Player, ObstacleTop, ObstacleBottom, Gasoline, Fish, BigFish
from sprites import parsed_dialog, character_images

def level1():
    frame_now = 0
    pygame.display.set_caption('Звездные войны. 1 эпизод')
    clock = pygame.time.Clock()
    BACKGROUND_IMAGE = load_image('background.jpg')
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    obstacles_group = pygame.sprite.Group()
    fuel_group = pygame.sprite.Group()
    fish_group = pygame.sprite.Group()
    big_fish_group = pygame.sprite.Group()
    Player.init_groups([all_sprites, player_group])
    Gasoline.init_groups([fuel_group, all_sprites])
    Player.obstacles_group = obstacles_group
    Player.fuel_group = fuel_group
    player = Player(PLAYER_SPAWN_X, PLAYER_SPAWN_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
    Fish.init_groups([fish_group])
    Fish.player = player
    fish = Fish(0, HEIGHT // 2, FISH_WIDTH, FISH_HEIGHT)
    BigFish.init_groups([big_fish_group])
    BigFish.target_fish = fish
    big_fish = BigFish(0, fish.rect.y, BIG_FISH_WIDTH, BIG_FISH_HEIGHT)

    # sound
    pygame.mixer.music.play()

    # Поверхность для затемнения экрана в начале
    alpha = 255  # максимально темно
    dark_surface = pygame.Surface(screen.get_size())
    dark_surface.fill(pygame.Color('black'))

    running = True

    while running:
        # тряска
        moved_x, moved_y = shake(player.shakes_start_time, player.shakes_end_time, player.shakes_intensity,
                                 player.time_game)
        screen.blit(BACKGROUND_IMAGE, (0 + moved_x, 0 + moved_y))

        if player.lives == 0:
            pygame.mixer.music.stop()
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        all_sprites.update()

        # Генерация препятствий
        if (not len(obstacles_group) or obstacles_group.sprites()[
            -1].rect.x < WIDTH - DISTANCE_BETWEEN_COLUMN) and player.time_game >= 7 and not (
                62 < player.time_game < 90) and not (player.time_game > 190):
            top, bottom = generate_obstacles(ObstacleTop, ObstacleBottom)
            obstacles_group.add(top, bottom)
            all_sprites.add(top, bottom)

        # Генерация бензоколонок
        generate_fuel(1, player, Gasoline, fuel_group)

        # Обновляем спрайты
        all_sprites.draw(screen)
        player.update()
        obstacles_group.update()

        frame_now += 1

        # Диалоги
        for dialog in parsed_dialog():
            if dialog['start'] <= player.time_game <= dialog['end']:
                lines = textwrap.wrap(dialog['text'], 40)
                rect_text = pygame.draw.rect(screen, pygame.Color('gray'), (50, HEIGHT - 120, WIDTH - 100, 100))
                screen.blit(character_images[dialog['character']], (60, rect_text.center[1] - 50))
                y = rect_text.top + 10
                for line in lines:
                    text = pygame.font.Font(None, 32).render(line, True, pygame.Color('white'))
                    screen.blit(text, (150, y))
                    y += 30
                break

        # Считаем время
        if frame_now % FPS == 0:
            player.time_game += 1
            player.gasoline_level -= 0.5
        font = pygame.font.Font(None, 32)
        time_text = font.render(f'Таймер: {player.time_game - 3} секунд', True, pygame.Color('black'))
        screen.blit(time_text, (50, 30))

        if 60 < player.time_game < 77:
            fish_group.draw(screen)
            fish_group.update()

        if 75 < player.time_game < 90:
            big_fish_group.draw(screen)
            big_fish_group.update()

            # add_to_db_sqlite(1, LIVES - player.lives, 'Всегда найдется рыба покрупнее', 'Рыбы дуреют с этой прикормки', 'data/img/карасики.png', str(datetime.now())[:-7], 'True') # Достижение



        # Подсчет point
        font = pygame.font.Font(None, 32)
        time_text = font.render(f'Poins: {int(player.point)}', True, pygame.Color('black'))
        screen.blit(time_text, (50, 60))

        # Подсчет попыток
        font = pygame.font.Font(None, 32)
        time_text = font.render(f'LIVES: {int(player.lives)}', True, pygame.Color('red'))
        screen.blit(time_text, (50, 90))

        # Подсчет бензина
        font = pygame.font.Font(None, 32)
        time_text = font.render(f'Бензин: {int(player.gasoline_level)}', True, pygame.Color('black'))
        screen.blit(time_text, (50, 120))

        # Приборы
        font = pygame.font.Font(None, 32)
        time_text = font.render(f'Глубина: {int(player.rect.y)}', True, pygame.Color('black'))
        screen.blit(time_text, (WIDTH - 200, 60))

        if 140 < player.time_game < 165:
            font = pygame.font.Font(None, 32)
            time_text = font.render(f'Неисправный мотор!', True, pygame.Color('yellow'))
            screen.blit(time_text, (WIDTH - 250, 90))
            problem_sound.set_volume(0.3)
            problem_sound.play()
        if player.time_game > 165:
            problem_sound.stop()

        if 55 < player.time_game < 60:
            font = pygame.font.Font(None, 25)
            time_text = font.render(f'РЫБА ГУБЕР СОВСЕМ БЛИЗКА', True, pygame.Color('RED'))
            time_text1 = font.render(f'ПРИГОТОВЬТЕСЬ К УСКОРЕНИЮ!(SHIFT)', True, pygame.Color('RED'))
            screen.blit(time_text, (WIDTH - 300, 90))
            screen.blit(time_text1, (WIDTH - 355, 120))

        if player.time_game > 196:
            player.gasoline_level = 0
            player.rect.x += 5
            player.rect.y -= 3

        if player.time_game > 199:
            pygame.mixer.music.stop()
            running = False

        if alpha > 0 and player.time_game >= 3:
            alpha -= 2
            dark_surface.set_alpha(alpha)
        # наложение темной поверхности
        screen.blit(dark_surface, (0, 0))


        pygame.display.flip()
        clock.tick(FPS)
    terminate()

level1()