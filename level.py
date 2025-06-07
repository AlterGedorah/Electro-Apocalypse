# level.py
import pygame
from settings import Settings
from tile import Tile
from player import Player

class Level:
    def __init__(self):
        self.settings = Settings()
        self.display_surface = pygame.display.get_surface()

        # Two sprite groups:
        #  - visible_sprites: for drawing (with YSortCameraGroup)
        #  - obstacle_sprites: for collision checks only (no camera needed)
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(self.settings.tilemap):
            for col_index, col in enumerate(row):
                x = col_index * self.settings.tilesize
                y = row_index * self.settings.tilesize

                if col == 1:
                    # Wall tile → belongs to both visible_sprites and obstacle_sprites
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])

                if col == 'p':
                    # Player → belongs only to visible_sprites, but knows obstacle_sprites
                    self.player = Player(
                        (x, y),
                        [self.visible_sprites],
                        self.obstacle_sprites
                    )

    def run(self):
        # Update & draw everything in visible_sprites
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] //  2 #unpacks the cords then gets the int
        self.half_height = self.display_surface.get_size()[1] //  2
        self.offset = pygame.math.Vector2()
        # Floor creation
        self.floor_surf = pygame.image.load("assets\map.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

       
    def custom_draw(self, player):
        # 1) Compute the camera offset based on player’s rect.center
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)
        # 2) Draw each sprite in ascending order of rect.centery (Y‐sort)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        
       