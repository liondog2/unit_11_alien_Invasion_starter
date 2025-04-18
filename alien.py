import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien(Sprite):
    def __init__(self, fleet: 'AlienFleet', x: float, y: float) -> None:
        super().__init__()
        self.fleet = fleet
        self.screen = fleet.game.screen
        self.settings = fleet.game.settings
        self.boundaries = fleet.game.screen.get_rect()

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
        """
        Move the alien on the y axis at temp_speed multiplied by the current
        direction of the fleet. Update the rect.
        """
        temp_speed = self.settings.fleet_speed
        
        self.y += temp_speed * self.fleet.fleet_direction
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self) -> bool:
        """
        Check if the alien has hit an edge of the screen. If the top rect is
        less than or equal to the top bound of the screen, or the bottom rect is
        greater than or equal to the bottom bound, this will return true.
        Otherwise, false.

        Returns:
            bool: Whether or not the alien is touching a boundary.
        """
        return (
            self.rect.top <= self.boundaries.top 
            or self.rect.bottom >= self.boundaries.bottom
            )

    def draw_alien(self) -> None:
        """
        Draw the alien.
        """
        self.screen.blit(self.image, self.rect)