import pygame.font


class Button:
    def __init__(self, game, msg):

        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.widht, self.height = 200, 50
        self.button_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(
            0, 
            0, 
            self.widht, 
            self.height
            )
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        # Render the text
        self.msg_image = self.font.render(
            msg, 
            True, 
            self.text_color, 
            self.button_color
        )
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw button and message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)