import pygame
from pathlib import Path
from pygame.sprite import Sprite

IMAGE_SPACECRAFT = Path(__file__).parent / "files" / "spacecraft.png"


class Spacecraft(Sprite):
    """ Class to manage the spaceship """

    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = game.screen.get_rect()

        # Load ship image
        self.image = pygame.image.load(IMAGE_SPACECRAFT)
        self.image = pygame.transform.scale(
            self.image, 
            (40, 40)
        )
        self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()

        # Positioning the ship on the game screen
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)

        self.moving_up = False
        self.moving_down = False

    def update(self):
        # Moving the ship vertically
        if self.moving_up and self.rect.top > 41:
            self.y -= self.settings.spacecraft_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.spacecraft_speed

        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_spacecraft(self):
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)
