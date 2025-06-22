import pygame
import math
from settings import *
from support import import_cut_graphics, get_frame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        
        # Animation setup - ensure paths are correct
        self.animations = {
            'idle': import_cut_graphics('assets/Soldier/Soldier/Soldier-Idle.png', 64),
            'walk': import_cut_graphics('assets/Soldier/Soldier/Soldier-Walk.png', 64),
            'attack': import_cut_graphics('assets/Soldier/Soldier/Soldier-Attack01.png', 64),
            'hurt': import_cut_graphics('assets/Soldier/Soldier/Soldier-Hurt.png', 64)
        }
        
        # State management
        self.state = 'idle'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        
        # Hitbox setup - adjusted for better collision
        self.hitbox = self.rect.inflate(-20, -26)
        
        # Movement attributes
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites
        
        # Combat attributes
        self.shoot_cooldown = 0
        self.facing_left = False
        self.health = 100

    def input(self):
        if not pygame.key.get_pressed():  # Safety check
            return
            
        keys = pygame.key.get_pressed()

        # Reset direction first
        self.direction.x = 0
        self.direction.y = 0

        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_left = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_left = False

        # Vertical movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1

        # Normalize diagonal movement
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Attack input
        if (keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and not self.attacking:
            self.attack()

    def attack(self):
        self.attacking = True
        self.attack_time = pygame.time.get_ticks()
        self.shoot()

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            # Create bullet in front of player
            bullet_x = self.rect.left - 10 if self.facing_left else self.rect.right + 10
            Bullet(
                pos=(bullet_x, self.rect.centery),
                direction=-1 if self.facing_left else 1,
                groups=[self.groups()[0], BULLET_GROUP],
                facing_left=self.facing_left
            )

    def move(self, speed):
        # Horizontal movement and collision
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        
        # Vertical movement and collision
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        
        # Update rect position to match hitbox
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # Moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:  # Moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # Moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:  # Moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.attacking and current_time - self.attack_time >= self.attack_cooldown:
            self.attacking = False
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def animate(self):
        animation = self.animations[self.state]
        
        # Loop frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        # Get current frame and flip if needed
        image = animation[int(self.frame_index)]
        self.image = pygame.transform.flip(image, self.facing_left, False)

    def get_state(self):
        if self.attacking:
            self.state = 'attack'
        elif self.direction.magnitude() > 0:
            self.state = 'walk'
        else:
            self.state = 'idle'

    def update(self):
        self.input()
        self.cooldowns()
        self.get_state()
        self.animate()
        self.move(self.speed)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, facing_left=False):
        super().__init__(groups)
        
        # Visual setup
        self.image = pygame.Surface((10, 6))
        self.image.fill((255, 215, 0))  # Gold color
        self.rect = self.image.get_rect(center=pos)
        
        # Movement attributes
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = direction
        self.speed = BULLET_SPEED
        self.facing_left = facing_left
        
        # Lifetime management
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000  # Milliseconds

    def update(self):
        # Position update
        self.pos.x += self.direction * self.speed
        self.rect.centerx = round(self.pos.x)
        
        # Destroy if past lifetime or off screen
        if (pygame.time.get_ticks() - self.spawn_time > self.lifetime or
            not pygame.display.get_surface().get_rect().collidepoint(self.rect.center)):
            self.kill()
 #this one runs