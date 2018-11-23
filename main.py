import pygame
from classes import *
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()
width, height = 1000, 800

game_area = pygame.Surface((800, 800))
sidebar = pygame.Surface((200, 800))


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("SPACESHOOTER")
pygame.mouse.set_cursor(*pygame.cursors.arrow)

background = pygame.image.load("./img/back.png").convert()
player = Spaceship(width/2, height-50)

side_frame = pygame.image.load("./img/side_frame.png").convert_alpha()
side_frame = pygame.transform.rotate(side_frame, 90)
# sidebar = Rect(width-200, 0, 200, 800)

asteroids = [Asteroid(), Asteroid(), Asteroid(), Asteroid()]

clock = pygame.time.Clock()
state = "windowed"
p = True
running = True
while running:

    p = not p

    for e in pygame.event.get():
        if e.type == QUIT:
            running = False

    k = pygame.key.get_pressed()
    if k[K_ESCAPE]:
        running = False
    if k[K_w]:
        if state == "windowed":
            pygame.display.set_mode((width, height), FULLSCREEN)
            state = "fullscreen"
        elif state == "fullscreen":
            pygame.display.set_mode((width, height))
            state = "windowed"

    """ We reinitialise the screen """

    # screen.fill((0,0,0))
    game_area.blit(background, (0, 0))
    sidebar.fill(((224, 236, 255)))
    sidebar.blit(side_frame, (0,0))


    # Update the game

    [asteroid.update(game_area, player, p) for asteroid in asteroids]
    for asteroid in asteroids:
        if asteroid.rect.centerx not in range(-20, width+20) or asteroid.rect.y > height+20 or asteroid.health == 0:
            asteroids.remove(asteroid)
            asteroids.append(Asteroid())

    player.update(game_area, sidebar, p)

    # Draw the game

    """pygame.draw.rect(screen, (0, 0, 0), sidebar)
    pygame.draw.rect(screen, (255, 255, 255), sidebar, 5)"""

    screen.blit(game_area, (0, 0))
    screen.blit(sidebar, (800, 0))


    if p:
        parts = [(0, 0, 800, 800)]
    else:
        parts = [(0, 0, 800, 800), (800, 0, 200, 800)]

    pygame.display.update(parts)
    clock.tick(30)
    print(clock.get_fps())
