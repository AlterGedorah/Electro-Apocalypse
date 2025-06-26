import pygame
import sys
from settings import Settings
from level import Level
from debug import debug
from ui import UI


class Game:
    def __init__(self):
        pygame.init()

        # Initialize settings
        self.settings = Settings()

        # Set up the time clock
        self.clock = pygame.time.Clock()

        # Set up the screen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Electro Apocalypse")

        # Create the level
        self.level = Level()
        self.game_over = False

        # Load fonts and UI elements
        font = pygame.font.Font(None, 80)
        self.title = font.render("Mage.", True, (255, 255, 255))
        self.start_text = font.render("Press ENTER to Start", True, (200, 200, 200))
        self.quit_text = font.render("Press Q to Quit", True, (200, 200, 200))

    def show_game_over(self):
        # Load and draw the background image
        bg = pygame.image.load('assets/images/game_over.png').convert()
        bg = pygame.transform.scale(bg, (self.settings.screen_width, self.settings.screen_height))
        self.screen.blit(bg, (0, 0))

        # Overlay semi-transparent black
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Draw "GAME OVER"
        font = pygame.font.Font(None, 100)
        text = font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(
            text,
            (
                self.settings.screen_width // 2 - text.get_width() // 2,
                self.settings.screen_height // 2 - text.get_height() // 2 - 50,
            ),
        )

        # Draw instructions
        small_font = pygame.font.Font(None, 50)
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
                        self.main_menu()  # Go back to menu before restarting

            # Check for game over
            if self.level.player.health <= 0:
                self.game_over = True

            if self.game_over:
                self.show_game_over()
                continue

            # Draw background image in game loop
            bg = pygame.image.load('assets\images\game_over.png').convert()
            bg = pygame.transform.scale(bg, (self.settings.screen_width, self.settings.screen_height))
            self.screen.blit(bg, (0, 0))
            self.level.run()
            pygame.display.flip()

    def main_menu(self):
        # Load and scale the background image
        bg = pygame.image.load('assets/images/game_over.png').convert()
        bg = pygame.transform.scale(bg, (self.settings.screen_width, self.settings.screen_height))

        # Use a custom font file (e.g., 'assets/fonts/YourFont.ttf')
        font_path = 'assets\fonts\Pixeltype.ttf'
        try:
            font = pygame.font.Font(font_path, 80)
        except FileNotFoundError:
            font = pygame.font.Font(None, 80)  # Fallback to default if not found
        title = font.render("Mage.", True, (255, 255, 255))
        start_text = font.render("Press ENTER to Start", True, (200, 200, 200))
        quit_text = font.render("Press Q to Quit", True, (200, 200, 200))

        while True:
            self.screen.blit(bg, (0, 0))  # Draw the background image
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
                        return  # Start the game
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.main_menu()
    game.run_game()
