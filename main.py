import pygame , sys
from settings import Settings
from level import Level
from debug import debug



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


if __name__ == "__main__":
    game = Game()   
    game.run_game()