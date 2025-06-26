import pygame
from settings import *
from support import *
from magic import Magic, MagicMissile
from entity import Entity
class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups['main'])
        self.image = pygame.image.load('assets\player\idle\idle_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)  # Adjust hitbox size if needed 
        # Graphics setup
        self.import_player_assets()

        self.weapon_group = groups['attack']  # So it gets added to the same group `Level` uses
        self.magic = Magic(self, [groups['main']])

        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = 20
        self.obstacle_sprites = obstacle_sprites

        # Combat
        self.hurt = False  # still included if needed

        #shoot_sound
        self.shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
        #WALK
        self.walk_sound = pygame.mixer.Sound(r'sounds\walk.wav')

        # gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.shoot_cooldown = 100  # milliseconds
        # Status
        self.status = 'idle'

        # Stats for player
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'speed':10}
        self.health = self.stats['health'] 
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500  # milliseconds


        self.load_images()

    def import_player_assets(self):
        character_path = 'assets/player/'
        self.animations = {'idle': [], 'left': [], 'right': [],}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = 'idle'

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        return base_damage

    def load_images(self):
        bullet = pygame.image.load(r'assets\weapons\energy_ball.png').convert_alpha()
        self.bullet_surf = pygame.transform.smoothscale(bullet, (64, 64))  # Adjust size as needed


    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.shoot_cooldown:
                self.can_shoot = True

    def cooldown(self):
        if not self.vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_left = True
            self.status = 'left'
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_left = False
            self.status = 'right'

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'right'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'right'

                # ✅ Play walking sound only if moving
        if self.direction.x != 0 or self.direction.y != 0:
            if not self.walk_sound.get_num_channels():
                self.walk_sound.play(-1)
        else:
            self.walk_sound.stop()


        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            print("shoot")
            self.shoot_sound.play()
            # Calculate the wand tip offset (adjust values as needed)
            # wand_offset = pygame.math.Vector2(40, -30) if not self.facing_left else pygame.math.Vector2(-40, -30)
            # pos = pygame.math.Vector2(self.rect.center) + wand_offset
            pos = self.magic.rect.center + self.magic.player_direction * 40  # Adjust the offset as needed
            MagicMissile(self.bullet_surf, pos, self.magic.player_direction, self.weapon_group)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]


        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def update(self):
        self.input()
        self.cooldown()
        self.gun_timer()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.weapon_group.update()

