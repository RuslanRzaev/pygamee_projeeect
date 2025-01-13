from level1_sprites import *
from utils import *
from config import *

pygame.init()

class Scene1:
    def __init__(self, lives, window):
        self.con = sqlite3.connect("db/game.db")
        self.lives = lives
        self.success = False
        len_db = self.con.execute("select count(*) from level3").fetchone()
        self.current_attempt = len_db[0]
        self.window = window
        pygame.mixer.init()
        pygame.mixer.music.load("data/sound/game_sound.mp3")
        self.problem_sound = pygame.mixer.Sound('data/sound/звуктревоги.mp3')

    def level1_gameplay(self):
        shakes_start_time = 3
        shakes_end_time = 7
        shakes_intensity = 3
        TIME_GAME = 60
        font = pygame.font.Font(None, 32)
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
        dark_surface = pygame.Surface(self.window.get_size())
        dark_surface.fill(pygame.Color('black'))

        running = True

        while running:
            frame_now += 1
            # тряска
            shakes(shakes_start_time, shakes_end_time, shakes_intensity, TIME_GAME, self.window, BACKGROUND_IMAGE)

            if player.point >= 4:
                pygame.mixer.music.stop()
                running = False

            if player.lives == 0:
                pygame.mixer.music.stop()
                running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == PLAYER_HIT:
                    shakes_start_time = TIME_GAME
                    shakes_end_time = TIME_GAME + 2
                elif event.type == GAME_STOP:
                    pygame.mixer.music.stop()
                    running = False

            all_sprites.update()

            # Генерируем препяствия
            generate_obsracled(obstacles_group, TIME_GAME, ObstacleTop, ObstacleBottom, all_sprites)

            # Генерация бензоколонок
            generate_fuel(TIME_GAME, 1, player, Gasoline, fuel_group)

            # Обновляем спрайты
            all_sprites.draw(self.window)
            player.update()
            obstacles_group.update()

            # Диалоги
            generate_dialogs(TIME_GAME, self.window)

            # Выводим приборы:
            show_devices(self.window, player, font)

            # Тайминги
            timings(self.window, self.problem_sound, TIME_GAME, fish_group, big_fish_group, font, player)

            # Считаем время
            if frame_now % FPS == 0:
                TIME_GAME += 1
                player.gasoline_level -= 0.5  # расходуем бензин

            if alpha > 0 and TIME_GAME >= 3:
                alpha -= 2
                dark_surface.set_alpha(alpha)

            # наложение темной поверхности
            self.window.blit(dark_surface, (0, 0))

            pygame.display.flip()
            clock.tick(FPS)
        self.lives = player.lives
