import math
import pygame.display
import utils
from level3_objs.asteroid_ import Asteroid
from level3_objs.enemy import Enemy
from level3_objs.explosion import Explosion
from level3_objs.player import Player
from level3_objs.space_station import SpaceStation
from utils import *

pygame.font.init()

class Scene3:
    def __init__(self, lives, window, current_attempt):
        self.con = sqlite3.connect("db/game.db")
        self.lives = lives
        self.success = False
        self.current_attempt = current_attempt
        self.window = window

    def gameplay(self):
        BG_MUSIC_BATTLE.play(-1)

        showed_ship_a = False

        run = True

        lives = self.lives
        time_point = TIME_POINT
        b = False

        enemies = []
        enemies_vel = 2
        enemies_count = 1

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

        time_count = 0
        time_expl_count = 60

        bg_height = BG.get_height()

        bg = pygame.transform.scale(BG, (WIDTH, bg_height))

        scroll = 0
        panels = math.ceil(HEIGHT / bg_height) + 2

        explosion_group = pygame.sprite.Group()

        for i in range(enemies_count):
            enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                          random.choice(["advanced", "interceptor", "assault"]))
            enemies.append(enemy)

        while run:

            clock.tick(FPS)
            if lives <= 0:
                result = False
                BG_MUSIC_BATTLE.stop()
                final = True

            for i in range(panels):
                self.window.blit(bg, (0, i * bg_height + scroll - bg_height))

            # draw text
            lives_label = MAIN_FONT.render(f"Lives: {lives}", 1, (255, 255, 255))

            self.window.blit(lives_label, (10, 10))

            for enemy in enemies:
                enemy.draw(self.window)

            for asteroid in asteroids:
                asteroid.draw(self.window)

            player.draw(self.window)


            if final:
                BG_MUSIC_BATTLE.stop()
                if result:
                    VICTORY_SOUND.play()
                else:
                    LOST_SOUND.play()
                if not showed_ship_a:
                    utils.add_to_db_sqlite(3, self.current_attempt, title1, desc1, 'icon_3_1.png',
                                       str(datetime.now())[:-7],
                                       0)
                self.success = result
                pause = True
                used_lives = self.lives - lives
                self.lives = lives
                showed_health_a = False
                alpha = -10

                while pause:
                    win_bg = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA).convert()
                    if used_lives == 0:
                        if not showed_health_a:
                            achievement_health.draw_n_move(self.window, 10)
                            utils.add_to_db_sqlite(3, self.current_attempt, title2, desc2, 'icon_3_1.png',
                                                   str(datetime.now())[:-7],
                                                   1 if self.success else 0)
                            showed_health_a = True
                        if achievement_health.x <= 1000:
                            achievement_health.draw_n_move(self.window, 10)


                    if result:
                        win_bg.fill((2, 62, 198))
                    else:
                        win_bg.fill((52, 14, 16))
                    if alpha <= 60:
                        alpha += 0.1
                    win_bg.set_alpha(alpha)
                    self.window.blit(win_bg, (0, 0))
                    self.window.blit(BUTTON_NEXT, (WIDTH / 2 - BUTTON_NEXT.get_width() / 2, 550))
                    if result:
                        label = LOST_FONT.render(f"You Won!!!", True, (255, 255, 255))
                        self.window.blit(label, (WIDTH / 2 - label.get_width() / 2, 250))

                    else:
                        label = LOST_FONT.render(f"You Lost!!!", True, (255, 255, 255))
                        self.window.blit(label, (WIDTH / 2 - label.get_width() / 2, 250))

                    label1 = LOST_FONT.render(f"Kill count: {player.kill_count + 1}", 1, (255, 255, 255))
                    label2 = LOST_FONT.render(f"Lives used: {used_lives}", 1, (255, 255, 255))
                    label3 = LOST_FONT.render(f"Time count: {time_count / 60:.2f} seconds", 1, (255, 255, 255))

                    self.window.blit(label1, (WIDTH / 2 - label1.get_width() / 2, 320))

                    self.window.blit(label2, (WIDTH / 2 - label2.get_width() / 2, 390))

                    self.window.blit(label3, (WIDTH / 2 - label3.get_width() / 2, 460))
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
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

            space_station.move(0.7)

            time_count += 1
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
            if player.kill_count == enemies_count:
                if not showed_ship_a:
                    utils.add_to_db_sqlite(3, self.current_attempt, title1, desc1, 'icon_3_1.png', str(datetime.now())[:-7],
                                     1)
                    showed_ship_a = True
                achievement_ships.draw_n_move(self.window, 10)

            if len(asteroids) == 0:
                for i in range(10):
                    asteroid = Asteroid(random.randrange(50, WIDTH-100), random.randrange(-1500, -100))
                    asteroids.append(asteroid)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            keys = pygame.key.get_pressed()
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.x - player_vel > 0: # left
                player.x -= player_vel
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.x + player_vel + player.get_width() < WIDTH: # right
                player.x += player_vel

            if keys[pygame.K_SPACE]:
                # sound player
                PLAYER_LASER_SOUND.play()

                player.shoot()

            for enemy in enemies[:]:
                enemy.move(enemies_vel)
                enemy.move_lasers(laser_vel, player)

                if random.randrange(0, 2*60) == 1 and (30 <= enemy.y <= HEIGHT):
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
                    player.health -= 10
                    ASTEROID_BOOM_SOUND.play()
                    expl = Explosion(asteroid.x, asteroid.y)
                    explosion_group.add(expl)
                    asteroids.remove(asteroid)

            player.move_lasers(-laser_vel, enemies)
            if space_station.y >= -400:
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
