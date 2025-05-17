class Settings:
    def __init__(self):
        self.screen_width = 416
        self.screen_height = 224
        self.fps = 60
        self.bg = ('white')
        self.tilesize = 32
        self.tilemap = [
        [1]*13,
        [1] + [0]*11 + [1],
        [1] + [0]*11 + [1],
        [1] + [0]*11 + [1],
        [1] + [0]*11 + [1],
        [1] + [0]*11 + [1],
        [1]*13
        ]