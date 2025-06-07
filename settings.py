class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 400
        self.fps = 60
        self.bg = ('black')
        self.tilesize = 32
        self.tilemap = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],     # Top wall
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],     # Room 1 left, corridor, room 2 right
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],     # Walls inside rooms/corridors
        [1,0,0,0,0,0,0,'p',0,0,0,0,0,0,0,1],     # Open space inside rooms
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],     # Corridor walls with a door maybe
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],     # Big room bottom
        [1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1],      # Bottom wall
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],     # Room 1 left, corridor, room 2 right
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],     # Walls inside rooms/corridors
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],     # Open space inside rooms
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],     # Corridor walls with a door maybe
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],     # Big room bottom
        [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
        