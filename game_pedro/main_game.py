import pygame
import sys
from time import sleep
from spacecraft import Spacecraft
from settings import Settings
from bullets import Bullet
from aliens import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class Game:

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        # Define tela do jogo
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Invasão Alien")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.spacecraft = Spacecraft(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._game_sounds()

        pygame.mixer.music.load('sounds/background_music.wav')
        pygame.mixer.music.play(-1)

        self._create_fleet()

        self.play_button = Button(self, "Play")

    def run(self):
        """Loop principal do jogo"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.spacecraft.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _game_sounds(self):

        # Sons de ação do jogo
        self.alien_hit_sound = pygame.mixer.Sound('sounds/alien_hit.wav')
        self.spacecraft_hit_sound = pygame.mixer.Sound('sounds/spacecraft_hit.wav')
        self.bullet_shoot_sound = pygame.mixer.Sound('sounds/spacecraft_shoot.wav')
        self.level_up_sound = pygame.mixer.Sound('sounds/level_up.mp3')

    def _check_events(self):
        """Recebe os eventos vindo do teclado"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_events_keydown(event)

            elif event.type == pygame.KEYUP:
                self._check_events_keyup(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            self.settings.iniatialize_dynamic_settings()

            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_spacecraft()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.spacecraft.center_spacecraft()

            pygame.mouse.set_visible(False)

    def _check_events_keydown(self, event):
        if event.key == pygame.K_w:
            self.spacecraft.moving_up = True

        elif event.key == pygame.K_s:
            self.spacecraft.moving_down = True

        elif event.key == pygame.K_d:
            self.spacecraft.moving_right = True

        elif event.key == pygame.K_a:
            self.spacecraft.moving_left = True

        elif event.key == pygame.K_SPACE:
            self._fire_bullets()

    def _check_events_keyup(self, event):
        if event.key == pygame.K_w:
            self.spacecraft.moving_up = False

        elif event.key == pygame.K_s:
            self.spacecraft.moving_down = False

        elif event.key == pygame.K_d:
            self.spacecraft.moving_right = False

        elif event.key == pygame.K_a:
            self.spacecraft.moving_left = False

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        avaiable_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = avaiable_space_x // (2 * alien_width)

        spacecraft_height = self.spacecraft.rect.height
        avaiable_space_y = (self.settings.screen_height - (3 * alien_height) - spacecraft_height)
        number_rows = avaiable_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.spacecraft, self.aliens):
            self._spacecraft_hit()

        self._check_aliens_bottom()

    def _spacecraft_hit(self):
        if self.stats.spacecraft_left > 0:
            self.spacecraft_hit_sound.play()

            self.stats.spacecraft_left -= 1
            self.sb.prep_spacecraft()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.spacecraft.center_spacecraft()

            sleep(1)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._spacecraft_hit()
                break

    def _fire_bullets(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullet_shoot_sound.play()
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            self.alien_hit_sound.play()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

            self.stats.level += 1
            self.settings.increase_speed()
            self.sb.prep_level()
            self.level_up_sound.play()

    def _update_screen(self):
        self.screen.fill(self.settings.background_color)
        self.spacecraft.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()