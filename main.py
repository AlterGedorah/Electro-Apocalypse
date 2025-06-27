import pygame
import sys
from settings import Settings
from level import Level
from debug import debug
from ui import UI


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(32)

        # ✅ Play background music
        self.play_background_music()

        # Game over sound
        if not hasattr(Game, 'game_over_sound'):
            Game.game_over_sound = pygame.mixer.Sound("sounds/8-bit-game-over-sound-effect-331435.mp3")
        self.game_over_sound = Game.game_over_sound
        self.game_over_played = False

        # Initialize settings
        self.settings = Settings()
        self.clock = pygame.time.Clock()

        # Screen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Lost Wizard")

        # Level
        self.level = Level()
        self.game_over = False

        # Fonts/UI
        self.font = pygame.font.Font(None, 80)
        self.title = self.font.render("Lost Wizard", True, (255, 255, 255))
        self.start_text = self.font.render("Press ENTER to Start", True, (200, 200, 200))
    def play_background_music(self):
        music_path = "sounds/exploration-chiptune-rpg-adventure-theme-336428.mp3"
        if not hasattr(self, '_current_music') or self._current_music != music_path:
            pygame.mixer.music.load(music_path)
            self._current_music = music_path
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def show_game_over(self):
        bg = pygame.image.load('assets/images/game_over.png').convert()
        bg = pygame.transform.scale(bg, (self.settings.screen_width, self.settings.screen_height))
        self.screen.blit(bg, (0, 0))

        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        font_path = r'assets/fonts/Pixeltype.ttf'
        try:
            font = pygame.font.Font(font_path, 100)
        except FileNotFoundError:
            font = pygame.font.Font(None, 100)

        text = font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(
            text,
            (
                self.settings.screen_width // 2 - text.get_width() // 2,
                self.settings.screen_height // 2 - text.get_height() // 2 - 50,
            ),
        )

        small_font = pygame.font.Font(font_path, 50)
        instr = small_font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
        self.screen.blit(
            instr,
            (
                self.settings.screen_width // 2 - instr.get_width() // 2,
                self.settings.screen_height // 2 + text.get_height() // 2,
            ),
        )

        pygame.display.flip()

    def run_game(self):
        while True:
            dt = self.clock.tick(self.settings.fps) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if self.game_over and event.key == pygame.K_r:
                        self.level = Level()
                        self.game_over = False
                        self.game_over_played = False
                        self.play_background_music()

            # Game over check
            if self.level.player.health <= 0:
                if not self.game_over_played:
                    pygame.mixer.music.stop()
                    pygame.mixer.stop()
                    self.game_over_sound.play()
                    self.game_over_played = True
                self.game_over = True

            if self.game_over:
                self.show_game_over()
                continue
                
            # Game loop drawing
            if not hasattr(self, '_cached_bg') or self._cached_bg is None:
                bg = pygame.image.load('assets/images/game_over.png').convert()
                bg = pygame.transform.scale(bg, (self.settings.screen_width, self.settings.screen_height))
                self._cached_bg = bg
            self.screen.blit(self._cached_bg, (0, 0))
            self.level.run(dt)
            pygame.display.flip()

    def main_menu(self):
        bg = pygame.image.load('assets/images/game_over.png').convert()
        bg = pygame.transform.scale(bg, (self.settings.screen_width, self.settings.screen_height))

        font_path = r'assets/fonts/Pixeltype.ttf'
        try:
            font = pygame.font.Font(font_path, 80)
        except FileNotFoundError:
            font = pygame.font.Font(None, 80)

        title = font.render("Lost Wizard", True, (255, 255, 255))
        start_text = font.render("Press ENTER to Start", True, (200, 200, 200))
        quit_text = font.render("Press Q to Quit", True, (200, 200, 200))

        while True:
            self.screen.blit(bg, (0, 0))
            self.screen.blit(title, (self.settings.screen_width // 2 - title.get_width() // 2, 200))
            self.screen.blit(start_text, (self.settings.screen_width // 2 - start_text.get_width() // 2, 400))
            self.screen.blit(quit_text, (self.settings.screen_width // 2 - quit_text.get_width() // 2, 500))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.main_menu()
    game.run_game()
