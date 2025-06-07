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
            'boundary': import_csv_layout(r'assets\map\level_1_floor.csv')
        }

        obstacle_ids = {'0','1', '3', '5', '7', '12','15','17','19','21', '14', '24', '25', '26'}  # Add more if needed

        for style, layout_grid in layout.items():
            for row_index, row in enumerate(layout_grid):
                for col_index, col in enumerate(row):
                    x = col_index * self.settings.tilesize
                    y = row_index * self.settings.tilesize

                    if style == 'boundary' and col != '-1' and col in obstacle_ids:
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'invisible')


        #         if col == 1:
        #             # Wall tile → belongs to both visible_sprites and obstacle_sprites
        #             Tile((x, y), [self.visible_sprites, self.obstacle_sprites])

        #         if col == 'p':
        #             # Player → belongs only to visible_sprites, but knows obstacle_sprites
        #             self.player = Player(
        #                 (x, y),
        #                 [self.visible_sprites],
        #                 self.obstacle_sprites
        #             )
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

        self.zoom = 1  # zoom 
        
        # Off-screen surface for drawing
        self.internal_surface_size = (int(self.display_surface.get_width() / self.zoom),
                                      int(self.display_surface.get_height() / self.zoom))
        self.internal_surface = pygame.Surface(self.internal_surface_size)
        self.internal_rect = self.internal_surface.get_rect(center=(self.half_width, self.half_height))

        self.floor_surf = pygame.image.load(r"assets\map\floor.png").convert()
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
       