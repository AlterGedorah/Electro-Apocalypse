import pygame
from csv import reader

def import_cut_graphics(path, tile_size):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = surface.get_width() // tile_size
    tile_num_y = surface.get_height() // tile_size

    tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            frame = surface.subsurface(pygame.Rect(x, y, tile_size, tile_size)).copy()
            
            # Trim transparent pixels from the frame
            trimmed_rect = frame.get_bounding_rect()
            trimmed_frame = frame.subsurface(trimmed_rect).copy()

            tiles.append(trimmed_frame)
    return tiles

def get_frame(frames, index, facing_left):
    frame = frames[index]
    if facing_left:
        return pygame.transform.flip(frame, True, False)
    return frame

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map
