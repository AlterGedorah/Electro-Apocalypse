class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 400
        self.fps = 60
        self.bg = ('white')
        self.tilesize = 32

        self.monster_data = {
            'slime': {
                'health': 30,
                'exp': 50,
                'speed': 70,  # Changed from 5 to 150 pixels per second
                'attack_damage': 10,
                'attack_type': 'bash',
                'attack_sound': '../assets/sounds/slime.mp3',
                'resistance': 0.1,
                'attack_radius': 50,
                'notice_radius': 200,
        }
        }


#UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
UI_FONT = 'assets/fonts/Pixeltype.ttf'
UI_FONT_SIZE = 18

#GENERAL COLORS
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

#UI COLOR
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BOARDER_COLOR_ACTIVE = 'gold'