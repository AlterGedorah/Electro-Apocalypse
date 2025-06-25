import pygame
from settings import *
from support import import_cut_graphics, get_frame
from magic import Magic, MagicMissile

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

        
        self.weapon_group = pygame.sprite.Group()
        self.magic = Magic(self, self.weapon_group)

        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = 20
        self.obstacle_sprites = obstacle_sprites

        # Combat
        self.hurt = False  # still included if needed

        # gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.shoot_cooldown = 100  # milliseconds


        # Stats for player
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'speed':5}
        self.health = self.stats['health'] * 0.5
        self.energy = self.stats['energy'] * 0.8
        self.speed = self.stats['speed']
        
        self.load_images()

    def load_images(self):
        self.bullet_surf = pygame.image.load(r'assets\weapons\energy_ball.png').convert_alpha()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.shoot_cooldown:
                self.can_shoot = True


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

        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            print("shoot")
            # Calculate the wand tip offset (adjust values as needed)
            # wand_offset = pygame.math.Vector2(40, -30) if not self.facing_left else pygame.math.Vector2(-40, -30)
            # pos = pygame.math.Vector2(self.rect.center) + wand_offset
            pos = self.magic.rect.center + self.magic.player_direction * 40  # Adjust the offset as needed
            MagicMissile(self.bullet_surf, pos, self.magic.player_direction, self.weapon_group)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            
    

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
        self.gun_timer()
        self.animate()
        self.move(self.speed)
        self.weapon_group.update()

