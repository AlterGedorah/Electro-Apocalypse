# player.py
import pygame
from settings import *
from support import import_cut_graphics, get_frame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)

        # Load animations AFTER display is initialized
        self.animations = {
            'idle': import_cut_graphics(r'assets/Soldier/Soldier/Soldier-Idle.png', tile_size=200),
            'walk': import_cut_graphics(r'assets/Soldier/Soldier/Soldier-Walk.png', tile_size=200),
            'attack': import_cut_graphics(r'assets/Soldier/Soldier/Soldier-Attack01.png', tile_size=200),
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
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites

        # Combat
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.hurt = False  # Make sure this is defined

    def input(self):
        keys = pygame.key.get_pressed()

        # Reset movement direction
        self.direction.x = 0
        self.direction.y = 0  # add this if you want up/down later

        # Movement keys
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_left = True
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_left = False
        
            # Vertical movement
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1


        # Attack input
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print('Attack')

        # State logic — do this AFTER setting direction & inputs
        if self.attacking:
            self.state = 'attack'
        elif self.hurt:
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
            if self.state in ['attack', 'hurt']:
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


    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking and current_time - self.attack_time >= self.attack_cooldown:
            self.attacking = False

    def update(self):
        # pygame.draw.rect(self.image, (255, 0, 0), self.image.get_rect(), 2)
        self.animate()
        self.input()
        self.cooldowns()
        self.move(self.speed)
