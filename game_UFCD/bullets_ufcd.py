import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Classe para os disparos da nave espacial"""

    def __init__(self, game):
        super().__init__()

        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )

        self.rect.midright = game.spacecraft.rect.midright

        self.x = float(self.rect.x)
        self.color = self.settings.bullet_color
        self.speed_factor = self.settings.bullet_speed

    def update(self):
        self.x += self.speed_factor
        self.rect.x = self.x

    def draw_bullet(self):
        """Desenha a projetil na tela"""
        pygame.draw.rect(self.screen, self.color, self.rect)