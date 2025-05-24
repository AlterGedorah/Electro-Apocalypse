import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos, groups,obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('assets\sol-export.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        # self.image = pygame.transform.scale(pygame.image.load('assets\sol-export.png'),(16, 16))
        self.obstacle_sprites = obstacle_sprites
        self.hitbox = self.rect.inflate(0,-10)

        self.direction = pygame.math.Vector2()
        self.speed = 5

       
    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.x > 0: #move right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #move left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #down
                        self.hitbox.bottom = sprite.hitbox.top    
                    if self.direction.y < 0: #up
                        self.hitbox.top = sprite.hitbox.bottom


    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() # Normalizing the vector
        
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        # self.rect.center += self.direction * speed
        self.rect.center = self.hitbox.center



    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: #UP
            self.direction.y = -1
        elif keys[pygame.K_s]: #Down
            self.direction.y = 1 
        else:
            self.direction.y = 0    
        
        if keys[pygame.K_a]:#Left
            self.direction.x = -1
        elif keys[pygame.K_d]: #Right
            self.direction.x = 1 
        else:
            self.direction.x = 0 #if key is not pressed 

    def update(self):
        self.input()
        self.move(self.speed)