import pygame
from random import randrange
from pygame.locals import *


class Bullet(object):

    def __init__(self, parent, side):

        self.parent = parent
        if side == "right":
            self.rect = Rect(parent.rect.centerx+30, parent.rect.centery, 2, 4)
        elif side == "left":
            self.rect = Rect(parent.rect.centerx-32, parent.rect.centery, 2, 4)
        self.alive = True

    def draw(self, game_area):

        if self.alive:
            self.rect.move_ip(0, -8)
            """if self.rect.y < -20:
                del self"""
            pygame.draw.rect(game_area, (150, 242, 255), self.rect)


class Spaceship(object):

    def __init__(self, x, y):

        self.image = pygame.image.load("./img/ship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 40))
        self.heart = pygame.image.load("./img/heart.png").convert_alpha()
        self.blast = pygame.mixer.Sound("./sounds/laser.wav")

        self.font = pygame.font.SysFont("Arial", 40)


        # self.rect = Rect((x, y, 60, 30))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.velx = 0

        self.bullets = []
        self.cooldown = 0

        self.blast.set_volume(0.2)

        self.health = 5
        self.alive = True

        self.even = True

        self.score = 0

    def draw(self, game_area, sidebar):

        # Draw the player
        # pygame.draw.rect(game_area, (255, 255, 255), self.rect)
        game_area.blit(self.image, self.rect)
        for b in self.bullets:
            b.draw(game_area)

        # Draw the player's scoreboard part
        """x = 5
        for i in range(self.health):

            sidebar.blit(self.heart, (x, 200))
            x += 35"""

        sidebar.blit(self.font.render("x" + str(self.health), False, (0, 0, 0)), (75, 750))

    def shoot(self):

        self.cooldown = 15
        self.bullets.append(Bullet(self, "left"))
        self.bullets.append(Bullet(self, "right"))
        # self.blast.play(maxtime=166)

    def clean(self):

        if self.even:
            if len(self.bullets) > 30:
                self.bullets = self.bullets[20:]

            for b in self.bullets:

                if not b.alive:
                    self.bullets.remove(b)
        self.even = not self.even

    def move(self, height, width):

        k = pygame.key.get_pressed()

        if k[K_LEFT] and self.rect.left > 4:
            self.rect.move_ip(-8, 0)
        if k[K_RIGHT] and self.rect.right < width-4:
            self.rect.move_ip(8, 0)
        if k[K_SPACE] and self.cooldown == 0:
            self.shoot()

    def update(self, flying_objects):

        if self.cooldown > 0:
            self.cooldown -= 1

        self.move(height=800, width=800)
        self.clean()

        i = self.rect.collidelist([i.rect for i in flying_objects.asteroids])

        if i != -1 and flying_objects.asteroids[i].health > 0:
            if abs(self.rect.centerx - flying_objects.asteroids[i].rect.centerx) < 20 and abs(self.rect.centery - flying_objects.asteroids[i].rect.centery) < 20:
                self.health -= 1
                flying_objects.asteroids[i].health = 0

        if self.health < 0:
                self.alive = False


class Asteroid(object):

    def __init__(self):

        self.base_image = pygame.image.load("./img/asteroids/amed.png").convert_alpha()
        self.image = self.base_image
        self.rect = self.image.get_rect()
        # self.rect.x, self.rect.y = randrange(800), -30
        self.health = 2
        self.velx, self.vely = randrange(-2, 2), 3
        self.even = True
        self.rotation = 0

        self.rect.y = -100

        if self.velx < 0:
            self.rect.x = randrange(400, 1000)
        elif self.velx > 0:
            self.rect.x = randrange(-200, 400)
        else:
            self.rect.x = randrange(0, 800)

    def draw(self, game_area):

        game_area.blit(self.image, self.rect)

    def update(self, player):

        """if self.rotation <= 360:
            self.image = pygame.transform.rotate(self.base_image, self.rotation)
            self.rotation +=1
        else:
            self.rotation = 0"""

        if self.health > 0:

            if self.even:
                self.rect.move_ip(0, self.vely)
            else:
                self.rect.move_ip(self.velx, 0)

            # Collision detection
            if self.even:
                i = self.rect.collidelist([i.rect for i in player.bullets])
                if i != -1 and player.bullets[i].alive:
                    if (abs(self.rect.centerx - player.bullets[i].rect.centerx) < 20) and (abs(self.rect.centery - player.bullets[i].rect.centery)<20):
                        self.health -= 1
                        player.bullets[i].alive = False
                        player.score += 1

            self.even = not self.even


class FlyingObjects:

    def __init__(self, game_area, player):

        self.amount = 5
        self.asteroids = [Asteroid() for a in range(self.amount)]
        self.game_area = game_area
        self.player = player

    def update(self):

        for asteroid in self.asteroids:

            if asteroid.health <= 0:
                self.asteroids.remove(asteroid)
                self.asteroids.append(Asteroid())
            elif asteroid.rect.centerx < -30 or asteroid.rect.centerx > self.game_area.get_width()+30:
                self.asteroids.remove(asteroid)
                self.asteroids.append(Asteroid())
            elif asteroid.rect.top > self.game_area.get_height()+10:
                self.asteroids.remove(asteroid)
                self.asteroids.append(Asteroid())
            asteroid.update( self.player)

    def draw(self):

        for asteroid in self.asteroids:

            asteroid.draw(self.game_area)