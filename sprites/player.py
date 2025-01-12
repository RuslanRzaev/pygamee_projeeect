from config import *
from utils import load_image
from sprites import GameSprite

pygame.mixer.init()
crashed_sound = pygame.mixer.Sound('data/sound/звукудара.mp3')


class Player(GameSprite):
    obstacles_group = pygame.sprite.Group()
    fuel_group = pygame.sprite.Group()
    def __init__(self, x, y, width, height):
        self.IMAGE = pygame.transform.smoothscale(load_image('player2.png'), (width, height))
        super().__init__(x, y, width, height)
        self._lives = LIVES
        self.point = 3
        self.shakes_start_time = 3
        self.shakes_end_time = 7
        self.shakes_intensity = 3
        self.gravity = 0.25 # гравитация
        self.jump_f = -2 # сила прыжка
        self.time_game = 195
        self._gasoline_level = 100
        self.speed_y = 0

    @property
    def gasoline_level(self):
        return self._gasoline_level

    @gasoline_level.setter
    def gasoline_level(self, value):
        self._gasoline_level = value
        if self._gasoline_level > 100:
            self._gasoline_level = 100
        elif self._gasoline_level < 0:
            self._gasoline_level = 0

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value):
        self._lives = value
        if self._lives < 0:
            self._lives = 0

    def update(self):
        if pygame.key.get_mods() & pygame.KMOD_SHIFT and self.gasoline_level:
            self.gravity = 5
            self.jump_f = -3
            self.rect.x += 5
            self.gasoline_level -= 0.02
            if self.rect.x > 250:
                self.rect.x = 250
        else:
            self.gravity = 0.25
            self.jump_f = -2
            self.rect.x -= 5
            if self.rect.x < PLAYER_SPAWN_X:
                self.rect.x = PLAYER_SPAWN_X


        self.rect.y += self.speed_y
        self.speed_y += self.gravity
        self.speed_y = min(self.speed_y, MAX_FALL_SPEED)

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.jump()

        # Проверка на столкновения по пикселям(с препятствиями)
        for obstacle in self.obstacles_group:
            if not obstacle.passed_or_not and pygame.sprite.collide_mask(self, obstacle):
                self.lives -= 1

                self.shakes_start_time = self.time_game
                self.shakes_end_time = self.time_game + 1

                # Эффект удара(звук)
                crashed_sound.set_volume(1)
                crashed_sound.play()

                obstacle.passed_or_not = True
            if not obstacle.passed_or_not and self.rect.right > obstacle.rect.right:
                obstacle.passed_or_not = True
                self.point += 0.5  # по 0.5 для каждого

        # Проверка на столкновения по пикселям(с топливом)
        for fuel in self.fuel_group:
            if pygame.sprite.collide_mask(self, fuel):
                self.gasoline_level += 50
                fuel.kill()

    def jump(self):
        if self._gasoline_level:
            self.speed_y = self.jump_f

