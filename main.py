import pygame , sys
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
        
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Electro Apocalypse")
        # pygame.display.set_icon('') 
        dt = self.clock.tick(60) / 1000  
        
        self.level = Level()

        self.paused = False


    def run_game(self): 
        while True:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
            

                
            # self.screen.fill(self.settings.bg)
            self.level.run() 
            # debug('hello')
            pygame.display.flip()
            self.clock.tick(self.settings.fps)

    def main_menu(self):
        font = pygame.font.Font(None, 80)
        title = font.render("Mage.", True, (255, 255, 255))
        start_text = font.render("Press ENTER to Start", True, (200, 200, 200))
        quit_text = font.render("Press Q to Quit", True, (200, 200, 200))

        while True:
            self.screen.fill((0, 0, 0))  # black background
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