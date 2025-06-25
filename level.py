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
            'walls': import_csv_layout(r'assets\map\csv\TILES FOR GAME_WALLS_Walls.csv')
        }

        self.tileset = import_cut_graphics(r'assets\map\pictures\tileset.png', self.settings.tilesize)
        obstacle_ids = {str(i) for i in range(200)}  # Add more if needed

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
        # Update
        camera_offset = self.visible_sprites.get_offset(self.player)
        self.visible_sprites.update()

        # Draw all normal sprites
        self.visible_sprites.custom_draw(self.player)

        # Draw weapon manually with offset
        for weapon in self.player.weapon_group:
            offset_pos = weapon.rect.topleft - camera_offset
            self.display_surface.blit(weapon.image, offset_pos)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()


        self.floor_surf = pygame.image.load(r"assets\map\pictures\floor.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def get_offset(self, player):
        self.offset.x = player.rect.centerx - self.display_surface.get_width() // 2
        self.offset.y = player.rect.centery - self.display_surface.get_height() // 2
        return self.offset

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.display_surface.get_width() // 2
        self.offset.y = player.rect.centery - self.display_surface.get_height() // 2

        # Clear the internal surface
        self.display_surface.fill((0, 0, 0))

        # debug(player.rect.center)  # use the passed argument!
        # Draw floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # Draw sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        # Scale and blit to the main display surface
        scaled_surface = pygame.transform.scale(self.display_surface, self.display_surface.get_size())
        self.display_surface.blit(scaled_surface, (0, 0))
       