import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Alien(Sprite):
    def __init__(self, game: 'AlienInvasion', x: float, y: float) -> None:
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.boundaries = game.screen.get_rect()

        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.alien_w, self.settings.alien_h)
            )
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self) -> None:
        temp_speed = self.settings.fleet_speed

        if self.check_edges():
            self.settings.fleet_direction *= -1
            self.x -= self.settings.fleet_move_speed
        
        self.y += temp_speed * self.settings.fleet_direction
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self) -> bool:
        return (
            self.rect.top <= self.boundaries.top 
            or self.rect.bottom >= self.boundaries.bottom
            )

    def draw_alien(self) -> None:
        self.screen.blit(self.image, self.rect)