import pygame
from settings import *
from support import import_cut_graphics, get_frame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)

        # Load animations
        self.animations = {
            'idle': import_cut_graphics(r'assets/Soldier/Soldier/Soldier-Idle.png', tile_size=200),
            'walk': import_cut_graphics(r'assets/Soldier/Soldier/Soldier-Walk.png', tile_size=200),
            'hurt': import_cut_graphics(r'assets/Soldier/Soldier/Soldier-Hurt.png', tile_size=200)
        }

        self.state = 'idle'
        self.facing_left = False
        self.frame_index = 0
        self.animation_speed = 0.2

        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -5)

        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = 20
        self.obstacle_sprites = obstacle_sprites

        # Combat
        self.hurt = False  # still included if needed

    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_left = True
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_left = False

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1

        if pygame.mouse.get_pressed()[0]:
            print("Shoot!")
    

        if self.hurt:
            self.state = 'hurt'
        elif self.direction.magnitude() != 0:
            self.state = 'walk'
        else:
            self.state = 'idle'

    def animate(self):
        frames = self.animations[self.state]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(frames):
            self.frame_index = 0
            if self.state == 'hurt':
                self.state = 'idle'

        self.image = get_frame(frames, int(self.frame_index), self.facing_left)

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')

        self.rect.topleft = self.hitbox.topleft

    def update(self):
        self.input()
        self.animate()
        self.move(self.speed)
