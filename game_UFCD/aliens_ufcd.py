import pygame
from pygame.sprite import Sprite
from pathlib import Path

ROOT_IMAGE = Path(__file__).parent / "files" / "image_alien_1.png"


class Alien(Sprite):

    def __init__(self, game):

        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(ROOT_IMAGE)
        self.image = pygame.transform.scale(
            self.image, (self.settings.alien_width, self.settings.alien_height)
        )
        self.rect = self.image.get_rect()

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        self.y = self.rect.y + (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.y = self.y

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom or self.rect.top <= 40:
            return True