from pathlib import Path

class Settings:
    def __init__(self):
        self.name: str = 'Alien Invasion'
        self.screen_w = 1820
        self.screen_h = 1048
        self.FPS = 60
        self.difficulty_scale = 1.1

        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'background.png'

        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'tank_player.png'
        self.ship_w = 128
        self.ship_h = 106

        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'bullet.png'
        # For later
        # self.projectile_sounds = {
        #     Path.cwd() / 'Assets' / 'sound' / 'fireProjectile1.ogg',
        #     Path.cwd() / 'Assets' / 'sound' / 'fireProjectile2.ogg'
        # }
        
        self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'fireProjectile1.ogg'
        self.impact_sound = Path.cwd() / 'Assets' / 'sound' / 'impact1.ogg'
        

        self.alien_file = Path.cwd() / 'Assets' / 'images' / 'tank_enemy.png'
        self.alien_w = 128
        self.alien_h = 100
        self.fleet_direction = 1

        self.button_w = 200
        self.button_h = 50
        self.button_color = (0, 135, 50)

        self.text_color = (255, 255, 255)
        self.button_font_size = 48
        self.HUD_font_size = 20
        self.font_file = Path.cwd() / 'Assets' / 'Fonts' / 'Silkscreen' / 'Silkscreen-Bold.ttf'

    def initialize_dynamic_settings(self) -> None:
        self.ship_speed = 5.5
        self.starting_ship_count = 3

        self.bullet_w = 32
        self.bullet_h = 16
        self.bullet_speed = 8.5
        self.bullet_amount = 6

        self.fleet_speed = 5
        self.fleet_move_speed = self.ship_w
    
    def increase_difficulty(self) -> None:
        self.ship_speed *= self.difficulty_scale
        self.bullet_speed *= self.difficulty_scale
        self.fleet_speed *= self.difficulty_scale