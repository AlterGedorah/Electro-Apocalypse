# player.py
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('assets/sol-export.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32,32))
        self.rect = self.image.get_rect(topleft=pos)

        # Create a smaller “hitbox” inside self.rect
        self.hitbox = self.rect.inflate(0, -10)

        self.obstacle_sprites = obstacle_sprites
        self.direction = pygame.math.Vector2()
        self.speed = 5
        

    def input(self):
        keys = pygame.key.get_pressed()
        # Vertical
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        # Horizontal
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def collision(self, direction):
        """
        Move hitbox, then check collisions against each obstacle's hitbox.
        """

        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                # Compare tile.hitbox to player.hitbox
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def move(self,speed):
        # Normalize diagonal speed
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Move on X, collide, then move on Y, collide
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')

        # NOW that hitbox is final, sync rect.center BEFORE drawing
        self.rect.center = self.hitbox.center

    def update(self):
        self.input()
        self.move(self.speed)
