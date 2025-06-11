import pygame
from settings import Settings as st

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=None):
        super().__init__(groups)
        self.sprite_type = sprite_type

        if surface is None:
            surface = pygame.Surface((32, 32))
            # surface.fill((0, 0, 0, 0))  # Transparent

        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
