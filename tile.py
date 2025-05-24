import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos, groups):
        super().__init__(groups)
        self.wall = pygame.image.load('assets\WALL.png').convert_alpha()
        self.rect = self.wall.get_rect(topleft = pos)
        self.image = pygame.transform.scale(pygame.image.load('assets\WALL.png'),(32, 32))
        self.hitbox = self.rect.inflate(0,-10)