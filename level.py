# level.py
import pygame
from settings import Settings
from tile import Tile
from player import Player
from support import *
from debug import *


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
        layout = {
            'walls': import_csv_layout(r'assets/map/map_Walls.csv')
        }

        self.tileset = import_cut_graphics(r'assets\map\WALL_FINAL_ASE.png', self.settings.tilesize)
        obstacle_ids = {str(i) for i in range(27)}  # Add more if needed

        for style, layout_grid in layout.items():
            for row_index, row in enumerate(layout_grid):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * self.settings.tilesize
                        y = row_index * self.settings.tilesize
                        
                        tile_id = int(col)
                        if style == 'walls' and col in obstacle_ids:
                            image = self.tileset[tile_id]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'wall', image)

        self.player = Player(
            (100, 200),
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
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        # original_floor = pygame.image.load("assets/map/floor.png").convert_alpha()
        # cropped_floor = original_floor.subsurface((0, 0, 512, 416))
        
        self.zoom = 2  # zoom 
        
        # Off-screen surface for drawing
        self.internal_surface_size = (int(self.display_surface.get_width() / self.zoom),
                                      int(self.display_surface.get_height() / self.zoom))
        self.internal_surface = pygame.Surface(self.internal_surface_size)
        self.internal_rect = self.internal_surface.get_rect(center=(self.half_width, self.half_height))

        self.floor_surf = pygame.image.load(r"assets\map\mao.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.internal_surface.get_width() // 2
        self.offset.y = player.rect.centery - self.internal_surface.get_height() // 2

        # Clear the internal surface
        self.internal_surface.fill((0, 0, 0))

        # debug(player.rect.center)  # use the passed argument!
        # Draw floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.internal_surface.blit(self.floor_surf, floor_offset_pos)

        # Draw sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.internal_surface.blit(sprite.image, offset_pos)

        # Scale and blit to the main display surface
        scaled_surface = pygame.transform.scale(self.internal_surface, self.display_surface.get_size())
        self.display_surface.blit(scaled_surface, (0, 0))
       