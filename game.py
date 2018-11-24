import pygame
from pygame.locals import *
from classes import *

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()


class Game:

    def __init__(self):

        self.running = True

        self.state = "running"

        self.width, self.height = 1000, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Space shooter")
        pygame.display.set_icon(pygame.image.load("./img/ship.png"))
        self.player = Spaceship((self.width-200)/2 - 35, self.height - 50)

        self.clock = pygame.time.Clock()

        self.game_area = pygame.Surface((800, 800))
        self.background = pygame.image.load("./img/back.png").convert()
        # self.background = pygame.transform.scale(self.background, (800, 800))

        self.sidebar_base = pygame.Surface((200, 800))
        self.side_frame = Rect(0, 0, 200, 800)
        self.sidebar_base.fill((157, 166, 181))
        # self.sidebar_base.fill((255, 255, 255))
        pygame.draw.rect(self.sidebar_base, (255, 255, 255), self.side_frame, 5)
        self.sidebar_base.blit(self.player.image, (65, 700))

        self.sidebar = pygame.Surface((200, 800))

        self.flying_objects = FlyingObjects(self.game_area, self.player)

    def update(self):

        self.player.update(self.flying_objects)
        self.flying_objects.update()

        if not self.player.alive:
            self.state = "gameover"

    def draw(self):

        # Reset the screen
        self.game_area.blit(self.background, (0, 0))
        self.sidebar.blit(self.sidebar_base, (0, 0))

        # Draw elements onto the screen
        self.player.draw(self.game_area, self.sidebar)
        self.flying_objects.draw()

        # Blit the two areas to the screen
        self.screen.blit(self.game_area, (0, 0))
        self.screen.blit(self.sidebar, (800, 0))

        # Render the final image
        pygame.display.update()

    def main(self):
        """This is the game's main loop
        It calls all the necessary functions
        All is wrapped into a class to improve readability
        """
        while self.running:

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

            if self.state == "running":
                self.update()
                self.draw()


            elif self.state == "gameover":
                self.screen.fill((0,0,0))
                pygame.display.update()

            self.clock.tick(60)
game = Game()

game.main()
