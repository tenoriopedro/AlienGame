class Settings:
    def __init__(self):
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.background_color = (245, 245, 245)

        # Spacecraft settings
        self.spacecraft_limit = 3
        self.spacecraft_speed = None

        # Bullet settings
        self.bullet_speed = None
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_width = 50
        self.alien_height = 50
        self.fleet_drop_speed = 20
        self.alien_speed = None

        # Game speed
        self.speedup_scale = 1.2

        self.alien_points = 50

        self.fleet_direction = None

        self.iniatialize_dynamic_settings()

    def iniatialize_dynamic_settings(self):
        # Defines settings that change during gameplay
        self.bullet_speed = 5
        self.alien_speed = 2
        self.spacecraft_speed = 6

        self.fleet_direction = 1

    def increase_speed(self):
        # Increases game speed during gameplay
        self.spacecraft_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
