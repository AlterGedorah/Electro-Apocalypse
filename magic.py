import pygame
from math import atan2, degrees


class Magic(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player = player
        self.distance = 20
        self.direction = pygame.math.Vector2(0, 1)

        
        self.screen = pygame.display.get_surface()
        #sprite setup
        self.wand_surf = pygame.image.load(r'assets\weapons\staff.png').convert_alpha()
        self.wand_surf = pygame.transform.smoothscale(self.wand_surf, (18, 42)) 
        self.image = self.wand_surf
        self.rect = self.image.get_rect(center=player.rect.center + self.direction * self.distance)
        
    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(self.screen.get_width() // 2, self.screen.get_height() // 2)
        direction = mouse_pos - player_pos
        if direction.length() != 0:
            self.player_direction = direction.normalize()
        else:
            self.player_direction = pygame.Vector2(0, -1)

    def rotate_wand(self):
        angle = degrees(atan2(-self.player_direction.y, self.player_direction.x)) - 90  
        self.image = pygame.transform.rotozoom(self.wand_surf, angle, 1)


    def update(self, dt):  
        self.get_direction()
        self.rotate_wand()
        # Reposition the wand based on direction toward mouse
        self.rect.center = self.player.rect.center + self.player_direction * self.distance
        # Re-center the rect after rotation
        self.rect = self.image.get_rect(center=self.player.rect.center + self.player_direction * self.distance)

class MagicMissile(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = 'magic_missile'
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.spawn_time = pygame.time.get_ticks()
        self.pos = pygame.Vector2(pos)
        self.direction = direction.normalize()
        self.speed = 800  
        self.obstacle_sprites = obstacle_sprites
        self.life_time = 2000  

    def update(self, dt): 
        self.pos += self.direction * self.speed * dt  
        self.rect.center = self.pos

        # Check for lifetime expiration
        if pygame.time.get_ticks() - self.spawn_time >= self.life_time:
            self.kill()

        # Check for collisions
        hitbox = self.rect.inflate(-self.rect.width * 0.4, -self.rect.height * 0.4)
        for obstacle in self.obstacle_sprites:
            if hitbox.colliderect(obstacle.rect):
                self.kill()
                break
