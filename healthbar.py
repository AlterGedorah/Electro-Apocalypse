class HealthBar():
    """Healthbar gang, its responsible for your HP"""
    def init(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        #The ratio of the health
        ratio = slice.hp / self.max_hp

HealthBar = HealthBar( 250, 200, 300, 40, 100)