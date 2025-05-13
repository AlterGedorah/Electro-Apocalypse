import pygame
from settings import Settings


class Game:
    def __init__(self):
        pygame.init()

        # Initialize settings
        self.settings = Settings()
        # Set up the time clock
        self.clock = pygame.time.Clock()
        # Set up the screen
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Electro Apocalypse")


    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.screen.fill((0, 0, 0))
            pygame.display.flip()
            self.clock.tick(self.settings.fps)


if __name__ == "__main__":
    game = Game()
    game.run_game()