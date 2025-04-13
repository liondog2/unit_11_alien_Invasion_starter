from pathlib import Path
class Settings:

    def __init__(self):
        self.name: str = 'Alien Invasion'
        self.screen_w = 800
        self.screen_h = 1200
        self.FPS = 60
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'Starbasesnow.png'

        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'tank_player.png'
        self.ship_w = 128
        self.ship_h = 106
        self.ship_speed = 5

        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'bullet.png'
        self.laser_sound =Path.cwd() / 'Assets' / 'sound' / 'laser.mp3'
        self.bullet_speed = 7
        self.bullet_w = 32
        self.bullet_h = 16
        self.bullet_amount = 5

        self.alien_file = Path.cwd() / 'Assets' / 'images' / 'tank_enemy.png'
        self.alien_w = 128
        self.alien_h = 100
        self.fleet_speed = 2.5
        self.fleet_direction = 1