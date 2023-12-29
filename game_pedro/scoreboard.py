import pygame.font
from pygame.sprite import Group
from spacecraft import Spacecraft


class Scoreboard:
    def __init__(self, game):

        self.score_rect = None
        self.high_score_rect = None
        self.score_image = None
        self.high_score_image = None
        self.level_rect = None
        self.level_image = None
        self.spacecrafts = None
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 30)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_spacecraft()

    def prep_spacecraft(self):
        self.spacecrafts = Group()
        for spacecraft_number in range(self.stats.spacecraft_left):
            spacecraft = Spacecraft(self.game)
            spacecraft.rect.x = 10 + spacecraft_number * spacecraft.rect.width
            spacecraft.rect.y = 10
            self.spacecrafts.add(spacecraft)

    def prep_level(self):
        level_str = f'Level: {self.stats.level}'
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.background_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom 

    def prep_high_score(self):
        high_score_str = f'high score: {self.stats.high_score:,}'.replace(',', '.')
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.background_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_score(self):
        score_str = f'score: {self.stats.score:,}'.replace(',', '.')
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.background_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.score_rect.right + 650
        self.score_rect.top = 10

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.spacecrafts.draw(self.screen)

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
