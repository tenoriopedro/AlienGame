class GameStats:

    def __init__(self, game):
        self.level = None
        self.score = None
        self.spacecraft_left = None
        self.settings = game.settings
        self.reset_stats()

        self.game_active = False

        self.high_score = 0

    def reset_stats(self):

        self.spacecraft_left = self.settings.spacecraft_limit
        self.score = 0
        self.level = 1
