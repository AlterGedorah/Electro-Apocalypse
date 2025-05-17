import pygame
from settings import Settings
from tile import Tile
from player import Player


class Level:
    def __init__(self):
        self.settings = Settings()
        # self.tile = Tile()
        # self.player = Player()
        # get display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()
        
        # sprite setup
        self.create_map()

    def create_map(self):
        for row_index,row in enumerate(self.settings.tilemap): 
            for col_index, col in enumerate(row):
                x = col_index * self.settings.tilesize
                y = row_index * self.settings.tilesize
                if col == 1:
                    Tile((x,y),[self.visible_sprites])


    def run(self):
        # update and draw
        self.visible_sprites.draw(self.display_surface)