import math

import pygame.display

import utils
from level2_objs.asteroid_ import Asteroid
from level2_objs.enemy import Enemy
from level2_objs.explosion import Explosion
from level2_objs.player import Player
from level2_objs.space_station import SpaceStation
from utils import *

pygame.font.init()


class Scene2:
    def __init__(self, lives, window, current_attempt):
        self.con = sqlite3.connect("db/game.db")
        self.lives = lives
        self.success = False
        self.current_attempt = current_attempt
        self.window = window

    def gameplay(self):
        pygame.display.set_caption('Звездные войны. I эпизод: Космическое сражение')
        BG_MUSIC_BATTLE.play(-1)

        showed_ship_a = False

        run = True

        lives = self.lives
        time_point = TIME_POINT
        b = False

        enemies_count = 10
        enemies_cnt_nc = 10
        enemies = []
        enemies_vel = 2
        timer_enemy = 0

        asteroids = []
        asteroid_vel = 2

        player_vel = 6
        laser_vel = 13

        player = Player(300, 610)
        space_station = SpaceStation(WIDTH // 2 - 250, -700)

        title1 = "Восход Скайуокера"
        desc1 = "Все вражеские корабли уничтожены"

        title2 = "Неуловимый Татуинец"
        desc2 = "Не потеряно ни одной жизни"

        achievement_ships = Achievement(1100, 100, ACHIEVEMENT_BG, title1, desc1, ACHIEVEMENT_3_1)
        achievement_health = Achievement(1100, 100, ACHIEVEMENT_BG, title2, desc2, ACHIEVEMENT_3_1)

        clock = pygame.time.Clock()

        final = False
        result = False

        time_expl_count = 60

        bg_height = BG.get_height()

        bg = pygame.transform.scale(BG, (WIDTH, bg_height))

        scroll = 0
        panels = math.ceil(HEIGHT / bg_height) + 2

        explosion_group = pygame.sprite.Group()

        while run:

            clock.tick(FPS)
            timer_enemy += 1
            if lives <= 0:
                result = False
                BG_MUSIC_BATTLE.stop()
                final = True

            for i in range(panels):
                self.window.blit(bg, (0, i * bg_height + scroll - bg_height))

            # draw text
            lives_label = REGULAR_FONT.render(f"Жизни: {lives}", 1, (255, 255, 255))
            kill_count_label = REGULAR_FONT.render(f"Счёт врагов: {player.kill_count}/{enemies_cnt_nc}", 1,
                                                   (255, 255, 255))

            self.window.blit(lives_label, (10, 10))
            self.window.blit(kill_count_label, (10, 50))

            if timer_enemy == 200 and enemies_count > 0:
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                              random.choice(["advanced", "interceptor", "assault"]))
                enemies.append(enemy)
                timer_enemy = 0
                enemies_count -= 1

            for enemy in enemies:
                enemy.draw(self.window)

            for asteroid in asteroids:
                asteroid.draw(self.window)

            player.draw(self.window)

            if final:
                check_rect = pygame.Rect(WIDTH / 2 - TEXT_NEXT.get_width() / 2, 550, TEXT_NEXT.get_width(),
                                         TEXT_NEXT.get_height())
                BG_MUSIC_BATTLE.stop()
                if result:
                    VICTORY_SOUND.play()
                else:
                    LOST_SOUND.play()
                if not showed_ship_a:
                    utils.add_to_db_sqlite(2, self.current_attempt, title1, desc1, 'icon_3_1.png',
                                           str(datetime.now())[:-7],
                                           0)
                self.success = result
                pause = True
                used_lives = self.lives - lives
                self.lives = lives
                showed_health_a = False
                alpha = -10
                count = 0

                while pause:
                    count += 1
                    win_bg = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA).convert()
                    if used_lives == 0:
                        if not showed_health_a:
                            achievement_health.draw_n_move(self.window, 15)
                            utils.add_to_db_sqlite(2, self.current_attempt, title2, desc2, 'icon_3_1.png',
                                                   str(datetime.now())[:-7],
                                                   1)
                            showed_health_a = True
                        achievement_health.draw_n_move(self.window, 15)
                    else:
                        if not showed_health_a:
                            achievement_health.draw_n_move(self.window, 15)
                            utils.add_to_db_sqlite(2, self.current_attempt, title2, desc2, 'icon_3_1.png',
                                                   str(datetime.now())[:-7],
                                                   0)
                            showed_health_a = True

                    if result:
                        win_bg.fill((0, 0, 53))
                        label = BIG_FONT.render(f"Вы победили!!!", True, (255, 255, 255))
                    else:
                        win_bg.fill((52, 14, 16))
                        label = BIG_FONT.render(f"Вы проиграли!!!", True, (255, 255, 255))
                    if alpha <= 70:
                        alpha += 0.1
                    win_bg.set_alpha(alpha)
                    self.window.blit(win_bg, (0, 0))
                    self.window.blit(label, (WIDTH / 2 - label.get_width() / 2, 250))

                    label1 = BIG_FONT.render(f"Уничтоженные враги: {player.kill_count + 1}", 1, (255, 255, 255))
                    label2 = BIG_FONT.render(f"Использованные жизни: {used_lives}", 1, (255, 255, 255))

                    self.window.blit(label1, (WIDTH / 2 - label1.get_width() / 2, 320))

                    self.window.blit(label2, (WIDTH / 2 - label2.get_width() / 2, 390))

                    self.window.blit(TEXT_NEXT, (WIDTH / 2 - TEXT_NEXT.get_width() / 2, 550))

                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if check_rect.collidepoint(pygame.mouse.get_pos()):
                                if result:
                                    VICTORY_SOUND.stop()
                                else:
                                    LOST_SOUND.stop()
                                pause = False
                        if event.type == pygame.QUIT:
                            pause = False
                            if result:
                                VICTORY_SOUND.stop()
                            else:
                                LOST_SOUND.stop()
                    pygame.display.flip()

            # space station
            if b:
                space_station.draw(self.window)
                space_station.move(1)

            scroll += 5

            if time_point <= 0:
                b = True

            if abs(scroll) > bg_height:
                scroll = 0

            time_point -= 1

            if player.health <= 0:
                lives -= 1
                player.health = player.max_health

            if final:
                run = False

            # achievement_ships
            if len(enemies) == 0 and timer_enemy >= 200:
                if not showed_ship_a:
                    utils.add_to_db_sqlite(2, self.current_attempt, title1, desc1, 'icon_3_1.png',
                                           str(datetime.now())[:-7],
                                           1)
                    showed_ship_a = True
                achievement_ships.draw_n_move(self.window, 15)

            if len(asteroids) == 0:
                for i in range(10):
                    asteroid = Asteroid(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100))
                    asteroids.append(asteroid)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            keys = pygame.key.get_pressed()
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.x - player_vel > 0:  # left
                player.x -= player_vel
            if (keys[pygame.K_d] or keys[
                pygame.K_RIGHT]) and player.x + player_vel + player.get_width() < WIDTH:  # right
                player.x += player_vel

            if keys[pygame.K_SPACE]:
                # sound player
                PLAYER_LASER_SOUND.play()

                player.shoot()

            for enemy in enemies[:]:
                enemy.move(enemies_vel)
                enemy.move_lasers(laser_vel, player)

                if random.randrange(0, 2 * 60) == 1 and (30 <= enemy.y <= HEIGHT):
                    # sound enemy
                    ENEMY_LASER_SOUND.play()

                    enemy.shoot()

                if collide(enemy, player):
                    player.health -= 10
                    player.kill_count += 1
                    ENEMY_BOOM_SOUND.play()
                    expl = Explosion(enemy.x, enemy.y)
                    explosion_group.add(expl)
                    enemies.remove(enemy)

            for asteroid in asteroids[:]:
                asteroid.move(asteroid_vel)

                if collide(asteroid, player):
                    player.health -= 5
                    ASTEROID_BOOM_SOUND.play()
                    expl = Explosion(asteroid.x, asteroid.y)
                    explosion_group.add(expl)
                    asteroids.remove(asteroid)

            player.move_lasers(-laser_vel, enemies)
            if space_station.y >= -270:
                player.move_lasers(-laser_vel, space_station)
            player.move_lasers(-laser_vel, asteroids)
            explosion_group.draw(self.window)
            explosion_group.update()
            if player.explosion is not None:
                ENEMY_BOOM_SOUND.play()
                explosion_group.add(player.explosion)
                player.explosion = None
            if not space_station.alive:
                space_station.rect_red = pygame.draw.rect(self.window, (255, 0, 0), (0, 0, 0, 0))
                space_station.x = 0
                space_station.y = 2000
                space_station.draw(self.window)

                result = True
                if time_expl_count > 0:
                    ENEMY_BOOM_SOUND.play()
                    time_expl_count -= 1
                elif time_expl_count <= 0:
                    BG_MUSIC_BATTLE.stop()
                    final = True
            pygame.display.flip()
