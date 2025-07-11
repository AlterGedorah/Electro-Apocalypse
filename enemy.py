import pygame
from settings import *
from entity import Entity
from support import *

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player):
        self.death_sound = pygame.mixer.Sound(r"sounds\slime-impact-352473.mp3") 
        self.death_sound.set_volume(0.9)
    
        self.walk_sound = pygame.mixer.Sound(r"sounds\slime.walk.mp3")  
        self.walk_sound.set_volume(0.3)
        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.settings = Settings()
        self.direction = pygame.math.Vector2()
        self.has_died = False
        # graphics setup        
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # Movement setup
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites
        monster_data = self.settings.monster_data
        # stat
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['attack_damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400

        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300  # milliseconds
        self.damage_player = damage_player

        # Add this line for dt movement
        self.pos = pygame.Vector2(pos)
        



    def import_graphics(self,name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'assets/enemy/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_and_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize() 
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)
    
    
    def get_status(self, player):
        distance = self.get_player_distance_and_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'


    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            print(f"{self.monster_name} is attacking!")
        elif self.status == 'move':
            self.direction = self.get_player_distance_and_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)  

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255) 
    

    def get_damage(self, attack_type, player):
        
        if self.vulnerable:
            self.direction = self.get_player_distance_and_direction(player)[1]
            if attack_type == 'magic_missile':
                self.health -= player.get_full_weapon_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.walk_sound.stop() 
            self.death_sound.play()
            self.kill()
    
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True
                

    def update(self, dt): 
        self.hit_reaction()
        self.move(self.speed * dt)  
        self.animate()
        if self.direction.x != 0 or self.direction.y != 0:
            if not self.walk_sound.get_num_channels():
                self.walk_sound.play(-1)  
        else:
            self.walk_sound.stop()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player, dt):  
        self.get_status(player)
        self.actions(player)
        self.update(dt)  