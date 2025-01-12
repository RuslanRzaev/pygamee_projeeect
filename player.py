from config import *
from enemy import Enemy
from explosion import Explosion
from ship import Ship


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.explosion = None
        self.kill_count = 0

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                try:
                    for obj in objs:
                        if laser.collision(obj):
                            obj.health -= 10
                            if obj.health == 0:
                                self.explosion = Explosion(obj.x, obj.y)
                                if isinstance(obj, Enemy):
                                    self.kill_count += 1
                                objs.remove(obj)
                            if laser in self.lasers:
                                self.lasers.remove(laser)
                except TypeError:
                    if laser.collision(objs):
                        objs.health -= 10
                        if objs.health <= 0:
                            objs.alive = False
                            self.explosion = Explosion(500, 100)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
