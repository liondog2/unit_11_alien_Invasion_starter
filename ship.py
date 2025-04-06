import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship:
    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal') -> None:
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        # Ship
        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.ship_w, self.settings.ship_h)
            )
        
        self.rect = self.image.get_rect()
        self.rect.midleft = self.boundaries.midleft
        
        # Flags
        self.moving_up = False
        self.moving_down = False

        self.y = float(self.rect.y)

        self.arsenal = arsenal

    def update(self) -> None:
        # Updating the position of the ship
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        temp_speed = self.settings.ship_speed
        if self.moving_up and self.rect.bottom < self.boundaries.bottom:
            self.y += temp_speed
        if self.moving_down and self.rect.top > self.boundaries.top:
            self.y -= temp_speed
        
        self.rect.y = self.y

    def draw(self) -> None:
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self) -> None:
        return self.arsenal.fire_bullet()