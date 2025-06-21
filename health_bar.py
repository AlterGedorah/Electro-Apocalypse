import pygame

class HealthBar():
    """Healthbar, its responsible for your HP"""
    def init(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        #The ratio of the health
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.w, self.h))  # Background
        pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y, self.w * ratio, self.h))

health_bar = HealthBar( 250, 200, 300, 40, 100)